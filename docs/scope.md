## Problem: 
    It's a hassle to cook meal plans daily, let alone make it healthy and decide a menu based on the ingredients i have , i end up ordering food because of the confusion and amount of effort.
    If i had an agent which takes the grocery items and decide things for me while keeping track of my macros and micro intake , it would make my life much simpler.
## User:
    Me & Friends.

## Commands:
1. ``nutroo pantry add "2 eggs and toast"``: Saves on entry in Ingredients table.
2. ``nutroo recipes`` : calls llm with saved pantry items , to suggest some recipies.
3. ``nutroo cook "recipe name"`` : saves one entry of recipe from the suggested recipes in Recipes table.
3. ``nutroo log "2 eggs and toast"``: saves one entry per food item with grams, kcal, protein, carbs, fat in the daily intake table.
4. ``nutroo today``: sends nutritional intake for today , categorised by recipies logged for the day.
5. ``nutroo checkin``: sends remaining intake for today based on logged food intake.


## Acceptance Criteria:
    Returns up to 3 recipes. Every ingredient exists in the pantry in enough quantity. Each recipe shows kcal and macros per serving, sourced from USDA.


## Data Models:
    1. Ingredients:
        id: uuid (PK)
        user_id: uudi (FK)
        items: list[str]
    2. UserProfile:
        id: uuid (PK)
        name: str
        age: int
        email: str
        password: str
    3. UserGoals:
        user_id: uuid(FK)
        id: uuid(PK)
        Calories: int
        protein: float
        carbs: float
        fat: float
    4. Recipes:
        ingredients_id: uuid (FK)
        id: uuid(PK)
        Name: str
        Cooking_time: float
        Instructions: str
        daily_intake_id: uuid(FK)
        confidence_score: float
    5. DailyIntake:
        user_id: uuid(FK)
        id: uuid(PK)
        Calories: int
        protein: float
        carbs: float
        fat: float
        created_at: datetime

## Out of Scope(v1):
    1. Line/iMessage Integration
    2. UI elements
    3. Image as Input
    4. Scheduled Check-ins
    5. Micro-Nutrients

## Success Metrics:
    1. Average Calories Error Under 20%.
    2. Recipies Using only provided items list 100% of the time.
    3. Calories Estimate should be right 60% of the time.

## Risks:
    1. UnSure Units: Consistent Unit of truth is grams , if user adds 1 bowl/1 cup of rice , agent should not guess, instead ask a user to clarify the weight.
    2. UnSure Nutrional Estimates:  App Should Check USDA FOODATA CENTRAL for nutrional value estimate first, and only then recommend recipies,any recipie without Clear Nutritional Value should not be sent to user.
    3. Extra health/cooking Advice: Any extra advice should not be sent to user , need to be handled by the middleware as a output guardrails , and blocked.
    4. No Handling of Dietry preferences or dislikes: Assuming the User will responsibly buy grocieries according to their restrictions or dislikes. Instead we can just add a small section at the end of suggested recipe to be mindful of their dietry restrictions.
    5. items - list[str]: Need to add a small text , to let the user know to input their quantities with items like ``1 chicken breast , 2 bowl rice, a bowl of chopped onions``.
