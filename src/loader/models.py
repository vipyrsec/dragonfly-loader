from pydantic import BaseModel

class Job(BaseModel):
    name: str
    version: str
    distributions: list[str]
