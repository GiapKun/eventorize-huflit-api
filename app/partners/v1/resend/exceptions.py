from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def SizeLimit(size):
        return CustomException(type="resend/info/size-limit", status=400, title="Size limit.", detail=f"This attachment is {size: .2f}MB in size and exceeds the 5MB limit.")

    @staticmethod
    def TemplateNotFound(template_name):
        return CustomException(type="resend/info/template-not-found", status=400, title="Template Not Found", detail=f"This {template_name} template was not found.")
