from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str
    password: str
    email: str
    phone: str = Field(max_length=11)