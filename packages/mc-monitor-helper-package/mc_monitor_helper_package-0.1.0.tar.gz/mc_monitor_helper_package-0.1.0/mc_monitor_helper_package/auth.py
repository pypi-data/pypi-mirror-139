import os
from dataclasses import dataclass


@dataclass
class MonteCarloAuth:
    x_mcd_id: str
    x_mcd_token: str

    @property
    def auth_headers(self) -> dict[str, str]:
        return {"x-mcd-id": self.x_mcd_id, "x-mcd-token": self.x_mcd_token}


def get_monte_carlo_auth_from_env():
    return MonteCarloAuth(
        x_mcd_id=str(os.environ.get("X_MCD_ID")),
        x_mcd_token=str(os.environ.get("X_MCD_TOKEN")),
    )


def get_monte_carlo_auth(x_mcd_id: str, x_mcd_token: str) -> MonteCarloAuth:
    return MonteCarloAuth(x_mcd_id, x_mcd_token)
