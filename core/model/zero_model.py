from sqlmodel import SQLModel, Column, Field
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.types import TIMESTAMP
import sqlalchemy.dialects.postgresql as pg
import uuid




class ZeroModel(SQLModel):
    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True
    )

    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"server_default": func.now()}
    )

    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": func.now()
        }
    )