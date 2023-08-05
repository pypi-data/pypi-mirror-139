"""
Defines the Orion FastAPI app.
"""

import asyncio
import os
from functools import partial
from typing import Dict, List, Optional

from fastapi import Depends, FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

import prefect
import prefect.orion.api as api
import prefect.orion.services as services
import prefect.settings
from prefect.logging import get_logger
from prefect.orion.api.dependencies import CheckVersionCompatibility

TITLE = "Prefect Orion"
API_TITLE = "Prefect Orion API"
UI_TITLE = "Prefect Orion UI"
API_VERSION = prefect.__version__
ORION_API_VERSION = "0.1.0"

logger = get_logger("orion")

version_checker = CheckVersionCompatibility(ORION_API_VERSION, logger)


class SPAStaticFiles(StaticFiles):
    # This class overrides the get_response method
    # to ensure that when a resource isn't found the application still
    # returns the index.html file. This is required for SPAs
    # since in-app routing is handled by a single html file.
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        if response.status_code == 404:
            response = await super().get_response("./index.html", scope)
        return response


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Provide a detailed message for request validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "exception_message": "Invalid request received.",
                "exception_detail": exc.errors(),
                "request_body": exc.body,
            }
        ),
    )


async def custom_internal_exception_handler(request: Request, exc: Exception):
    """Log a detailed exception for internal server errors before returning."""
    logger.error(f"Encountered exception in request:", exc_info=True)
    return JSONResponse(
        content={"exception_message": "Internal Server Error"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def create_orion_api(
    router_prefix: Optional[str] = "",
    include_admin_router: Optional[bool] = True,
    dependencies: Optional[List[Depends]] = None,
    health_check_path: str = "/health",
    fast_api_app_kwargs: dict = None,
) -> FastAPI:
    """
    Create a FastAPI app that includes the Orion API

    Args:
        router_prefix: a prefix to apply to all included routers
        include_admin_router: whether or not to include admin routes, these routes
            have can take desctructive actions like resetting the database
        dependencies: a list of global dependencies to add to each Orion router
        health_check_path: the health check route path
        fast_api_app_kwargs: kwargs to pass to the FastAPI constructor

    Returns:
        a FastAPI app that serves the Orion API
    """
    fast_api_app_kwargs = fast_api_app_kwargs or {}
    api_app = FastAPI(title=API_TITLE, **fast_api_app_kwargs)

    @api_app.get(health_check_path)
    async def health_check():
        return True

    # always include version checking
    if dependencies is None:
        dependencies = [Depends(version_checker)]
    else:
        dependencies.append(Depends(version_checker))

    # api routers
    api_app.include_router(
        api.data.router, prefix=router_prefix, dependencies=dependencies
    )
    api_app.include_router(
        api.flows.router, prefix=router_prefix, dependencies=dependencies
    )
    api_app.include_router(
        api.flow_runs.router, prefix=router_prefix, dependencies=dependencies
    )
    api_app.include_router(
        api.task_runs.router, prefix=router_prefix, dependencies=dependencies
    )
    api_app.include_router(
        api.flow_run_states.router, prefix=router_prefix, dependencies=dependencies
    )
    api_app.include_router(
        api.task_run_states.router, prefix=router_prefix, dependencies=dependencies
    )
    api_app.include_router(
        api.deployments.router, prefix=router_prefix, dependencies=dependencies
    )
    api_app.include_router(
        api.saved_searches.router, prefix=router_prefix, dependencies=dependencies
    )
    api_app.include_router(
        api.logs.router, prefix=router_prefix, dependencies=dependencies
    )
    api_app.include_router(
        api.concurrency_limits.router, prefix=router_prefix, dependencies=dependencies
    )

    if include_admin_router:
        api_app.include_router(
            api.admin.router, prefix=router_prefix, dependencies=dependencies
        )

    return api_app


APP_CACHE: Dict[prefect.settings.Settings, FastAPI] = {}


def create_app(settings: prefect.settings.Settings = None) -> FastAPI:
    """Create an FastAPI app that includes the Orion API and UI"""
    settings = settings or prefect.settings.get_current_settings()

    if settings in APP_CACHE:
        return APP_CACHE[settings]

    app = FastAPI(title=TITLE, version=API_VERSION)
    api_app = create_orion_api(
        fast_api_app_kwargs={
            "exception_handlers": {
                Exception: custom_internal_exception_handler,
                RequestValidationError: validation_exception_handler,
            }
        }
    )
    ui_app = FastAPI(title=UI_TITLE)

    # middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api_app.mount(
        "/static",
        StaticFiles(
            directory=os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "static"
            )
        ),
        name="static",
    )

    app.mount("/api", app=api_app)
    if (
        os.path.exists(prefect.__ui_static_path__)
        and prefect.settings.PREFECT_ORION_UI_ENABLED.value()
    ):
        ui_app.mount(
            "/",
            SPAStaticFiles(directory=prefect.__ui_static_path__, html=True),
            name="ui_root",
        )
        app.mount("/", app=ui_app, name="ui")
    else:
        pass

    def openapi():
        """
        Convenience method for extracting the user facing OpenAPI schema from the API app.

        This method is attached to the global public app for easy access.
        """
        partial_schema = get_openapi(
            title=API_TITLE,
            version=API_VERSION,
            routes=api_app.routes,
        )
        new_schema = partial_schema.copy()
        new_schema["paths"] = {}
        for path, value in partial_schema["paths"].items():
            new_schema["paths"][f"/api{path}"] = value

        new_schema["info"]["x-logo"] = {"url": "static/prefect-logo-mark-gradient.png"}
        return new_schema

    app.openapi = openapi

    @app.on_event("startup")
    async def start_services():
        """Start additional services when the Orion API starts up."""
        if prefect.settings.PREFECT_ORION_SERVICES_RUN_IN_APP.value():
            loop = asyncio.get_running_loop()
            service_instances = [
                services.scheduler.Scheduler(),
                services.late_runs.MarkLateRuns(),
            ]
            app.state.services = {
                service: loop.create_task(service.start())
                for service in service_instances
            }

            for service, task in app.state.services.items():
                logger.info(f"{service.name} service scheduled to start in-app")
                task.add_done_callback(partial(on_service_exit, service))
        else:
            logger.info(
                "In-app services have been disabled and will need to be run separately."
            )
            app.state.services = None

    @app.on_event("shutdown")
    async def wait_for_service_shutdown():
        """Ensure services are stopped before the Orion API shuts down."""
        if app.state.services:
            await asyncio.gather(*[service.stop() for service in app.state.services])
            try:
                await asyncio.gather(
                    *[task.stop() for task in app.state.services.values()]
                )
            except Exception as exc:
                # `on_service_exit` should handle logging exceptions on exit
                pass

    def on_service_exit(service, task):
        """
        Added as a callback for completion of services to log exit
        """
        try:
            # Retrieving the result will raise the exception
            task.result()
        except Exception:
            logger.error(f"{service.name} service failed!", exc_info=True)
        else:
            logger.info(f"{service.name} service stopped!")

    APP_CACHE[settings] = app

    return app
