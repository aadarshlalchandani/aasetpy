from src.utils import BaseSettings, lru_cache
from typing import Any


class ENVSettings(BaseSettings):
    class Config:
        env_file = ".env"
        extra = "allow"


env_settings = ENVSettings()


class EnvironmentVariables:
    @lru_cache
    def __getattr__(self, env_var_name):
        return getattr(env_settings, env_var_name.lower(), None)
    
    def __call__(self, env_var_name: str, default_value: Any = None) -> Any:
        value = getattr(env_settings, env_var_name.lower(), None)
        return value if value is not None else default_value


env = EnvironmentVariables()
