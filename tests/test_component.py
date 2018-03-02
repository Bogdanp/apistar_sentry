from unittest.mock import patch

from .app import Sentry


@patch.object(Sentry, "clear")
@patch.object(Sentry, "track")
def test_before_and_after_request_are_called(track_mock, clear_mock, client):
    # Given that I have an endpoint
    # And I've mocked Sentry.{clear, track}
    # When I call that endpoint
    response = client.get("/")

    # Then the request should succeed
    assert response.status_code == 200

    # And each mock should be ccalled once
    track_mock.assert_called_once()
    clear_mock.assert_called_once()
