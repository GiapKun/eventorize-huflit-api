from core.controllers import BaseControllers
from core.schemas import CommonsDependencies
from core.services import BaseServices
from fastapi import UploadFile
from partners.v1.cloudflare.r2 import r2_services
from utils import converter
from partners.v1.resend.services import user_mail_services

from . import schemas
from .config import settings
from .exceptions import ErrorCode as UsersErrorCode
from .services import user_services


class UserControllers(BaseControllers):
    def __init__(self, controller_name: str, service: BaseServices = None) -> None:
        super().__init__(controller_name, service)

    async def register(self, data: schemas.RegisterRequest) -> dict:
        # Convert the Pydantic model 'data' to a dictionary
        data = data.model_dump()
        results = await self.service.register(data=data)
        # Send mail welcome
        await user_mail_services.send_welcome_email(recipient=data["email"], fullname=data["fullname"])
        return results

    async def login(self, data: schemas.LoginRequest) -> dict:
        # Convert the Pydantic model 'data' to a dictionary
        data = data.model_dump()
        return await self.service.login(data=data)

    async def get_me(self, commons: CommonsDependencies, fields: str = None):
        current_user_id = self.get_current_user(commons=commons)
        return await self.get_by_id(_id=current_user_id, fields_limit=fields, commons=commons)

    async def edit(self, _id: str, data: schemas.EditRequest, commons: CommonsDependencies) -> dict:
        # Check if that user id exists or not
        await self.get_by_id(_id=_id, commons=commons)
        data = data.model_dump(exclude_none=True)
        return await self.service.edit(_id=_id, data=data, commons=commons)

    async def get_user_fullname_by_id(self, _id: str, commons: CommonsDependencies = None) -> str:
        fields_limit = ["fullname"]
        user_data = await self.get_by_id(_id=_id, fields_limit=fields_limit, commons=commons)
        return user_data.get("fullname") if user_data else None

    async def edit_avatar(self, _id: str, file: UploadFile = None, image_url: str = None, commons: CommonsDependencies = None) -> dict:
        await self.get_by_id(_id=_id, commons=commons)
        if file is None and image_url is None:
            raise UsersErrorCode.ImageOrFileRequired()
        if file and image_url:
            raise UsersErrorCode.OnlyOneInputAllowed()
        if file and file.size > settings.maximum_avatar_file_size:
            raise UsersErrorCode.FileTooLarge()

        data_update = {}
        if image_url:
            data_update["avatar"] = image_url
            return await self.service.edit(_id=_id, data=data_update, commons=commons)

        fullname = await self.get_user_fullname_by_id(_id=_id, commons=commons)
        fullname = converter.convert_str_to_slug(fullname)
        timestamp = self.service.get_current_timestamp()
        filename = f"{fullname}_{timestamp}.jpg"
        file_content = await file.read()
        await file.close()
        data_update["avatar"] = await r2_services.upload_file(filename=filename, file_content=file_content)
        return await self.service.edit(_id=_id, data=data_update, commons=commons)

    async def single_sign_on_with_google(self, data: schemas.GoogleSSORequest) -> dict:
        data = data.model_dump()
        return await self.service.single_sign_on_with_google(data=data)

user_controllers = UserControllers(controller_name="users", service=user_services)
