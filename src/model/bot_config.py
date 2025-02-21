from typing import List, Optional

from pydantic import BaseModel


class Response(BaseModel):
    type: str
    content: Optional[str] = None
    file_id: Optional[str] = None
    caption: Optional[str] = None


class MenuItem(BaseModel):
    title: str
    responses: List[Response]


class BotConfig(BaseModel):
    welcome_message: str
    welcome_message_buttons: str
    handbook_file_id: str
    default_reply: str
    menu: List[MenuItem]

    @classmethod
    def from_json(cls, json_str: str):
        return cls.model_validate_json(json_str)
