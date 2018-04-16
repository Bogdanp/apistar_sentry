from apistar import App as BaseApp, Route
from apistar_sentry import SentryComponent, SentryMixin


class App(SentryMixin, BaseApp):
    pass


def index():
    raise RuntimeError("example")


COMPONENTS = [
    SentryComponent("https://fake:user@example.com/test"),
]

ROUTES = [
    Route("/", "GET", index),
]


def create_app():
    return App(components=COMPONENTS, routes=ROUTES)
