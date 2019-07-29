"""Configuration File."""
import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False


class DevelopmentConfig(Config):

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BROKER_URL = os.getenv("REDIS_URL")


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BROKER_URL = os.getenv("REDIS_URL")


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URI')


class ConfigureApplication:
    """Application."""

    config_by_name = {
        "development": "api.configuration.config.DevelopmentConfig",
        "testing": "api.configuration.config.TestingConfig",
        "production": "api.configuration.config.ProductionConfig"
    }
    app_environment = os.getenv("APP_ENVIRONMENT")

    @classmethod
    def set_config(cls):
        """Set application configuration."""

        return cls.config_by_name[cls.app_environment]
