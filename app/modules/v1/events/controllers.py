from core.controllers import BaseControllers
from core.schemas import CommonsDependencies
from core.services import BaseServices
from modules.v1.organizers.controllers import organizer_controllers
from utils import converter

from . import schemas
from .exceptions import ErrorCode as EventErrorCode
from .services import event_services


class EventControllers(BaseControllers):
    def __init__(self, controller_name: str, service: BaseServices = None) -> None:
        super().__init__(controller_name, service)

    async def is_active(self, _id, ignore_error=False, commons: CommonsDependencies = None):
        # get event and check if event is still active
        event = await event_controllers.get_by_id(_id=_id, commons=commons)
        current_time = self.service.get_current_datetime()

        if converter.convert_str_to_datetime(event["end_date"]) < current_time:
            if not ignore_error:
                raise EventErrorCode.EventAlreadyEnded(event["title"])
            return False
        return event

    async def create(self, data: schemas.CreateRequest, commons: CommonsDependencies) -> dict:
        data = data.model_dump()
        await organizer_controllers.get_by_id(_id=data["organizer_id"], commons=commons)
        return await self.service.create(data=data, commons=commons)

    async def edit(self, _id: str, data: schemas.EditRequest, commons: CommonsDependencies) -> dict:
        await self.get_by_id(_id=_id, commons=commons)
        data = data.model_dump(exclude_none=True)
        return await self.service.edit(_id=_id, data=data, commons=commons)


event_controllers = EventControllers(controller_name="events", service=event_services)
