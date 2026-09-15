"""User-facing copy.

Unlike the rest of this package these are plain strings, not message objects:
they are printed to the user by Python before reading input, and are never sent
to the model.
"""

ASK_DAILY_GOALS = """First Enter your daily targets.
Enter protein, carbohydrates and fats in grams, and total calories in kcal."""

ASK_INGREDIENTS = """Now enter the ingredients you have available.
Enter them separated by commas."""
