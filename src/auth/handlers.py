import httpx
from litestar import Request, Router, post
from litestar.exceptions import NotFoundException, ValidationException
from sqlalchemy.ext.asyncio import AsyncSession

from auth.jwt import create_token
from auth.providers import PROVIDERS
from users.repository import UserRepository


@post("/{provider:str}")
async def oauth_login(provider: str, request: Request, db: AsyncSession) -> dict:
    if provider not in PROVIDERS:
        raise NotFoundException(detail=f"Unknown provider: {provider}")

    # Accept both JSON (frontend) and form-encoded (Swagger UI OAuth2 flow per RFC 6749)
    content_type = request.content_type[0] if request.content_type else ""
    if "application/json" in content_type:
        body = await request.json()
    else:
        body = dict(await request.form())

    code = body.get("code")
    redirect_uri = body.get("redirect_uri")
    if not code or not redirect_uri:
        raise ValidationException(detail="Missing code or redirect_uri")

    p = PROVIDERS[provider]

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(p.get_token_url(), data=p.build_token_payload(code, redirect_uri))
        if token_resp.is_error:
            raise ValidationException(detail="Failed to exchange code")

        userinfo_resp = await client.get(
            p.get_userinfo_url(),
            headers={"Authorization": f"Bearer {token_resp.json()['access_token']}"},
        )
        if userinfo_resp.is_error:
            raise ValidationException(detail="Failed to fetch user info")

    info = p.parse_userinfo(userinfo_resp.json())
    repo = UserRepository(db)

    user = await repo.get_by_oauth(provider, info.provider_user_id)
    if user is None:
        user = await repo.create_with_oauth(
            email=info.email,
            first_name=info.first_name,
            last_name=info.last_name,
            image=info.image,
            provider=provider,
            provider_user_id=info.provider_user_id,
        )

    await db.commit()
    # Return standard OAuth2 token response format (required for Swagger UI to pick up the token)
    return {"access_token": create_token(user.id), "token_type": "bearer"}


auth_router = Router(path="/auth", route_handlers=[oauth_login])
