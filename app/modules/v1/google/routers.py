from core.schemas import CommonsDependencies
from fastapi import Depends, Request
from fastapi.responses import RedirectResponse
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter
from users import schemas as user_schemas

from .controllers import google_controllers

router = InferringRouter(
    prefix="/v1",
    tags=["v1/google"],
)


@cbv(router)
class RoutersCBV:
    commons: CommonsDependencies = Depends(CommonsDependencies)  # type: ignore

    @router.post("/google/login", status_code=200, responses={200: {"description": "Generate Google login URL"}})
    async def google_login(self):
        """
        Generate and return Google's login page URL.
        """
        return await google_controllers.google_login()

    @router.get("/google/callback", status_code=200, responses={200: {"model": user_schemas.LoginResponse, "description": "Handle Google SSO callback"}})
    async def callback(self, request: Request):
        """
        Handle the callback from Google after login and process user information.
        """
        result = await google_controllers.google_callback(request)

        frontend_url = "https://eventorize.kiet.site"  # URL frontend
        redirect_url = f"{frontend_url}/auth-callback?access_token={result['access_token']}&token_type={result['token_type']}"
        return RedirectResponse(url=redirect_url)
