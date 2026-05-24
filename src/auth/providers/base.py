from dataclasses import dataclass
from typing import Protocol


@dataclass
class OAuthUserInfo:
    provider_user_id: str
    email: str
    first_name: str | None
    last_name: str | None
    image: str | None


class OAuthProvider(Protocol):
    name: str

    def get_token_url(self) -> str: ...
    def get_userinfo_url(self) -> str: ...
    def build_token_payload(self, code: str, redirect_uri: str) -> dict: ...
    def parse_userinfo(self, data: dict) -> OAuthUserInfo: ...
