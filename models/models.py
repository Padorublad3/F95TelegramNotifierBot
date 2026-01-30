from sqlalchemy import Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date as py_date

class Base(DeclarativeBase):
    pass

class Entry(Base):
    __tablename__="entries"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    guid: Mapped[str] = mapped_column(unique = True,nullable = False)
    author: Mapped[str] = mapped_column(nullable = False)
    title: Mapped[str] = mapped_column(nullable = False)
    date: Mapped[py_date] = mapped_column(Date, nullable = True)
