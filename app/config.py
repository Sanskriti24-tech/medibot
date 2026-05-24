"""
Configuration
=============
Environment-specific settings. Following best practice, sensitive values
are read from environment variables and never hardcoded.

Select a config by setting the FLASK_ENV environment variable to one of:
    development | testing | production
"""

import os


class Config:
    """Base configuration shared by all environments."""

    # SECRET_KEY is read from the environment in production.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
    JSON_SORT_KEYS = False
    APP_NAME = "MediBot"
    APP_VERSION = "2.0"


class DevelopmentConfig(Config):
    """Used while developing locally - verbose, auto-reloads."""

    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Used when running the automated test suite."""

    DEBUG = False
    TESTING = True


class ProductionConfig(Config):
    """Used when the app is deployed and serving real users."""

    DEBUG = False
    TESTING = False


# Maps the FLASK_ENV value to the matching config class.
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config():
    """Return the config class for the current FLASK_ENV (default: dev)."""
    env = os.environ.get("FLASK_ENV", "development").lower()
    return config_by_name.get(env, DevelopmentConfig)
