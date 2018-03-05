import apistar_sentry as sentry

from apistar import Component, Route, hooks, http
from apistar.frameworks.wsgi import WSGIApp as BaseApp
from apistar_sentry import SentryMixin, Sentry


class App(BaseApp, SentryMixin):
    pass


def root_handler():
    return {}


COMPONENTS = [
    Component(Sentry, init=Sentry.setup, preload=True),
]

ROUTES = [
    Route("/", "GET", root_handler),
]

SETTINGS = {
    "VERSION": "0.1.0",
    "SENTRY_DSN": "https://fake:user@example.com/test",
    "ENVIRONMENT": "test",
    "BEFORE_REQUEST": [
        sentry.before_request,
        hooks.check_permissions,
    ],
    "AFTER_REQUEST": [
        hooks.render_response,
        sentry.after_request,
    ],
}


def create_app():
    return App(
        components=COMPONENTS,
        settings=SETTINGS,
        routes=ROUTES,
    )
