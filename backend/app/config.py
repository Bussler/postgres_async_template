import logging
import os
import sys
import tomllib

from pydantic import BaseModel, ConfigDict


class LoggerConfig(BaseModel):
    level: int | None = None

    @classmethod
    def load_config(cls, logger_config: dict[str, str]) -> "LoggerConfig":
        logging_level = logging.DEBUG
        if "level" in logger_config:
            logging_level = cls.level_from_string(logger_config["level"])
        else:
            print("Did not find logging level specification in config, will assume DEBUG.")
        return LoggerConfig(level=logging_level)

    @staticmethod
    def level_from_string(input_string: str) -> int:
        if input_string == "INFO":
            return logging.INFO
        if input_string == "DEBUG":
            return logging.DEBUG
        if input_string == "ERROR":
            return logging.ERROR
        if input_string == "WARNING":
            return logging.WARNING
        return logging.DEBUG


class PostgresConfig(BaseModel):
    database: str
    host: str
    port: str
    user: str
    password: str

    def get_connection_string(self) -> str:
        if os.getenv("USINGDOCKER", "False") == "True":
            return f"postgresql+asyncpg://{self.user}:{self.password}@db/{self.database}"
        else:
            return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    model_config = ConfigDict(from_attributes=True)


def config_load() -> tuple[LoggerConfig, PostgresConfig]:
    """Load configs from config.toml file.

    Returns:
        tuple[LoggerConfig, CORSConfig, APIConfig]: Parsed configs.
    """
    config_path = os.getenv("CONFIG_PATH", "./config.toml")
    if not os.path.exists(config_path):
        print(f"Config {config_path} does not exist, aborting parsing")
        return sys.exit(1)

    with open(config_path, "rb") as f:
        data = tomllib.load(f)
        try:
            # Add configs to load here
            logger_config: LoggerConfig = LoggerConfig.load_config(data.get("logging"))  # type: ignore
            postgres_config: PostgresConfig = PostgresConfig.model_validate(data.get("postgres"))
        except Exception as e:
            print(f"Something went wrong in parsing the config file: {e}")
            return sys.exit(1)
    return logger_config, postgres_config


class ConfigController:
    """Controller to load and cache configs when they are needed. Implements the singleton pattern.

    Can be accessed by CONFIGS.instance.<Config>.<ConfigAttribute>.

    E.g. CONFIGS.instance.LOGGER_CONFIG.level

    Configs:
        LOGGER_CONFIG: LoggerConfig
        POSTGRES_CONFIG: PostgresConfig
    """

    _initialized: bool = False
    instance: "ConfigController"

    def __new__(cls) -> "ConfigController":
        if not cls._initialized:
            cls.instance = super(ConfigController, cls).__new__(cls)
            cls._initialized = True
        return cls.instance

    def __init__(self) -> None:
        self._logger_config: LoggerConfig | None = None
        self._postgres_config: PostgresConfig | None = None

    def _init_configs(self) -> None:
        (
            self._logger_config,
            self._postgres_config,
        ) = config_load()

    @property
    def LOGGER_CONFIG(self) -> LoggerConfig:
        if self._logger_config is None:
            self._init_configs()
            assert self._logger_config is not None
        return self._logger_config

    @property
    def POSTGRES_CONFIG(self) -> PostgresConfig:
        if self._postgres_config is None:
            self._init_configs()
            assert self._postgres_config is not None
        return self._postgres_config

CONFIGS: ConfigController = ConfigController()
