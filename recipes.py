"""
A small, self-contained recipe database + matching engine.

No external API needed — recipes live here as plain data. The matcher compares
each recipe's ingredients against what's currently in the pantry and reports what
you can cook now, and what you're only 1-2 ingredients away from.

Ingredient matching is intentionally forgiving: a pantry item matches a recipe
ingredient if either name contains the other (so "cherry tomatoes" matches "tomato").
"""

RECIPES = [
    {
        "name": "Tomato & Garlic Pasta",
        "time": "20 min",
        "ingredients": ["pasta", "tomato", "garlic", "olive oil", "onion"],
        "steps": "Cook pasta. Saute onion + garlic in oil, add chopped tomato, simmer 10 min, toss with pasta.",
    },
    {
        "name": "Veg Fried Rice",
        "time": "15 min",
        "ingredients": ["rice", "onion", "carrot", "peas", "soy sauce", "egg"],
        "steps": "Fry onion + veg, push aside and scramble egg, add cooked rice + soy sauce, toss on high heat.",
    },
    {
        "name": "Cheese Omelette",
        "time": "10 min",
        "ingredients": ["egg", "cheese", "butter", "salt"],
        "steps": "Beat eggs with salt. Cook in butter, add cheese, fold when just set.",
    },
    {
        "name": "Banana Oat Pancakes",
        "time": "15 min",
        "ingredients": ["banana", "oats", "egg", "milk"],
        "steps": "Blend everything to a batter, cook spoonfuls on a greased pan until golden both sides.",
    },
    {
        "name": "Chickpea Curry",
        "time": "25 min",
        "ingredients": ["chickpeas", "onion", "tomato", "garlic", "ginger", "spices"],
        "steps": "Saute onion, garlic, ginger + spices. Add tomato, then chickpeas + water, simmer 15 min.",
    },
    {
        "name": "Grilled Cheese Sandwich",
        "time": "8 min",
        "ingredients": ["bread", "cheese", "butter"],
        "steps": "Butter bread outsides, cheese in the middle, grill on a pan until golden and melty.",
    },
    {
        "name": "Chicken Stir Fry",
        "time": "20 min",
        "ingredients": ["chicken", "onion", "capsicum", "garlic", "soy sauce"],
        "steps": "Sear sliced chicken, add veg + garlic, splash soy sauce, stir-fry on high heat until cooked.",
    },
    {
        "name": "Fruit & Yogurt Bowl",
        "time": "5 min",
        "ingredients": ["yogurt", "banana", "honey", "oats"],
        "steps": "Layer yogurt with sliced fruit, oats and a drizzle of honey.",
    },
    {
        "name": "Tomato Soup",
        "time": "20 min",
        "ingredients": ["tomato", "onion", "garlic", "butter", "salt"],
        "steps": "Cook tomato, onion, garlic in butter, blend smooth, season and simmer.",
    },
    {
        "name": "Dal (Lentil Stew)",
        "time": "30 min",
        "ingredients": ["lentils", "onion", "tomato", "garlic", "spices"],
        "steps": "Boil lentils soft. Temper onion, garlic, tomato + spices and stir in.",
    },
    {
        "name": "Veg Sandwich",
        "time": "10 min",
        "ingredients": ["bread", "tomato", "cucumber", "onion", "butter"],
        "steps": "Butter bread, layer sliced veg, season, and press together.",
    },
    {
        "name": "Scrambled Eggs on Toast",
        "time": "10 min",
        "ingredients": ["egg", "bread", "butter", "milk", "salt"],
        "steps": "Whisk eggs with a splash of milk + salt, soft-scramble in butter, serve on toast.",
    },
]


def _matches(pantry_name: str, ingredient: str) -> bool:
    a, b = pantry_name.strip().lower(), ingredient.strip().lower()
    return a in b or b in a


def suggest(pantry_names):
    """
    Given a list of pantry item names, return two lists:
      can_make  -> recipes where every ingredient is present
      almost    -> recipes missing only 1-2 ingredients (with the missing list)
    Both sorted so the most-complete recipes come first.
    """
    pantry_names = [p for p in pantry_names if p]
    can_make, almost = [], []

    for recipe in RECIPES:
        missing = []
        for ing in recipe["ingredients"]:
            if not any(_matches(p, ing) for p in pantry_names):
                missing.append(ing)

        if not missing:
            can_make.append(recipe)
        elif len(missing) <= 2:
            almost.append({**recipe, "missing": missing})

    almost.sort(key=lambda r: len(r["missing"]))
    return can_make, almost
