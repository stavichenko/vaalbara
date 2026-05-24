from auth.providers.base import OAuthProvider
from auth.providers.google import GoogleOAuthProvider

PROVIDERS: dict[str, OAuthProvider] = {
    "google": GoogleOAuthProvider(),
    # "facebook": FacebookOAuthProvider(),
    # "instagram": InstagramOAuthProvider(),
}
