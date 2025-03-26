from pydantic import BaseModel


class SupportData(BaseModel):
    url: str
    text: str


support_data = SupportData(url="https://reqres.in/#support-heading",
                           text="To keep ReqRes free, contributions towards server costs are appreciated!")
