from pydantic import BaseSettings


class NetworkStoreAPIEnvironmentVariables(BaseSettings):
    class Config:
        env_file = "kisters_network_store.env"

    api_path: str = "/rest"
    deployment_url: str = ""
    enable_access_control: bool = False
    enable_static_assets: bool = False
    enable_viewer: bool = True
