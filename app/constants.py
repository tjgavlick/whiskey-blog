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
