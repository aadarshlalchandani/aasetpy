from src.utils import BaseSettings, lru_cache


class ENVSettings(BaseSettings):
    class Config:
        env_file = ".env"
        extra = "allow"


env_settings = ENVSettings()


class EnvironmentVariables:
    @lru_cache
    def __getattr__(self, env_var_name):
        return getattr(env_settings, env_var_name.lower(), None)


env = EnvironmentVariables()
