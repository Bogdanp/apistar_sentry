import inspect

from apistar import Component
from raven import Client
from typing import Optional

__version__ = "0.3.1"


class Sentry:
    """A simple wrapper around the Raven library for Sentry.

    Parameters:
      sentry_dsn: The sentry connection string.
      \**sentry_options: Arbitrary options that are passed to the
        raven client.
    """

    def __init__(self, sentry_dsn: str, **sentry_options) -> None:
        self.client = Client(sentry_dsn, **sentry_options)

    def track_user(self, user: dict) -> None:
        """Keep track of the current user.
        """
        self.client.context.activate()
        self.client.context.merge({"user": user})

    def clear_user(self) -> None:
        """Clear the current user from the request context.
        """
        self.client.context.clear()

    def capture_exception(self) -> None:
        """Send exception information to Sentry.
        """
        self.client.captureException()


class SentryComponent(Component):
    """A component that injects instances of the Sentry wrapper.

    Parameters:
      sentry_dsn: The sentry connection string.  If this is None
        (useful for local development), then a client is not
        instantiated.
      \**sentry_options: Arbitrary options that are passed to the
        raven client.
    """

    def __init__(self, sentry_dsn: Optional[str] = None, **sentry_options) -> None:
        if sentry_dsn is not None:
            self.sentry = Sentry(sentry_dsn, **sentry_options)
        else:
            self.sentry = None

    def can_handle_parameter(self, parameter: inspect.Parameter) -> bool:
        return parameter.annotation is Sentry

    def resolve(self) -> Sentry:
        return self.sentry


class SentryMixin:
    """Mix this into an API Star application to automatically send
    exceptions to Sentry.
    """

    def exception_handler(self, exc: Exception, sentry: Sentry = None) -> None:
        try:
            return super().exception_handler(exc)
        except Exception:
            if sentry is not None:
                try:
                    sentry.capture_exception()
                finally:
                    sentry.clear_user()

            raise
