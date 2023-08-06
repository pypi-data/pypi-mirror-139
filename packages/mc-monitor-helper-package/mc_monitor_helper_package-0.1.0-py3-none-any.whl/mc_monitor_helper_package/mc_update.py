from typing import Any, Dict, List

from mc_monitor_helper_package.api_functions import query_mc_api
from mc_monitor_helper_package.auth import MonteCarloAuth
from mc_monitor_helper_package.mc_table import MonteCarloTableContext
from mc_monitor_helper_package.queries import CreateOrUpdateMonitorSetter


def set_monitor(
    auth: MonteCarloAuth,
    table_with_context: MonteCarloTableContext,
    fields: List[str],
    fields_to_ignore: List[str],
    time_field: str,
    monitor_type: str = "stats",
    schedule_config: Dict = {"scheduleType": "LOOSE", "intervalMinutes": 720},
) -> Dict[Any, Any]:
    time_field = str.lower(time_field)
    fields_to_ignore = [str.lower(field) for field in fields_to_ignore]
    fields_filtered = [field for field in fields if field not in fields_to_ignore]
    return query_mc_api(
        auth=auth,
        executable=CreateOrUpdateMonitorSetter(
            mcon=table_with_context.mcon,
            fields=fields_filtered,
            time_axis_type=table_with_context.fields[time_field],
            time_axis_name=time_field,
            aggregation_time_interval="HOUR",
            lookback_days=1,
            monitor_type=monitor_type,
            schedule_config=schedule_config,
            uuid=table_with_context.monitor_id,
        ),
    )
