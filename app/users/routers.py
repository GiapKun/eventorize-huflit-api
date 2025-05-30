from auth.decorator import access_control
from core.schemas import CommonsDependencies, ObjectIdStr, PaginationParams, UrlStr
from fastapi import Depends, File, UploadFile
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from . import schemas
from .controllers import user_controllers

router = InferringRouter(
    prefix="/v1",
    tags=["v1/users"],
)


@cbv(router)
class RoutersCBV:
    """
    A class-based view for handling user-related routes in the FastAPI application.

    This class uses FastAPI's class-based view (`cbv`) approach to define various endpoints for user management,
    including retrieving user information, registering, logging in, updating, and deleting users.

    Attributes:
        commons (CommonsDependencies): Common dependencies for the request, such as the current user and user type.
    """

    commons: CommonsDependencies = Depends(CommonsDependencies)  # type: ignore

    @router.post("/users/register", status_code=201, responses={201: {"model": schemas.LoginResponse, "description": "Register user success"}})
    async def register(self, data: schemas.RegisterRequest):
        result = await user_controllers.register(data=data)
        return schemas.LoginResponse(**result)

    @router.post("/users/login", status_code=201, responses={201: {"model": schemas.LoginResponse, "description": "Login user success"}})
    async def login(self, data: schemas.LoginRequest):
        result = await user_controllers.login(data=data)
        return schemas.LoginResponse(**result)

    @router.get("/users/me", status_code=200, responses={200: {"model": schemas.Response, "description": "Get users success"}})
    async def get_me(self, fields: str = None):
        results = await user_controllers.get_me(commons=self.commons, fields=fields)
        return schemas.Response(**results)

    @router.get("/users/export", status_code=200)
    async def export_users(self):
        return await user_controllers.export_users(commons=self.commons)

    @router.get("/users", status_code=200, responses={200: {"model": schemas.ListResponse, "description": "Get users success"}})
    @access_control(admin=True)
    async def get_all(self, pagination: PaginationParams = Depends()):
        search_in = ["fullname", "email"]
        results = await user_controllers.get_all(
            query=pagination.query,
            search=pagination.search,
            search_in=search_in,
            page=pagination.page,
            limit=pagination.limit,
            fields_limit=pagination.fields,
            sort_by=pagination.sort_by,
            order_by=pagination.order_by,
            commons=self.commons,
        )
        if pagination.fields:
            return results
        return schemas.ListResponse(**results)

    @router.get("/users/{_id}", status_code=200, responses={200: {"model": schemas.Response, "description": "Get users success"}})
    async def get_detail(self, _id: ObjectIdStr, fields: str = None):
        results = await user_controllers.get_by_id(_id=_id, fields_limit=fields, commons=self.commons)
        if fields:
            return results
        return schemas.Response(**results)

    @router.put("/users/{_id}", status_code=200, responses={200: {"model": schemas.Response, "description": "Update user success"}})
    async def edit(self, _id: ObjectIdStr, data: schemas.EditRequest):
        results = await user_controllers.edit(_id=_id, data=data, commons=self.commons)
        return schemas.Response(**results)

    @router.delete("/users/{_id}", status_code=204)
    @access_control(admin=True)
    async def delete(self, _id: ObjectIdStr):
        await user_controllers.soft_delete_by_id(_id=_id, commons=self.commons)

    @router.put("/users/me/avatar", status_code=200, responses={200: {"model": schemas.Response, "description": "Update user's avatar success"}})
    async def edit_avatar(self, file: UploadFile = File(None), image_url: UrlStr = None):
        current_user = user_controllers.get_current_user(commons=self.commons)
        results = await user_controllers.edit_avatar(_id=current_user, file=file, image_url=image_url, commons=self.commons)
        return schemas.Response(**results)
