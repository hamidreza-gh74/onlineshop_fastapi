from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRETS: str
    JWT_ALGORITHM: str
    #redis
    REDIS_URL: str = "redis://localhost:6379/0"
 


    model_config = SettingsConfigDict(
        env_file='.env',
        extra="ignore"
    )


config = Settings()




    
