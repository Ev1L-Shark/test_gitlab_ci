from database import Base
from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column


class RecipeModel(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    cooking_time: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(500))
    views: Mapped[int] = mapped_column(default=0)
    ingredients: Mapped[dict] = mapped_column(JSON, nullable=False)
