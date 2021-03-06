# apistar-sentry

[Sentry] support for [API Star].


## Installation

    pipenv install apistar_sentry


## Usage

``` python
from apistar import App as BaseApp
from apistar_sentry import SentryComponent, SentryMixin


class App(SentryMixin, BaseApp):
    pass


COMPONENTS = [
    SentryComponent("YOUR_DSN_GOES_HERE", environment="example", version="0.1.0"),
]

ROUTES = [
    # ...
]

app = App(components=COMPONENTS, routes=ROUTES)
```

### Tracking user information

If you have a custom user or account object that can be dependency
injected, then you can define `on_request` and `on_response` hooks to
enrich the `Sentry` object with that user's information:

``` python
class SentryHooks:
  def on_request(self, account: Account, sentry: Sentry = None) -> None:
    if sentry is not None:
      sentry.track_user(account.to_dict())

  def on_response(self, response: http.Response, sentry: Sentry = None) -> http.Response:
    if sentry is not None:
      sentry.clear_user()
    return response

  on_error = on_response
```


## Authors

`apistar_sentry` was originally authored at [Leadpages][leadpages].
Check out their [careers] page!


## License

apistar_sentry is licensed under the MIT License.  Please see
[LICENSE] for licensing details.


[Sentry]: https://getsentry.com
[API Star]: https://github.com/encode/apistar/
[leadpages]: https://leadpages.net
[careers]: https://www.leadpages.net/careers
[LICENSE]: https://github.com/Bogdanp/apistar_sentry/blob/master/LICENSE
