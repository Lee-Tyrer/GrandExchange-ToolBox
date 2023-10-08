# Grand Exchange tax constants
TAX_PERCENTAGE = 0.01
TAX_THRESHOLD = 5_000_000
TAX_LOWER_ITEM_PRICE = 100

# Valid timesteps for time series data
VALID_TIMESTEPS = {
    "5m": 5, "1h": 60, "6h": 3600,
}

SAWMILL_COSTS = {
    "Logs": 100,
    "Oak logs": 250,
    "Teak logs": 500,
    "Mahogany logs": 1500,
}

PLANK_MAKE_COSTS = {
    "Logs": 70,
    "Oak logs": 175,
    "Teak logs": 350,
    "Mahogany logs": 1050,
}

REPAIR_BARROWS_COSTS = {
    "helm": 60_000,
    "body": 90_000,
    "legs": 80_000,
    "weapon": 100_000,
}

BARROWS = {
    "Dharoks":
        {"weapon": "Dharok's greataxe",
         "helm": "Dharok's helm",
         "body": "Dharok's platebody",
         "legs": "Dharok's platelegs",
         "set": "Dharok's armour set"},
    "Guthans":
        {"weapon": "Guthan's warspear",
         "helm": "Guthan's helm",
         "body": "Guthan's platebody",
         "legs": "Guthan's chainskirt",
         "set": "Guthan's armour set"},
    "Ahrims": {
        "weapon": "Ahrim's staff",
        "helm": "Ahrim's hood",
        "body": "Ahrim's robetop",
        "legs": "Ahrim's robeskirt",
        "set": "Ahrim's armour set"},
    "Karils":
        {"weapon": "Karil's greataxe",
         "helm": "Karil's coif",
         "body": "Karil's leathertop",
         "legs": "Karil's leatherskirt",
         "set": "Karil's armour set"},
    "Torags":
        {"weapon": "Torag's hammers",
         "helm": "Torag's helm",
         "body": "Torag's platebody",
         "legs": "Torag's platelegs",
         "set": "Torag's armour set"},
    "Veracs":
        {"weapon": "Veracs's flail",
         "helm": "Veracs's helm",
         "body": "Veracs's brassard",
         "legs": "Veracs's plateskirt",
         "set": "Veracs's armour set"}
}
