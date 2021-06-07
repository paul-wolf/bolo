import logging
from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    event,
)


logger = logging.getLogger(__name__)

metadata = MetaData()

user_prefs = Table(
    "user_prefs",
    metadata,
    Column("pref_id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id"), nullable=False),
    Column("pref_name", String(40), nullable=False),
    Column("pref_value", String(100)),
)
