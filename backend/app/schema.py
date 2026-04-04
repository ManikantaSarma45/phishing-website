from pydantic import BaseModel, HttpUrl

class URLInput(BaseModel):
    url: str   # keep string for flexibility (can switch to HttpUrl later)