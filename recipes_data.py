"""
Guided recipe content for PantryChef's Cook section.

Each recipe is fully self-contained data — no external API. Steps include a
`wait_sec` used to power an on-screen timer ("how long to wait"), and an `image`
slot (a filename under static/images/<id>/) that shows a real photo when you add
one, or a clean placeholder until then.

To add a recipe: copy one block, fill it in, and add matching images to
static/images/<id>/ . That's it — it appears on the site automatically.
"""

CATEGORY_ORDER = ["Tiffins", "Meals", "Biryani", "Desserts"]

DIET_LABELS = {"veg": "🟢 Veg", "vegan": "🌱 Vegan", "nonveg": "🔴 Non-veg"}
SPICE_LABELS = {"mild": "Mild", "medium": "Medium", "hot": "Hot 🌶️"}
SPICE_RANK = {"mild": 1, "medium": 2, "hot": 3}


RECIPES = [
    # ---------------- TIFFINS ----------------
    {
        "id": "masala-dosa",
        "name": "Masala Dosa",
        "category": "Tiffins",
        "diet": "vegan",
        "spice": "medium",
        "time": "30 min",
        "serves": 3,
        "ingredients": ["dosa batter", "potato", "onion", "mustard seeds",
                        "turmeric", "curry leaves", "green chilli", "oil", "salt"],
        "steps": [
            {"text": "Boil 3 potatoes until soft, peel and roughly mash. Set aside.",
             "wait_sec": 900, "image": "step1.jpg"},
            {"text": "Heat 2 tbsp oil, add 1 tsp mustard seeds and let them splutter.",
             "wait_sec": 60, "image": "step2.jpg"},
            {"text": "Add 1 sliced onion, green chillies and curry leaves. Fry until onion is soft.",
             "wait_sec": 180, "image": "step3.jpg"},
            {"text": "Add turmeric and salt, then the mashed potato. Mix and cook 2 min. This is your filling.",
             "wait_sec": 120, "image": "step4.jpg"},
            {"text": "Heat a flat tawa. Pour a ladle of batter and spread thin in a spiral. Drizzle oil at the edges.",
             "wait_sec": 30, "image": "step5.jpg"},
            {"text": "Cook until the dosa turns golden and crisp and lifts off easily (don't flip).",
             "wait_sec": 120, "image": "step6.jpg"},
            {"text": "Place a scoop of filling in the center, fold, and serve hot with chutney and sambar.",
             "wait_sec": 0, "image": "step7.jpg"},
        ],
        "spice_tip": "Hotter: add 2 extra green chillies to the filling. Milder: leave chillies out and use a pinch of black pepper.",
    },
    {
        "id": "rava-upma",
        "name": "Rava Upma",
        "category": "Tiffins",
        "diet": "veg",
        "spice": "mild",
        "time": "20 min",
        "serves": 2,
        "ingredients": ["rava", "onion", "mustard seeds", "urad dal", "green chilli",
                        "ginger", "curry leaves", "ghee", "water", "salt"],
        "steps": [
            {"text": "Dry-roast 1 cup rava (semolina) on low heat until it smells nutty. Tip out and set aside.",
             "wait_sec": 240, "image": "step1.jpg"},
            {"text": "In the same pan heat 2 tbsp ghee, add mustard seeds and urad dal; let them crackle.",
             "wait_sec": 60, "image": "step2.jpg"},
            {"text": "Add chopped onion, green chilli, ginger and curry leaves. Saute until onion turns soft.",
             "wait_sec": 180, "image": "step3.jpg"},
            {"text": "Pour in 2½ cups water with salt and bring to a rolling boil.",
             "wait_sec": 180, "image": "step4.jpg"},
            {"text": "Lower the heat and add the roasted rava slowly while stirring, so no lumps form.",
             "wait_sec": 60, "image": "step5.jpg"},
            {"text": "Cover and cook 2-3 min until the water is absorbed and fluffy. Serve hot.",
             "wait_sec": 180, "image": "step6.jpg"},
        ],
        "spice_tip": "Hotter: add an extra slit green chilli. Milder: reduce to none — the ginger still gives warmth.",
    },
    # ---------------- MEALS ----------------
    {
        "id": "sambar",
        "name": "Sambar (with rice)",
        "category": "Meals",
        "diet": "vegan",
        "spice": "medium",
        "time": "40 min",
        "serves": 4,
        "ingredients": ["toor dal", "tomato", "onion", "drumstick", "tamarind",
                        "sambar powder", "mustard seeds", "curry leaves", "turmeric", "oil", "salt"],
        "steps": [
            {"text": "Pressure-cook 1 cup toor dal with turmeric and water until very soft. Mash and keep aside.",
             "wait_sec": 900, "image": "step1.jpg"},
            {"text": "Soak a lemon-sized ball of tamarind in warm water, then squeeze out the pulp.",
             "wait_sec": 300, "image": "step2.jpg"},
            {"text": "In a pot, boil chopped onion, tomato and vegetables with the tamarind water until soft.",
             "wait_sec": 420, "image": "step3.jpg"},
            {"text": "Add 2 tbsp sambar powder and salt; simmer 5 min so the flavours open up.",
             "wait_sec": 300, "image": "step4.jpg"},
            {"text": "Stir in the mashed dal with a little water to loosen; simmer another 5 min.",
             "wait_sec": 300, "image": "step5.jpg"},
            {"text": "Temper: heat oil, splutter mustard seeds and curry leaves, and pour over. Serve over hot rice.",
             "wait_sec": 60, "image": "step6.jpg"},
        ],
        "spice_tip": "Hotter: add ½ tsp red chilli powder with the sambar powder. Milder: use a mild sambar powder and extra tomato.",
    },
    {
        "id": "curd-rice",
        "name": "Curd Rice",
        "category": "Meals",
        "diet": "veg",
        "spice": "mild",
        "time": "15 min",
        "serves": 2,
        "ingredients": ["rice", "curd", "milk", "mustard seeds", "urad dal",
                        "green chilli", "ginger", "curry leaves", "oil", "salt"],
        "steps": [
            {"text": "Cook 1 cup rice until soft (slightly overcooked is perfect here). Cool a little and mash lightly.",
             "wait_sec": 600, "image": "step1.jpg"},
            {"text": "Mix in 1 cup curd and a splash of milk with salt until creamy.",
             "wait_sec": 60, "image": "step2.jpg"},
            {"text": "Temper: heat oil, add mustard seeds, urad dal, green chilli, ginger and curry leaves; let it crackle.",
             "wait_sec": 90, "image": "step3.jpg"},
            {"text": "Pour the tempering over the curd rice and mix. Best served chilled.",
             "wait_sec": 0, "image": "step4.jpg"},
        ],
        "spice_tip": "Hotter: add a pinch of finely chopped green chilli into the rice itself. Milder: skip the chilli entirely.",
    },
    # ---------------- BIRYANI ----------------
    {
        "id": "veg-dum-biryani",
        "name": "Veg Dum Biryani",
        "category": "Biryani",
        "diet": "veg",
        "spice": "medium",
        "time": "60 min",
        "serves": 4,
        "ingredients": ["basmati rice", "mixed vegetables", "onion", "curd", "ginger garlic paste",
                        "biryani masala", "mint", "coriander", "ghee", "oil", "salt"],
        "steps": [
            {"text": "Soak 2 cups basmati rice for 20 min, then parboil with whole spices until 70% cooked. Drain.",
             "wait_sec": 1200, "image": "step1.jpg"},
            {"text": "Deep-fry 2 sliced onions until golden brown (birista). Set half aside for layering.",
             "wait_sec": 420, "image": "step2.jpg"},
            {"text": "Cook ginger-garlic paste, vegetables, curd, biryani masala and salt into a thick masala.",
             "wait_sec": 480, "image": "step3.jpg"},
            {"text": "Layer the parboiled rice over the masala. Top with fried onions, mint, coriander and a drizzle of ghee.",
             "wait_sec": 120, "image": "step4.jpg"},
            {"text": "Cover tightly (dum). Cook on the lowest heat so it steams without burning.",
             "wait_sec": 1200, "image": "step5.jpg"},
            {"text": "Rest 5 min, then gently fluff from the sides. Serve with raita.",
             "wait_sec": 300, "image": "step6.jpg"},
        ],
        "spice_tip": "Hotter: add 2 slit green chillies and extra biryani masala. Milder: halve the masala and add a little more curd.",
    },
    {
        "id": "chicken-biryani",
        "name": "Chicken Biryani",
        "category": "Biryani",
        "diet": "nonveg",
        "spice": "hot",
        "time": "70 min",
        "serves": 4,
        "ingredients": ["basmati rice", "chicken", "onion", "curd", "ginger garlic paste",
                        "biryani masala", "red chilli powder", "mint", "coriander", "ghee", "oil", "salt"],
        "steps": [
            {"text": "Marinate 700g chicken in curd, ginger-garlic paste, biryani masala, chilli powder and salt for 30 min.",
             "wait_sec": 1800, "image": "step1.jpg"},
            {"text": "Soak 2 cups basmati rice 20 min, then parboil with whole spices until 70% done. Drain.",
             "wait_sec": 1200, "image": "step2.jpg"},
            {"text": "Fry 2 sliced onions golden; keep half aside. Add marinated chicken and cook until nearly done.",
             "wait_sec": 600, "image": "step3.jpg"},
            {"text": "Layer parboiled rice over the chicken. Top with fried onions, mint, coriander and ghee.",
             "wait_sec": 120, "image": "step4.jpg"},
            {"text": "Seal the lid and cook on dum (lowest heat) so the flavours steam through the rice.",
             "wait_sec": 1500, "image": "step5.jpg"},
            {"text": "Rest 10 min, fluff gently, and serve hot with onion raita.",
             "wait_sec": 600, "image": "step6.jpg"},
        ],
        "spice_tip": "Hotter: increase red chilli powder to 1½ tbsp and add green chillies. Milder: drop to 1 tsp and add extra curd.",
    },
    # ---------------- DESSERTS ----------------
    {
        "id": "semiya-payasam",
        "name": "Semiya Payasam",
        "category": "Desserts",
        "diet": "veg",
        "spice": "mild",
        "time": "25 min",
        "serves": 4,
        "ingredients": ["vermicelli", "milk", "sugar", "ghee", "cashews", "raisins", "cardamom"],
        "steps": [
            {"text": "Heat 2 tbsp ghee and fry cashews and raisins until golden. Scoop out and set aside.",
             "wait_sec": 120, "image": "step1.jpg"},
            {"text": "In the same ghee, roast 1 cup vermicelli until light golden.",
             "wait_sec": 180, "image": "step2.jpg"},
            {"text": "Pour in 4 cups milk and simmer, stirring, until the vermicelli turns soft.",
             "wait_sec": 480, "image": "step3.jpg"},
            {"text": "Add ½ cup sugar and crushed cardamom; simmer 3-4 min until slightly thick.",
             "wait_sec": 240, "image": "step4.jpg"},
            {"text": "Top with the fried cashews and raisins. Serve warm or chilled.",
             "wait_sec": 0, "image": "step5.jpg"},
        ],
        "spice_tip": "Not a spicy dish — adjust sweetness instead: less sugar for lighter, more for richer.",
    },
    {
        "id": "rava-kesari",
        "name": "Rava Kesari",
        "category": "Desserts",
        "diet": "veg",
        "spice": "mild",
        "time": "20 min",
        "serves": 4,
        "ingredients": ["rava", "sugar", "ghee", "water", "cashews", "raisins", "cardamom", "saffron"],
        "steps": [
            {"text": "Fry cashews and raisins in a little ghee until golden; set aside.",
             "wait_sec": 120, "image": "step1.jpg"},
            {"text": "Roast 1 cup rava in 3 tbsp ghee on low heat until aromatic (don't brown it).",
             "wait_sec": 240, "image": "step2.jpg"},
            {"text": "Carefully add 2½ cups hot water with a pinch of saffron; it will bubble. Stir to avoid lumps.",
             "wait_sec": 120, "image": "step3.jpg"},
            {"text": "Cook until the rava absorbs the water and thickens.",
             "wait_sec": 180, "image": "step4.jpg"},
            {"text": "Add 1 cup sugar and cardamom; stir until it melts and pulls from the sides. Fold in the nuts.",
             "wait_sec": 180, "image": "step5.jpg"},
        ],
        "spice_tip": "Not spicy — for extra richness stir in an extra spoon of ghee at the end.",
    },
]


def by_id(recipe_id):
    return next((r for r in RECIPES if r["id"] == recipe_id), None)


def filtered(category=None, diet=None, spice=None):
    out = RECIPES
    if category:
        out = [r for r in out if r["category"] == category]
    if diet:
        out = [r for r in out if r["diet"] == diet]
    if spice:
        out = [r for r in out if r["spice"] == spice]
    return out


def grouped_by_category(recipes):
    return {c: [r for r in recipes if r["category"] == c] for c in CATEGORY_ORDER}
