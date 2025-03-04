from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(nullable=True)
    email: str = Field(unique=True)
    phone: str = Field(max_length=11, nullable=True)