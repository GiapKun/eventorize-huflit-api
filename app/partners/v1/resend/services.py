from typing import List, Union

import resend
from core.schemas import EmailStr
from jinja2 import Template

from .config import settings
from .exceptions import ErrorCode as ResendErrorCode


class BaseResend:
    def __init__(self, resend_api_key: str, resend_domain: str, resend_sender_name: str, resend_sender: str, max_size_file) -> None:
        self.api_key = resend_api_key
        self.sender_name = resend_sender_name
        self.sender = resend_sender
        self.domain = resend_domain
        self.sender_email = f"{self.sender}@{self.domain}"
        resend.api_key = self.api_key
        self.max_size_file = max_size_file

    async def check_file_size(self, file_size):
        if file_size > self.max_size_file:
            raise ResendErrorCode.SizeLimit(size=file_size)

    async def get_template_sample(self, template_name: str) -> str:
        template_path = f"../app/assets/email/{template_name}"
        try:
            with open(template_path, "r", encoding="UTF-8") as file:
                return file.read()
        except FileNotFoundError:
            raise ResendErrorCode.TemplateNotFound(template_name=template_name)

    async def render(self, data: dict, template_name: str) -> str:
        html_template = await self.get_template_sample(template_name)
        jinja2_template = Template(html_template)
        return jinja2_template.render(**data)

    async def send_mail(self, recipients: Union[EmailStr, List[EmailStr]], subject: str, content: str):
        params: resend.Emails.SendParams = {"from": f"{self.sender_name} <{self.sender_email}>", "to": recipients, "subject": subject, "html": content}
        return resend.Emails.send(params)


class ResendService(BaseResend):
    def __init__(self, resend_api_key, resend_domain, resend_sender_name, resend_sender, max_size_file):
        super().__init__(resend_api_key, resend_domain, resend_sender_name, resend_sender, max_size_file)

    async def send_welcome_email(self, recipient: str, fullname: str) -> dict:
        data = {"fullname": fullname}
        html_content = await self.render(data=data, template_name="welcome_new_user.html")
        return await self.send_mail(recipients=recipient, subject="Welcome to Eventorize", content=html_content)

    # async def send_verification_email(self, recipient: str, code: str) -> str:
    #     template_path = os.path.join(os.path.dirname(__file__), "template_test.html")
    #     with open(template_path, "r", encoding="utf-8") as file:
    #         html_content = file.read().replace("{{CODE}}", code)

    #     params: resend.Emails.SendParams = {
    #         "from": f"{self.sender_name} <{self.sender_email}>",
    #         "to": recipient,
    #         "subject": "Verify your email address with Eventorize",
    #         "html": html_content,
    #     }

    #     return resend.Emails.send(params)

    # async def send_email_with_remote_attachment(self, recipient: str | List[str], subject: str, attachment_url: str, filename: str) -> str:
    #     file_size = int(requests.head(attachment_url).headers.get("content-length", 0))
    #     self.check_file_size(file_size=file_size / (1024 * 1024))

    #     attachment = {"path": attachment_url, "filename": filename}
    #     params = {"from": f"{self.sender_name} <{self.sender_email}>", "to": recipient, "subject": subject, "html": "<p>Attachment email</p>", "attachments": attachment}

    #     _id_email = resend.Emails.send(params)
    #     return _id_email

    # async def send_email_with_local_attachment(self, recipient: str | List[str], subject: str, filepath: str, filename: str) -> str:
    #     file_size = os.path.getsize(filepath)
    #     self.check_file_size(file_size=file_size / (1024 * 1024))
    #     with open(filepath, "rb") as file:
    #         content = list(file.read())

    #     attachment = {"content": content, "filename": filename}
    #     params = {"from": f"{self.sender_name} <{self.sender_email}>", "to": recipient, "subject": subject, "html": "<p>Attachment email</p>", "attachments": attachment}

    #     _id_email = resend.Emails.send(params)
    #     return _id_email


resend_services = ResendService(
    resend_api_key=settings.resend_api_key,
    resend_domain=settings.resend_domain,
    resend_sender_name=settings.resend_sender_name,
    resend_sender=settings.resend_sender,
    max_size_file=settings.max_size_file,
)
