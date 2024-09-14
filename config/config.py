from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    token: SecretStr
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra="ignore"
    )

settings = Settings()

bot = Bot(
    token=settings.token.get_secret_value(),
    default=DefaultBotProperties(parse_mode="HTML")  # Устанавливаем свойства по умолчанию через DefaultBotProperties
)

# Функция завершения работы бота
async def on_shutdown():
    print("Бот завершает работу")

