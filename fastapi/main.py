from typing import Annotated

import uvicorn
from database import Base, engine, get_db
from models import RecipeModel
from schemas import RecipeListResponse, RecipeResponse, RecipeSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import Depends, FastAPI, HTTPException

app = FastAPI(title="CookBook API", version="1")
SessionDep = Annotated[AsyncSession, Depends(get_db)]


@app.post("/setup_database")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True}


@app.post("/recipes", response_model=RecipeResponse)
async def add_recipes(recipe: RecipeSchema, session: SessionDep):
    new_recipe = RecipeModel(**recipe.dict())
    session.add(new_recipe)
    await session.commit()
    await session.refresh(new_recipe)
    return new_recipe


@app.get("/recipes", response_model=list[RecipeListResponse])
async def get_recipes(session: SessionDep):
    result = await session.execute(
        select(RecipeModel).order_by(
            RecipeModel.views.desc(), RecipeModel.cooking_time.asc()
        )
    )
    return result.scalars().all()


@app.get("/recipes/{recipe_id}", response_model=RecipeResponse)
async def get_recipe_detail(recipe_id: int, session: SessionDep):
    result = await session.execute(
        select(RecipeModel).where(RecipeModel.id == recipe_id)
    )
    recipe = result.scalar()

    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

    recipe.views += 1
    await session.commit()
    await session.refresh(recipe)

    return recipe


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
