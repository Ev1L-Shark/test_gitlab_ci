from pydantic import BaseModel


class RecipeSchema(BaseModel):
    name: str
    cooking_time: int
    description: str
    ingredients: list[str]


class RecipeResponse(RecipeSchema):
    id: int
    views: int

    class Config:
        orm_mode = True


class RecipeListResponse(BaseModel):
    id: int
    name: str
    cooking_time: int
    views: int
