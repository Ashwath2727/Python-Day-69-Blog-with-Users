from flask_login import UserMixin
from sqlalchemy import Integer, Text, String
from sqlalchemy.orm import Mapped, mapped_column

from extensions import db

class User(UserMixin, db.Model):
    __tablename__ = "users_2"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)


    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.password}')"
    