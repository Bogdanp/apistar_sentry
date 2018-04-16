import pytest

from apistar_sentry import SentryComponent
from unittest.mock import patch


@patch("raven.Client.captureException")
def test_mixin_captures_exceptions(capture_mock, client):
    # Given that I have an endpoint
    # And I've mocked Sentry.capture_exception
    # When I call that an endpoint that raises an exception
    # Then the request should fail
    with pytest.raises(RuntimeError):
        client.get("/")

    # And capture_exception should get called
    capture_mock.assert_called_once()


def test_component_resolves_to_none_if_not_given_a_dsn():
    # Given that I don't have a Sentry dsn
    # When I attempt to resolve the component
    # Then I should get back None
    assert SentryComponent(None).resolve() is None
