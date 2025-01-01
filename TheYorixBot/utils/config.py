import json
import pathlib
import re

import decouple

__all__ = ()


def postgres_port_cast(value):
    match = re.search(r":(\d+)", value)
    if match:
        return int(match.group(1))

    return value


def lst_cast(value):
    lst = value.split(", ")
    return list(map(int, lst))


class YorixField:
    def __init__(self, env=None, default=None, cast=str, to_save=False):
        self.value = default
        if env:
            self.value = decouple.config(env, default, cast=cast)

        self.to_save = to_save


class YorixMeta(type):
    def __new__(cls, name, bases, namespace):
        fields = {}
        to_remove = []
        for key, value in namespace.items():
            if (
                key.startswith("__")
                and key.endswith("__")
                or key in ["load_config", "save_config"]
            ):
                continue

            if isinstance(value, YorixField):
                fields[key] = value
            else:
                fields[key] = YorixField(default=value, to_save=False)

            to_remove.append(key)

        namespace["fields"] = fields
        for key in to_remove:
            del namespace[key]

        return super().__new__(cls, name, bases, namespace)


class YorixConfig(metaclass=YorixMeta):
    def __init__(self, config=None):
        self.config_file = config or "data/configs/config.json"
        self.load_config()

    def load_config(self):
        if pathlib.Path(self.config_file).exists():
            with pathlib.Path(self.config_file).open("r", encoding="UTF-8") as f:
                saved_data = json.load(f)
                for key, value in saved_data.items():
                    if key in self.fields:
                        setattr(self, key, value)

    def save_config(self, config_name=None):
        if config_name:
            config_path = "data/configs/" + config_name
        else:
            config_path = self.config_file

        data_to_save = {}
        for key, field in self.fields.items():
            if field.to_save:
                data_to_save[key] = getattr(self, key)

        path = pathlib.Path(config_path)
        json_string = json.dumps(data_to_save, ensure_ascii=False, indent=4)
        path.write_text(json_string, encoding="UTF-8")

    def __getattr__(self, item):
        if item in self.fields:
            return self.fields[item].value

        raise AttributeError(f"'YorixConfig' object has no attribute '{item}'")

    def __setattr__(self, key, value):
        if key in ["fields", "config_file"]:
            super().__setattr__(key, value)
        elif key in self.fields:
            self.fields[key].value = value
        else:
            super().__setattr__(key, value)


class Config(YorixConfig):
    ENV = YorixField("ENV", default="dev", cast=str.lower)
    if ENV in ["dev", "test"]:
        BOT_TOKEN = YorixField("YORIX_TEST_BOT_TOKEN", default="YOUR TEST TOKEN")
        ENABLE_LOGGING = True
        DEBUG = True
        DEFAULT_USER_IS_ACTIVE = True
    else:
        BOT_TOKEN = YorixField("YORIX_BOT_TOKEN", default="YOUR BOT TOKEN")
        ENABLE_LOGGING = YorixField(
            "YORIX_ENABLE_LOGGING",
            default=False,
            cast=bool,
            to_save=True,
        )
        DEBUG = YorixField("YORIX_DEBUG", default=False, cast=bool, to_save=True)
        DEFAULT_USER_IS_ACTIVE = YorixField(
            "YORIX_DEFAULT_USER_IS_ACTIVE",
            default=False,
            cast=bool,
            to_save=True,
        )

    SECRET_KEY = YorixField("YORIX_SECRET_KEY", default="YOUR SECRET KEY")
    ALLOWED_HOSTS = YorixField("YORIX_ALLOWED_HOSTS", default="*", cast=decouple.Csv())
    EMAIL = YorixField("YORIX_EMAIL", default="YOUR EMAIL")
    EMAIL_PASSWORD = YorixField(
        "YORIX_EMAIL_PASSWORD",
        default="YOUR EMAIL APP PASSWORD",
    )
    DB_NAME = YorixField("POSTGRES_DB", default="postgres")
    DB_USER = YorixField("POSTGRES_USER", default="postgres")
    DB_PASSWORD = YorixField("POSTGRES_PASSWORD", default=None)
    DB_HOST = YorixField("POSTGRES_HOST", default="postgres")
    DB_PORT = YorixField("POSTGRES_PORT", default="5432", cast=postgres_port_cast)
    OWNER_ID = YorixField("YORIX_OWNER_ID", default="YOUR TELEGRAM ID")
    REDIS_HOST = YorixField("REDIS_HOST", default="redis", to_save=True)
    REDIS_PORT = YorixField("REDIS_PORT", default="6379", to_save=True)
    REDIS_DB = YorixField("REDIS_DB", default="1", to_save=True)
    CELERY_BROKER_PORT = YorixField("CELERY_BROKER_PORT", default="0", to_save=True)
    CAPTCHA_LENGTH = YorixField(
        "YORIX_CAPTCHA_LENGTH",
        default=6,
        cast=int,
        to_save=True,
    )
    CAPTCHA_FONT_SIZES = YorixField(
        "YORIX_CAPTCHA_FONT_SIZES",
        default="30, 40, 50",
        cast=lst_cast,
        to_save=True,
    )
    CAPTCHA_WIDTH = YorixField(
        "YORIX_CAPTCHA_WIDTH",
        default=300,
        cast=int,
        to_save=True,
    )
    CAPTCHA_HEIGHT = YorixField(
        "YORIX_CAPTCHA_HEIGHT",
        default=120,
        cast=int,
        to_save=True,
    )
    OWM_API_KEY = YorixField("YORIX_OWM_API_KEY", default="YOUR OWM API KEY")
    TELEGRAM_API_HASH = YorixField(
        "YORIX_TELEGRAM_API_HASH",
        default="YOUR TELEGRAM API HASH",
    )
    TELEGRAM_API_ID = YorixField(
        "YORIX_TELEGRAM_API_ID",
        default="YOUR TELEGRAM API ID",
    )


config = Config()
