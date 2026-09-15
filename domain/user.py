from pydantic import BaseModel, Field


class DailyGoals(BaseModel):
    """A user's daily macronutrient and calorie targets."""

    Protein: float = Field(ge=0, description="Daily protein target in grams.")
    Carbohydrates: float = Field(ge=0, description="Daily carbohydrate target in grams.")
    Fats: float = Field(ge=0, description="Daily fat target in grams.")
    Calories: int = Field(default=1500, ge=0, description="Daily calorie target in kcal.")


class IngredientsInput(BaseModel):
    """The ingredients a user currently has available."""

    ingredients: list[str] = Field(
        min_length=1,
        description="Ingredient names the user has on hand, without quantities.",
    )
