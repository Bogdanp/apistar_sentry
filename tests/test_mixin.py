from apistar import App as BaseApp, Route, TestClient, http
from apistar_sentry import SentryMixin


class App(SentryMixin, BaseApp):
    pass


class SomeHook:
    def on_response(self, response: http.Response) -> None:
        response.headers["x-example"] = "example"


def index():
    return {}


app = App(
    routes=[Route("/", "GET", index)],
    event_hooks=[SomeHook()],
)


def test_mixin_doesnt_interfere_with_response_injection():
    # Given that I have a test client
    client = TestClient(app)

    # When I request the index handler
    response = client.get("/")

    # Then I expect SomeHook to populate the headers
    assert response.headers["x-example"] == "example"
