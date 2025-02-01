from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def InvalidPasswordLength():
        return CustomException(type="users/info/invalid-password-length", status=400, title="Invalid password length.", detail="The password must be at least 8 characters long.")

    @staticmethod
    def FileTooLarge():
        return CustomException(type="users/info/file-too-large", status=413, title="File too large.", detail="The uploaded file exceeds the maximum size of 5MB.")

    @staticmethod
    def ImageOrFileRequired():
        return CustomException(type="users/info/image-or-file-required", status=400, title="Image or File Required", detail="Either 'image_url' or 'file' must be provided.")

    @staticmethod
    def OnlyOneInputAllowed():
        return CustomException(type="users/info/only-one-input-allowed", status=400, title="Only One Input Allowed", detail="Provide only one of 'image_url' or 'file'.")
    
    @staticmethod
    def SSOIdMismatch():
        return CustomException(type="users/sso/invalid-sso", status=400, title="Invalid SSO Information", detail="The provided SSO credentials are invalid. Please try again.")
