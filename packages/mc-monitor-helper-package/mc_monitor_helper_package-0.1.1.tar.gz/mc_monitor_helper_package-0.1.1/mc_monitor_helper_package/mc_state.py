from typing import List

from mc_monitor_helper_package import auth, queries
from mc_monitor_helper_package.api_functions import query_mc_api
from mc_monitor_helper_package.auth import MonteCarloAuth
from mc_monitor_helper_package.mc_table import MonteCarloTable


class MonteCarloState:
    def __init__(self, auth: MonteCarloAuth):
        self.auth = auth

    def get_warehouse_id(self) -> str:
        print("Getting monte carlo warehouse id")
        return query_mc_api(auth=self.auth, executable=queries.WarehouseIdGetter())

    def get_existing_monitors(self, monitor_types: List[str]) -> List[MonteCarloTable]:
        print("Finding existing monitors")
        return query_mc_api(
            auth=self.auth,
            executable=queries.ExistingMonitorGetter(
                user_defined_monitor_types=monitor_types
            ),
        )
