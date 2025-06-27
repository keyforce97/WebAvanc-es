import os

class Config:
    """Configuration de l'application Flask."""
    
    # Configuration Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    
    # Configuration base de données PostgreSQL
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'pass')
    DB_PORT = int(os.environ.get('DB_PORT', '5432'))
    DB_NAME = os.environ.get('DB_NAME', 'api8inf349')
    
    # Configuration Redis
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
    
    # Configuration RQ
    RQ_DEFAULT_TIMEOUT = 600  # 10 minutes
    
    @staticmethod
    def init_app(app):
        """Initialise l'application avec cette configuration."""
        pass

class DevelopmentConfig(Config):
    """Configuration pour le développement."""
    DEBUG = True

class ProductionConfig(Config):
    """Configuration pour la production."""
    DEBUG = False

class TestingConfig(Config):
    """Configuration pour les tests."""
    TESTING = True
    DB_NAME = os.environ.get('TEST_DB_NAME', 'test_api8inf349')

# Configuration par défaut
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


