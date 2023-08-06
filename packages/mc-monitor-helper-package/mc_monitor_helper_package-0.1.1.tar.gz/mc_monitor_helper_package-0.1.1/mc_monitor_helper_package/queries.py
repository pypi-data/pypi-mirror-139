from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from mc_monitor_helper_package.mc_table import MonteCarloTable, parse_mc_table


@dataclass
class WarehouseIdGetter:
    query: str = """
        query getUser {
        getUser {
            account {
            warehouses {
                uuid
                connectionType
            }
            }
        }
        }
    """

    @property
    def params(self) -> None:
        return

    @staticmethod
    def parse_response(response: dict) -> Optional[str]:
        return response["getUser"]["account"]["warehouses"][0]["uuid"]


@dataclass
class ExistingMonitorGetter:
    user_defined_monitor_types: Optional[list]
    query: str = """
        query getAllUserDefinedMonitors($userDefinedMonitorTypes: [String], $first: Int, $cursor: String) {
        getAllUserDefinedMonitorsV2(userDefinedMonitorTypes: $userDefinedMonitorTypes, first: $first, after: $cursor) {
            pageInfo {
            startCursor
            endCursor
            hasNextPage
            hasPreviousPage
            __typename
            }
            edges {
            node {
                __typename
                id
                uuid
                monitorType
                entities
                customRuleEntities: entities
            }
            __typename
            }
            __typename
        }
        }
        """

    @property
    def params(self) -> dict:
        return {
            "userDefinedMonitorTypes": self.user_defined_monitor_types,
            "first": 500,
        }

    @staticmethod
    def parse_response(response: dict) -> List[MonteCarloTable]:
        if response["getAllUserDefinedMonitorsV2"]["pageInfo"]["hasNextPage"]:
            raise NotImplementedError("Pagination not implemented")
        return [
            parse_mc_table(
                monitor["node"]["customRuleEntities"][0], monitor["node"]["uuid"]
            )
            for monitor in response["getAllUserDefinedMonitorsV2"]["edges"]
        ]


@dataclass
class MconsForTablesGetter:
    full_table_id: str
    dw_id: str
    query: str = """
        query getTable($dwId: UUID, $fullTableId: String, $mcon: String, $cursor: String, $versions: Int = 1, $first: Int = 1000) {
        getTable(dwId: $dwId, fullTableId: $fullTableId, mcon: $mcon) {
            id
            mcon
            fullTableId
            versions(first: $versions) {
            edges {
                node {
                fields(first: $first, after: $cursor) {
                    edges {
                    node {
                        name
                        fieldType
                        isTimeField
                        __typename
                    }
                    __typename
                    }
                    __typename
                }
                __typename
                }
                __typename
            }
            __typename
            }
            __typename
        }
        }
    """

    @property
    def params(self) -> dict:
        return {
            "fullTableId": self.full_table_id,
            "dwId": self.dw_id,
        }

    @staticmethod
    def parse_response(response: dict) -> Tuple[str, Dict]:
        mcon = response["getTable"]["mcon"]
        timefields = {
            node["node"]["name"]: node["node"]["fieldType"]
            for node in response["getTable"]["versions"]["edges"][0]["node"]["fields"][
                "edges"
            ]
        }
        return mcon, timefields


@dataclass
class CreateOrUpdateMonitorSetter:
    mcon: str
    fields: List[str]
    time_axis_type: str
    time_axis_name: str
    aggregation_time_interval: str
    lookback_days: int
    monitor_type: str
    schedule_config: dict
    where_contition: Optional[str] = None
    uuid: Optional[str] = None
    query: str = """
    mutation createOrUpdateMonitor($mcon: String!, $monitorType: String!, $fields: [String], $timeAxisName: String, $timeAxisType: String, $scheduleConfig: ScheduleConfigInput, $uuid: UUID, $whereCondition: String, $aggTimeInterval: MonitorAggTimeInterval, $lookbackDays: Int) {
    createOrUpdateMonitor(
        mcon: $mcon
        monitorType: $monitorType
        fields: $fields
        timeAxisName: $timeAxisName
        timeAxisType: $timeAxisType
        scheduleConfig: $scheduleConfig
        uuid: $uuid
        whereCondition: $whereCondition
        aggTimeInterval: $aggTimeInterval
        lookbackDays: $lookbackDays
    ) {
        monitor {
        uuid
        type
        fields
        entities
        timeAxisFieldName
        timeAxisFieldType
        aggTimeInterval
        aggSelectExpression
        historyDays
        whereCondition
        fullTableId
        selectExpressions {
            id
            expression
            dataType
            isRawColumnName
            __typename
        }
        scheduleConfig {
            scheduleType
            intervalMinutes
            startTime
            minIntervalMinutes
            __typename
        }
        schedule {
            resourceId
            __typename
        }
        __typename
        }
        __typename
    }
    }   
    """

    @property
    def params(self) -> dict:
        params = {
            "uuid": self.uuid,
            "mcon": self.mcon,
            "monitorType": self.monitor_type,
            "fields": self.fields,
            "timeAxisName": self.time_axis_name,
            "timeAxisType": self.time_axis_type,
            "aggTimeInterval": str.upper(self.aggregation_time_interval),
            "lookbackDays": self.lookback_days,
            "whereCondition": self.where_contition,
            "scheduleConfig": self.schedule_config,
        }
        return params

    @staticmethod
    def parse_response(response: Dict) -> Dict:
        return response
