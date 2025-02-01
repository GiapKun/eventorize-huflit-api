from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def EventAlreadyEnded(title_event):
        return CustomException(
            type="event/info/event-already-ended", status=400, title="Event has already ended", detail=f"Event '{title_event}' has already ended, so you cannot create an agenda for it."
        )
