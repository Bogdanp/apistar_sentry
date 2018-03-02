# apistar-sentry

[Sentry] support for [API Star].


## Installation

    pipenv install apistar_sentry


## Usage

In `sentry_component.py`:

``` python
from apistar_sentry import make_sentry_component
from user_component import User, user_to_dict

SentryMixin, Sentry, before_request, before_response = make_sentry_component(User, user_to_dict)
```

In `app.py`:

``` python
import sentry_component

from apistar import Component
from apistar.frameworks.wsgi import WSGIApp as BaseApp
from sentry_component import Sentry, SentryMixin


class App(BaseApp, SentryMixin):
    pass


COMPONENTS = [
    Component(Sentry, init=Sentry.setup, preload=True),
    # ...
]

SETTINGS = env.copy()
SETTINGS.update({
    # All of these settings are required:
    "VERSION": "0.1.0",
    "SENTRY_DSN": "...",
    "ENVIRONMENT": "prod",
    "BEFORE_REQUEST": [
        sentry_component.before_request,
        # ...
    ],
    "AFTER_REQUEST": [
        # ...
        sentry_component.after_request,
    ]
})

ROUTES = [
    # ...
]

app = App(
    components=COMPONENTS,
    settings=SETTINGS,
    routes=ROUTES,
)
```

## Authors

`apistar_sentry` was authored at [Leadpages][leadpages].  We welcome
contributions, and [we're always looking][careers] for more
engineering talent!

[Sentry]: https://getsentry.com
[API Star]: https://github.com/encode/apistar/
[leadpages]: https://leadpages.net
[careers]: https://www.leadpages.net/careers
