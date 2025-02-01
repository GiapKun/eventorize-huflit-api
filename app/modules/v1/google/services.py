from core.services import BaseServices
from db.base import BaseCRUD
from db.engine import app_engine


class GoogleServices(BaseServices):
    def __init__(self, service_name: str, crud: BaseCRUD = None) -> None:
        super().__init__(service_name, crud)


google_crud = BaseCRUD(database_engine=app_engine, collection="google")
google_services = GoogleServices(service_name="google", crud=google_crud)
