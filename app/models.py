from pydantic import BaseModel


class Service(BaseModel):
    service_name: str
    url: str