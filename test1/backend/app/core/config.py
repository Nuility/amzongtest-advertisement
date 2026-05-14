from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
import os


class Settings(BaseSettings):
    app_name: str = "Amazon Ads Intelligent Platform"
    app_version: str = "1.0.0"
    debug: bool = False
    
    database_url: str = "mysql+pymysql://user:pass@localhost:3306/amazon_ads"
    database_pool_size: int = 50
    database_max_overflow: int = 100
    database_pool_timeout: int = 30
    database_pool_recycle: int = 3600
    
    clickhouse_host: str = "localhost"
    clickhouse_port: int = 9000
    clickhouse_db: str = "amazon_ads"
    
    redis_url: str = "redis://localhost:6379/0"
    redis_max_connections: int = 100
    redis_socket_timeout: int = 5
    
    amazon_ads_api_base: str = "https://advertising-api.amazon.com"
    amazon_sp_api_base: str = "https://sellingpartnerapi-na.amazon.com"
    amazon_api_timeout: int = 30
    amazon_api_max_retries: int = 3
    
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"
    celery_task_serializer: str = "json"
    celery_result_serializer: str = "json"
    celery_accept_content: list = ["json"]
    
    log_level: str = "INFO"
    log_format: str = "json"
    log_file_path: Optional[str] = None
    
    cache_default_ttl: int = 300
    cache_max_ttl: int = 3600
    cache_slow_query_threshold: float = 1.0
    
    performance_slow_request_threshold: float = 1.0
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def validate_settings(self) -> None:
        if self.jwt_secret_key == "your-secret-key-change-in-production":
            if not self.debug:
                raise ValueError("JWT secret key must be changed in production environment")
        
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.log_level.upper() not in valid_log_levels:
            raise ValueError(f"Invalid log level: {self.log_level}. Must be one of {valid_log_levels}")


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    settings.validate_settings()
    return settings
