from pydantic import BaseModel
from user import DailyGoals

class Recipe(BaseModel):
    name: str
    ingredients: list[str]
    instructions: str
    servings: int
    prep_time: int  # in minutes
    cook_time: int  # in minutes
    total_time: int  # in minutes
    nutrition: DailyGoals