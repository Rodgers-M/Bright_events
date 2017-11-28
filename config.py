import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    SECRET_KEY = "samplesecret"

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True

class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}