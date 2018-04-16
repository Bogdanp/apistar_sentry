import pytest

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
