from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY:str
    SQLALCHEMY_DATABASE_URL : str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    class Config:
        env_file=".env"

settings=Settings()