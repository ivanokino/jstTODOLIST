from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime
from datetime import datetime, timezone



class Base(DeclarativeBase):
    pass

class TaskModel(Base):
    __tablename__="Tasks"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]
    text: Mapped[str]
    status: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc).replace(
            microsecond=0
        ),
        nullable=False
    )
    deadline: Mapped[str]

