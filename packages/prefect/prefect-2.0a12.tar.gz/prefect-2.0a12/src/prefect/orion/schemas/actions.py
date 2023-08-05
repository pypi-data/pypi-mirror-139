"""
Reduced schemas for accepting API actions.
"""
from typing import List

from pydantic import Field

import prefect.orion.schemas as schemas
from prefect.orion.utilities.schemas import PrefectBaseModel


class FlowCreate(
    schemas.core.Flow.subclass(
        name="FlowCreate",
        include_fields=["name", "tags"],
    )
):
    """Data used by the Orion API to create a flow."""


class FlowUpdate(
    schemas.core.Flow.subclass(name="FlowUpdate", include_fields=["tags"])
):
    """Data used by the Orion API to update a flow."""


class DeploymentCreate(
    schemas.core.Deployment.subclass(
        name="DeploymentCreate",
        include_fields=[
            "name",
            "flow_id",
            "schedule",
            "is_schedule_active",
            "tags",
            "parameters",
            "flow_data",
            "flow_runner",
        ],
    )
):
    """Data used by the Orion API to create a deployment."""


class FlowRunUpdate(
    schemas.core.FlowRun.subclass(
        name="FlowRunUpdate",
        include_fields=["flow_version", "parameters", "name", "flow_runner"],
    )
):
    """Data used by the Orion API to update a flow run."""


class StateCreate(
    schemas.states.State.subclass(
        name="StateCreate",
        include_fields=[
            "type",
            "name",
            "message",
            "data",
            "state_details",
        ],
    )
):
    """Data used by the Orion API to create a new state."""


class TaskRunCreate(
    schemas.core.TaskRun.subclass(
        name="TaskRunCreate",
        include_fields=[
            "name",
            "flow_run_id",
            "task_key",
            "dynamic_key",
            "cache_key",
            "cache_expiration",
            "task_version",
            "empirical_policy",
            "tags",
            "task_inputs",
        ],
    )
):
    """Data used by the Orion API to create a task run"""

    # TaskRunCreate states must be provided as StateCreate objects
    state: StateCreate = Field(None, description="The state of the task run to create")


class FlowRunCreate(
    schemas.core.FlowRun.subclass(
        name="FlowRunCreate",
        include_fields=[
            "name",
            "flow_id",
            "deployment_id",
            "flow_version",
            "parameters",
            "context",
            "tags",
            "idempotency_key",
            "parent_task_run_id",
            "flow_runner",
        ],
    )
):
    """Data used by the Orion API to create a flow run."""

    # FlowRunCreate states must be provided as StateCreate objects
    state: StateCreate = Field(None, description="The state of the flow run to create")


class DeploymentFlowRunCreate(
    schemas.core.FlowRun.subclass(
        name="FlowRunCreate",
        include_fields=[
            "name",
            "parameters",
            "context",
            "tags",
            "idempotency_key",
            "flow_runner",
        ],
    )
):
    """Data used by the Orion API to create a flow run from a deployment."""

    # FlowRunCreate states must be provided as StateCreate objects
    state: StateCreate = Field(None, description="The state of the flow run to create")


class SavedSearchCreate(
    schemas.core.SavedSearch.subclass(
        name="SavedSearchCreate",
        include_fields=["name", "filters"],
    )
):
    """Data used by the Orion API to create a saved search."""


class ConcurrencyLimitCreate(
    schemas.core.ConcurrencyLimit.subclass(
        name="ConcurrencyLimitCreate",
        include_fields=["tag", "concurrency_limit"],
    )
):
    """Data used by the Orion API to create a concurrency limit"""


class LogCreate(
    schemas.core.Log.subclass(
        name="LogCreate",
        include_fields=[
            "name",
            "level",
            "message",
            "timestamp",
            "flow_run_id",
            "task_run_id",
        ],
    )
):
    """Data used by the Orion API to create a log."""
