def format_price(price):
    if price % 1 == 0:
        return '${}'.format(int(price))
    return '${}'.format(Decimal(price).quantize(Decimal('1.00')))


def format_age(age):
    if age % 1 == 0:
        if age == 1:
            return 'One year'
        else:
            return '{} years'.format(int(age))
    elif age < 1:
        return '{} months'.format(round(age * 12))
    elif age < 2:
        return 'One year {} months'.format(round(age % 1 * 12))
    return '{} years {} months'.format(int(age), round(age % 1 * 12))


def format_proof(proof):
    if proof % 1 == 0:
        return str(int(proof))
    return proof
