from core.controllers import BaseControllers
from core.services import BaseServices
from fastapi import Request
from partners.v1.google.services import google_sso_services
from users.controllers import user_controllers

from .services import google_services


class GoogleControllers(BaseControllers):
    def __init__(self, controller_name: str, service: BaseServices = None) -> None:
        super().__init__(controller_name, service)

    async def google_login(self) -> dict:
        """
        Generate and return the Google login redirect URL.
        """
        redirect_url = await google_sso_services.get_login_redirect()
        return {"redirect_url": redirect_url}

    async def google_callback(self, request: Request) -> dict:
        """
        Handle the Google SSO callback, process user information, and create a token.
        """
        # Process the callback and get user information
        user = await google_sso_services.verify_and_process(request)
        return await user_controllers.single_sign_on_with_google(data=user)


google_controllers = GoogleControllers(controller_name="google", service=google_services)
