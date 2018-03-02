from apistar import Component, Route, hooks
from apistar.frameworks.wsgi import WSGIApp as BaseApp
from apistar_sentry import SentryMixin, make_sentry_component


class User:
    def __init__(self, username):
        self.username = username

    @classmethod
    def setup(cls):
        return User("fake-user")

    @staticmethod
    def to_dict(user):
        return {"username": user.username}


SentryMixin, Sentry, sentry_before_request, sentry_after_request = make_sentry_component(User, User.to_dict)


class App(BaseApp, SentryMixin):
    pass


def root_handler(user: User):
    return User.to_dict(user)


COMPONENTS = [
    Component(Sentry, init=Sentry.setup, preload=True),
    Component(User, init=User.setup),
]

ROUTES = [
    Route("/", "GET", root_handler),
]

SETTINGS = {
    "VERSION": "0.1.0",
    "SENTRY_DSN": "https://fake:user@example.com/test",
    "ENVIRONMENT": "test",
    "BEFORE_REQUEST": [
        sentry_before_request,
    ],
    "AFTER_REQUEST": [
        hooks.render_response,
        sentry_after_request,
    ],
}


def create_app():
    return App(
        components=COMPONENTS,
        settings=SETTINGS,
        routes=ROUTES,
    )
