from discord_webhook import AsyncDiscordWebhook

from .config import settings


class BaseBot:
    def __init__(self, webhook_url, environment) -> None:
        self.webhook_url = webhook_url
        self.environment = environment

    async def send_message(self, message):
        if self.environment not in ["production", "staging"]:
            return
        """Send a message to the specified Discord webhook."""
        bot = AsyncDiscordWebhook(url=self.webhook_url)
        bot.set_content(content=message)

        try:
            await bot.execute()
        except Exception as e:
            return


class ErrorBot(BaseBot):
    def __init__(self, webhook_url, environment) -> None:
        super().__init__(webhook_url, environment)

    async def send_error(self, exc_list, request, response, request_id, issue_link):
        name_error = file_error = line_number_error = function_error = line_error = None
        if exc_list:
            name_error = exc_list[-1].replace("\r\n", "")
            name_error = name_error[:100]
            error_detail = exc_list[-2]
            error_list = error_detail.split()
            file_error = error_list[error_list.index("File") + 1][:-1]
            line_number_error = error_list[error_list.index("line") + 1][:-1]
            function_error = error_list[error_list.index("in") + 1]
            line_error = error_detail.splitlines()[-1].strip()

        message = (
            f"**❌ THÔNG BÁO LỖI**\n\n"
            f"**Enviroment**: {self.environment}\n"
            f"**Title**: {name_error}\n"
            f"**File error** <pre language='shell'>{file_error}</pre>\n"
            f"**Line**: {line_number_error}\n"
            f"**Function**: {function_error}\n"
            f"**API**: {request.url.path}\n"
            f"**Method**: {request.method}\n"
            f"**Status code**: {response.status_code}\n"
            f"**Request Id**: {request_id}\n"
            f"**Issue link**: {issue_link}\n"
            f"**Line error** <pre language='python'>{line_error}</pre>"
        )
        await self.send_message(message)

    async def send_warning(self, request, response, response_body, request_id):
        name_error = response_body.get("title")
        detail_error = response_body.get("detail")
        type_error = response_body.get("type")
        message = (
            f"**⚠️ Cảnh báo**\n\n"
            f"**Enviroment**: {self.environment}\n"
            f"**Title**: {name_error}\n"
            f"**Detail**: {detail_error}\n"
            f"**Type**: {type_error}\n"
            f"**API**: {request.url.path}\n"
            f"**Method**: {request.method}\n"
            f"**Status code**: {response.status_code}\n"
            f"**Request Id**: {request_id}\n"
        )
        await self.send_message(message)


error_bot = ErrorBot(webhook_url=settings.error_webhook_url, environment=settings.environment)
