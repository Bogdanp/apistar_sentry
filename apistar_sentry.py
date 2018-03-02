import abc

from apistar import Settings
from apistar.types import ReturnValue
from raven import Client
from typing import Any, Callable, Dict, Tuple

__version__ = "0.1.1"


class Sentry(abc.ABC):  # pragma: no cover
    """Base class for sentry components.
    """

    @classmethod
    def setup(cls, settings: Settings):
        raise NotImplementedError

    @classmethod
    def setup_celery(cls, settings: Settings):
        raise NotImplementedError

    def track(self, user: Any):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def capture_exception(self):
        raise NotImplementedError


class SentryMixin(abc.ABC):  # pragma: no cover
    """Base class for sentry app mixins.
    """

    def exception_handler(self, exc: Exception, sentry: Sentry) -> Any:
        raise NotImplementedError


SentryComponentRes = Tuple[
    SentryMixin,
    Sentry,
    Callable[[Any, Sentry], None],
    Callable[[Sentry, ReturnValue], ReturnValue],
]


def make_sentry_component(
        user_class: type,
        user_encoder: Callable[[Any], Dict]
) -> SentryComponentRes:
    """Generate a Sentry component for an API Star app.

    Parameters:
      user_class: The type that represents users in your app.
      user_encoder: A function that turns a User into a dict.

    Returns:
      A tuple representing the component class, the mixin, and before
      and after request functions.
    """

    class SentryImpl(Sentry):
        def __init__(self, settings: Settings):
            self.client = Client(
                settings["SENTRY_DSN"],
                environment=settings["ENVIRONMENT"],
                release=settings["VERSION"],
            )

        @classmethod
        def setup(cls, settings: Settings):
            if settings.get("SENTRY_DSN"):
                return cls(settings)

            return None

        @classmethod
        def setup_celery(cls, settings: Settings):
            from raven.contrib import celery as raven_celery
            sentry = cls(settings)
            raven_celery.register_logger_signal(sentry.client)
            raven_celery.register_signal(sentry.client)

        def track(self, user: user_class):
            self.client.context.activate()

            if user is not None:
                self.client.context.merge({"user": user_encoder(user)})

        def clear(self):
            self.client.context.clear()

        def capture_exception(self):
            self.client.captureException()

    class SentryMixinImpl(SentryMixin):
        def exception_handler(self, exc: Exception, sentry: SentryImpl):
            try:
                return super().exception_handler(exc)
            except Exception:
                if sentry is not None:
                    try:
                        sentry.capture_exception()
                    finally:
                        sentry.clear()

                raise

    def before_request(user: user_class, sentry: SentryImpl):
        if sentry is not None:
            sentry.track(user)

    def after_request(sentry: SentryImpl, ret: ReturnValue):
        if sentry is not None:
            sentry.clear()
        return ret

    return SentryMixinImpl, SentryImpl, before_request, after_request
