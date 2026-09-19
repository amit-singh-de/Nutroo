import os
from typing import Any,Dict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import ValidationError
from domain.user import DailyGoals, IngredientsInput
from prompts.ask import ASK_DAILY_GOALS, ASK_INGREDIENTS
from prompts.suggest_meal import suggest_meal
from prompts.system_prompt import PERSONA
from tools.websearch import WebSearch
from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langsmith import uuid7
@tool()
def web_search_tool(query: str) -> Dict[str,Any]:
    """Perform a web search using the Tavily client."""
    web_search = WebSearch(api_key=os.getenv("TAVILY_API_KEY"))
    return web_search.search(query)

def build_agent():
    load_dotenv()
    model = ChatOpenAI(
        model="deepseek-flash",
        temperature=0.7,
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASE_URL"),
    )
    return create_agent(model=model, tools=[web_search_tool],checkpointer=InMemorySaver())


GOAL_FIELDS = {
    "Protein": ("protein (g)", float),
    "Carbohydrates": ("carbohydrates (g)", float),
    "Fats": ("fats (g)", float),
    "Calories": ("calories (kcal)", int),
}


def read_number(label: str, cast: type) -> float | int:
    """Read one number, re-asking until it parses."""
    while True:
        try:
            return cast(input(f"  {label}: "))
        except ValueError:
            print(f"  Please enter a number for {label}.")


def collect_goals() -> DailyGoals:
    """Read the daily targets, re-asking only the fields that fail validation."""
    print(ASK_DAILY_GOALS)
    values: dict[str, float | int] = {}
    pending = list(GOAL_FIELDS)
    while True:
        for name in pending:
            label, cast = GOAL_FIELDS[name]
            values[name] = read_number(label, cast)
        try:
            return DailyGoals(**values)
        except ValidationError as error:
            # Keep what passed; re-ask only what Pydantic rejected.
            pending = []
            for detail in error.errors():
                name = detail["loc"][0] if detail["loc"] else None
                print(f"  {name or 'input'}: {detail['msg']}")
                pending = list(GOAL_FIELDS) if name is None else pending + [name]


def collect_ingredients() -> IngredientsInput:
    """Read the ingredient list, re-prompting until it passes validation."""
    print(ASK_INGREDIENTS)
    while True:
        raw = input("  ingredients: ")
        items = [item.strip() for item in raw.split(",") if item.strip()]
        try:
            return IngredientsInput(ingredients=items)
        except ValidationError as error:
            print(f"\nThat didn't work: {error}\nLet's try again.\n")




def main():
    print("Nutroo — your meal prep assistant.\n")
    goals = collect_goals()
    print()
    ingredients = collect_ingredients()

    print("\nThinking...\n")
    agent = build_agent()
    thread_config = {"configurable": {"thread_id": str(uuid7())}}
    print(f"Starting Session with thread_id: {thread_config['configurable']['thread_id']}")
    reply = agent.invoke(
        {"messages": [PERSONA, suggest_meal(goals, ingredients)]},thread_config
    )
    print(reply["messages"][-1].content)



if __name__ == "__main__":
    main()
