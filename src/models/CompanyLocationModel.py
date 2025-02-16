from datetime import datetime
from BaseModel import EntityMeta
from sqlalchemy import (
    Column,
    Integer,
    Table,
    ForeignKey,
    DateTime,
)

company_location = Table(
    "company_location",
    EntityMeta.metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "company_id", Integer, ForeignKey("companies.id")
    ),
    Column(
        "location_id", Integer, ForeignKey("locations.id")
    ),
    Column(DateTime, default=datetime.now()),
    Column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now(),
    ),
)
