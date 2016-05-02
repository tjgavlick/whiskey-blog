ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

DRINK_TYPES = {
    'american': {
        'name': 'American whiskey',
        'filter_name': 'American whiskies'
    },
    'bourbon': {
        'name': 'Bourbon',
        'filter_name': 'bourbons'
    },
    'rye': {
        'name': 'Rye',
        'filter_name': 'ryes'
    },
    'scotchblend': {
        'name': 'Scotch (blended)',
        'filter_name': 'blended Scotches'
    },
    'scotchsingle': {
        'name': 'Scotch (single-malt)',
        'filter_name': 'single-malt Scotches'
    },
    'world': {
        'name': 'World',
        'filter_name': 'world whiskies'
    }
}

RARITIES = {
    'common': {
        'name': 'Common',
        'filter_name': 'easy-to-find',
        'value': 10
    },
    'uncommon': {
        'name': 'Uncommon',
        'filter_name': 'uncommon',
        'value': 20
    },
    'rare': {
        'name': 'Rare',
        'filter_name': 'hard-to-find',
        'value': 30
    },
    'nope': {
        'name': 'Not happening',
        'filter_name': 'unobtanium',
        'value': 40
    }
}

PROOF_RANGES = {
    'bare-minimum': {
        'name': '80',
        'filter_name': 'minimum proof',
        'proof_min': 0,
        'proof_max': 80
    },
    'low': {
        'name': '81 – 90',
        'filter_name': '81–90 proof',
        'proof_min': 80.1,
        'proof_max': 91
    },
    'med': {
        'name': '91 – 100',
        'filter_name': '91–100 proof',
        'proof_min': 91,
        'proof_max': 101
    },
    'high': {
        'name': 'Over 100',
        'filter_name': 'over 100 proof',
        'proof_min': 101,
        'proof_max': 200
    }
}

PRICE_RANGES = {
    'inexpensive': {
        'name': 'Under $25',
        'filter_name': 'under $25',
        'price_min': 0,
        'price_max': 25
    },
    'affordable': {
        'name': '$25 – $40',
        'filter_name': '$25–40',
        'price_min': 25,
        'price_max': 40
    },
    'moderate': {
        'name': '$41 – $75',
        'filter_name': '$41–75',
        'price_min': 40,
        'price_max': 75
    },
    'high': {
        'name': '$76 – $150',
        'filter_name': '$76–150',
        'price_min': 75,
        'price_max': 150
    },
    'ouch': {
        'name': 'Over $150',
        'filter_name': 'over $150',
        'price_min': 150,
        'price_max': 10000
    }
}

REVIEW_SORTS = {
    'best': {
        'name': 'Favorite',
        'filter_name': 'what I liked the most'
    },
    'worst': {
        'name': 'Least Favorite',
        'filter_name': 'what I least enjoyed'
    }
}

NO_REVIEWS_MESSAGES = [
    "Obviously, I need to drink more.",
    "Sorry about that.",
    "Hold tight; I'm always trying new things!",
    "Try removing one or two and see if that helps.",
    "One man can only drink so quickly!",
    "I'm drinking new things all the time, so try again later.",
    "I have failed you and brought dishonor to my family."
]
