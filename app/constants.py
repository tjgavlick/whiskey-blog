DRINK_TYPES = {
    'american-malt': {
        'name': 'American single-malt',
        'filter_name': 'American single-malts'
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

AGE_RANGES = {
    'unknown': {
        'name': 'Unknown / no age statement',
        'filter_name': 'of unknown age',
        'age_min': -1,
        'age_max': 0
    },
    'young': {
        'name': 'Under 2 years',
        'filter_name': 'under 2 years of age',
        'age_min': 0,
        'age_max': 2
    },
    'youngish': {
        'name': '2 – 4 years',
        'filter_name': '2–4 years of age',
        'age_min': 2,
        'age_max': 5
    },
    'mid': {
        'name': '5 – 10 years',
        'filter_name': '5–10 years of age',
        'age_min': 5,
        'age_max': 10
    },
    'old': {
        'name': '10 – 15 years',
        'filter_name': '10–15 years of age',
        'age_min': 10,
        'age_max': 15
    },
    'ancient': {
        'name': 'Over 15 years',
        'filter_name': 'over 15 years of age',
        'age_min': 15,
        'age_max': 200
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
        'name': 'Best',
        'filter_name': 'my favorites'
    },
    'worst': {
        'name': 'Worst',
        'filter_name': 'my least favorite'
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
