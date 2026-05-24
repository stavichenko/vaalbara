from auth.providers.base import OAuthProvider, OAuthUserInfo
from config import settings


class GoogleOAuthProvider:
    name = "google"
    _token_url = "https://oauth2.googleapis.com/token"
    _userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"

    def get_token_url(self) -> str:
        return self._token_url

    def get_userinfo_url(self) -> str:
        return self._userinfo_url

    def build_token_payload(self, code: str, redirect_uri: str) -> dict:
        return {
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
            "code": code,
        }

    def parse_userinfo(self, data: dict) -> OAuthUserInfo:
        return OAuthUserInfo(
            provider_user_id=data["sub"],
            email=data["email"],
            first_name=data.get("given_name"),
            last_name=data.get("family_name"),
            image=data.get("picture"),
        )
