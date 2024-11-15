from pydantic import BaseModel
from typing import Optional, List

class Message(BaseModel):
    en: str
    zh: Optional[str] = None
    id: Optional[str] = None

class Result(BaseModel):
    job_id: Optional[str] = None
    output_image_url: Optional[List[str]] = None
    credits_states: Optional[int] = None
    need_credits: Optional[int] = None
    credits: Optional[int] = None
    freeze_credits: Optional[int] = None

class ResponseData(BaseModel):
    code: int
    result: Optional[Result]
    message: Message
