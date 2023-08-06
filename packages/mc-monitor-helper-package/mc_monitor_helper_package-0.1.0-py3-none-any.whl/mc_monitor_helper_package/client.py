import sys
from typing import Any, Dict, List

from mc_monitor_helper_package.auth import MonteCarloAuth
from mc_monitor_helper_package.exceptions import NoNewMonitorsFoundError
from mc_monitor_helper_package.mc_state import MonteCarloState
from mc_monitor_helper_package.mc_table import (
    MonteCarloTableContext,
    combine_tables_with_monitor,
    find_tables_without_monitor,
    parse_tables,
)
from mc_monitor_helper_package.mc_update import set_monitor


def prepare_tables_for_update(
    tablenames_to_monitor: List[str], auth: MonteCarloAuth, update_monitors: bool
) -> List[MonteCarloTableContext]:
    tables_to_monitor = parse_tables(tablenames_to_monitor)
    state = MonteCarloState(auth=auth)
    wh_id = state.get_warehouse_id()
    monitors = state.get_existing_monitors(monitor_types=["stats"])

    if update_monitors:
        tables_with_monitor_context = combine_tables_with_monitor(
            tables_to_monitor, monitors
        )

        return [
            table.get_mc_information(auth=auth, dw_id=wh_id)
            for table in tables_with_monitor_context
        ]

    else:
        try:
            tables_without_monitor = find_tables_without_monitor(
                tables_to_monitor, monitors
            )
        except NoNewMonitorsFoundError as e:
            sys.exit(e)

        return [
            table.get_mc_information(auth=auth, dw_id=wh_id)
            for table in tables_without_monitor
        ]


def create_or_update_monitors(
    tables_with_context: List[MonteCarloTableContext],
    fields_to_ignore: List[str],
    time_field: str,
    auth: MonteCarloAuth,
) -> List[Dict[Any, Any]]:
    monitors_set: List[Dict[Any, Any]] = []
    for table in tables_with_context:
        if table.evaluate_if_monitorable(time_field):
            monitor = set_monitor(
                auth=auth,
                table_with_context=table,
                fields=table.fields,
                fields_to_ignore=fields_to_ignore,
                time_field=time_field,
            )
            monitors_set.append(monitor)
            print(
                f"Monitor created: {monitor['createOrUpdateMonitor']['monitor']['uuid']}"
            )

    print(f"Created {len(monitors_set)} monitors")
    return monitors_set
