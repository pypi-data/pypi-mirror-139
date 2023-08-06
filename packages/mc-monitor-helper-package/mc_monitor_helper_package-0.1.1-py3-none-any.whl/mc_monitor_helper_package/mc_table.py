from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from mc_monitor_helper_package import queries
from mc_monitor_helper_package.api_functions import query_mc_api
from mc_monitor_helper_package.auth import MonteCarloAuth
from mc_monitor_helper_package.exceptions import (
    DuplicateMonitorsFoundError,
    NoNewMonitorsFoundError,
)


@dataclass
class MonteCarloTable:
    database: str
    schema: str
    table_name: str
    monitor_id: Optional[str] = None

    def __eq__(self, other: MonteCarloTable):
        return self.full_table_name == other.full_table_name

    @property
    def full_table_name(self) -> str:
        return str.lower(f"{self.database}:{self.schema}.{self.table_name}")

    def __repr__(self) -> str:
        return self.full_table_name

    def get_mc_information(
        self, auth: MonteCarloAuth, dw_id: str
    ) -> MonteCarloTableContext:
        mcon, fields = query_mc_api(
            auth=auth,
            executable=queries.MconsForTablesGetter(
                full_table_id=str(self.full_table_name), dw_id=dw_id
            ),
        )
        return MonteCarloTableContext(table=self, fields=fields, mcon=mcon)


@dataclass
class MonteCarloTableContext:
    table: MonteCarloTable
    fields: Dict
    mcon: str

    def evaluate_if_monitorable(self, timefield: str) -> bool:
        return str.lower(timefield) in [
            name
            for name, field_type in self.fields.items()
            if "timestamp" in field_type
        ]

    @property
    def monitor_id(self) -> Optional[str]:
        return self.table.monitor_id

    def __repr__(self) -> str:
        return str(self.table)


def parse_tables(tables_to_monitor: List[str]) -> list:
    clean_tables_to_monitor = [
        str.lower(table).split(".") for table in tables_to_monitor
    ]
    return [
        MonteCarloTable(
            database=table_to_monitor[0],
            schema=table_to_monitor[1],
            table_name=table_to_monitor[2],
        )
        for table_to_monitor in clean_tables_to_monitor
    ]


def parse_mc_table(table: str, monitor_id: str) -> MonteCarloTable:
    table_to_monitor = table.replace(":", ".")
    return MonteCarloTable(
        database=table_to_monitor.split(".")[0],
        schema=table_to_monitor.split(".")[1],
        table_name=table_to_monitor.split(".")[2],
        monitor_id=monitor_id,
    )


def find_tables_without_monitor(
    database_tables: List[MonteCarloTable],
    tables_with_monitor: List[MonteCarloTable],
) -> List[MonteCarloTable]:
    tables_with_monitor = [
        table for table in database_tables if table not in tables_with_monitor
    ]
    if len(tables_with_monitor) == 0:
        raise NoNewMonitorsFoundError("No new tables to monitor")
    return tables_with_monitor


def combine_tables_with_monitor(
    database_tables: List[MonteCarloTable],
    tables_with_monitor: List[MonteCarloTable],
) -> List[MonteCarloTable]:
    tables_with_monitor_context: List[MonteCarloTable] = [
        table for table in tables_with_monitor if table in database_tables
    ]

    for table in database_tables:
        if table not in tables_with_monitor_context:
            tables_with_monitor_context.append(table)

    if len({table.full_table_name for table in tables_with_monitor_context}) != len(
        tables_with_monitor_context
    ):
        raise DuplicateMonitorsFoundError("Duplicate tables found")
    return tables_with_monitor_context
