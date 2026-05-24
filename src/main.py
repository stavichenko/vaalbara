from litestar import Litestar
from litestar.di import Provide
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Components, OAuthFlow, OAuthFlows, SecurityScheme

from auth.dependencies import provide_current_user
from auth.handlers import auth_router
from db import provide_db
from exceptions import AppError, app_exception_handler
from users.handlers import users_router

app = Litestar(
    route_handlers=[auth_router, users_router],
    dependencies={
        "db": Provide(provide_db),
        "current_user": Provide(provide_current_user),
    },
    exception_handlers={AppError: app_exception_handler},
    openapi_config=OpenAPIConfig(
        title="Vaalbara API",
        version="0.1.0",
        components=Components(
            security_schemes={
                "GoogleOAuth2": SecurityScheme(
                    type="oauth2",
                    flows=OAuthFlows(
                        authorization_code=OAuthFlow(
                            authorization_url="https://accounts.google.com/o/oauth2/v2/auth",
                            token_url="/auth/google",
                            scopes={
                                "openid": "OpenID Connect",
                                "email": "Email address",
                                "profile": "Profile information",
                            },
                        )
                    ),
                )
            }
        ),
        security=[{"GoogleOAuth2": ["openid", "email", "profile"]}],
    ),
)
