from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    github_base_url: str = "https://api.github.com"
    static_dir: str = "app/static"

    class Config:
        env_prefix = "APP_"
        env_file = ".env"
