import typing

from apistar import Settings
from apistar.interfaces import Auth
from apistar.types import ReturnValue
from raven import Client

__version__ = "0.2.0"


class Sentry:
    def __init__(self, settings: Settings) -> None:
        self.client = Client(
            settings["SENTRY_DSN"],
            environment=settings["ENVIRONMENT"],
            release=settings["VERSION"],
        )

    @classmethod
    def setup(cls, settings: Settings) -> typing.Optional["Sentry"]:
        if settings.get("SENTRY_DSN"):
            return cls(settings)

        return None

    @classmethod
    def setup_celery(cls, settings: Settings) -> None:
        from raven.contrib import celery as raven_celery
        sentry = cls(settings)
        raven_celery.register_logger_signal(sentry.client)
        raven_celery.register_signal(sentry.client)

    def track(self, auth: Auth) -> None:
        self.client.context.activate()

        if auth is not None:
            self.client.context.merge({
                "user": {
                    "id": auth.get_user_id(),
                    "name": auth.get_display_name(),
                    "authenticated": auth.is_authenticated(),
                }
            })

    def clear(self) -> None:
        self.client.context.clear()

    def capture_exception(self) -> None:
        self.client.captureException()


class SentryMixin:
    def exception_handler(self, exc: Exception, sentry: Sentry) -> None:
        try:
            return super().exception_handler(exc)
        except Exception:
            if sentry is not None:
                try:
                    sentry.capture_exception()
                finally:
                    sentry.clear()

            raise


def before_request(auth: Auth, sentry: Sentry) -> None:
    if sentry is not None:
        sentry.track(auth)


def after_request(sentry: Sentry, ret: ReturnValue) -> ReturnValue:
    if sentry is not None:
        sentry.clear()
    return ret
