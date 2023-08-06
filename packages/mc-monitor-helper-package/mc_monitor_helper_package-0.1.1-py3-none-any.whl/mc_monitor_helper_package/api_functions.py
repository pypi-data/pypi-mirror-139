from typing import Dict, List, Optional, Protocol, Tuple, Union

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from mc_monitor_helper_package.auth import MonteCarloAuth


class ApiExecutable(Protocol):
    query: str
    params: Optional[dict] = None

    def parse_response(self, response: dict) -> Union[dict, str, List]:
        ...


def query_mc_api(
    auth: MonteCarloAuth,
    executable: ApiExecutable,
) -> Union[Dict, str, List, Tuple]:
    transport = RequestsHTTPTransport(
        url="https://api.getmontecarlo.com/graphql",
        headers=auth.auth_headers,
    )
    query = gql(executable.query)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    response = client.execute(query, variable_values=executable.params)
    return executable.parse_response(response)
