from langchain_core.messages import HumanMessage

from domain.user import DailyGoals, IngredientsInput


def suggest_meal(goals: DailyGoals, user: IngredientsInput) -> HumanMessage:
    """Build the meal-suggestion prompt from the user's collected goals and ingredients.

    Taking the validated models as arguments is the point: the prompt cannot be
    built from unchecked input. The goals are serialised with ``model_dump_json``
    so a field added to :class:`DailyGoals` reaches the prompt without an edit here.
    """
    ingredients = "\n".join(f"- {item}" for item in user.ingredients)
    return HumanMessage(
        content=f"""Here are my daily targets:

{goals.model_dump_json(indent=2)}

Here is everything I have available:

{ingredients}

Plan my meals for the day using only these ingredients. For each meal give the
portions in grams, and finish with a total showing how close the day lands to my
targets."""
    )
