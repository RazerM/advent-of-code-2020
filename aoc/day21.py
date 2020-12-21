from collections import Counter

import regex

from .registry import register


def parse(lines):
    foods = []
    for line in lines:
        match = regex.match(
            r'''
                (?P<ingredient>\w+)(?:\s+(?&ingredient))*\s+
                \(contains\s+(?P<allergen>\w+)(?:,\s*(?&allergen))*\)
            ''',
            line,
            flags=regex.VERBOSE,
        )
        ingredients = match.captures('ingredient')
        allergens = match.captures('allergen')
        foods.append((ingredients, allergens))
    return foods


@register(day=21)
def solve(file, verbose):
    foods = parse(file)

    allergen_candidates = dict()
    all_ingredients = set()
    for ingredients, allergens in foods:
        for allergen in allergens:
            try:
                candidates = allergen_candidates[allergen]
            except KeyError:
                allergen_candidates[allergen] = set(ingredients)
            else:
                candidates &= set(ingredients)
            all_ingredients.update(ingredients)

    all_candidates = set.union(*allergen_candidates.values())
    allergen_free = {x for x in all_ingredients if x not in all_candidates}

    ingredient_counter = Counter()
    for ingredients, _ in foods:
        ingredient_counter.update(ingredients)

    print('Part 1:', sum(ingredient_counter[ingredient] for ingredient in allergen_free))

    found = dict()

    while sum(len(c - found.keys()) for c in allergen_candidates.values()):
        for allergen, candidates in allergen_candidates.items():
            try:
                ingredient, = candidates - found.keys()
            except ValueError:
                continue
            else:
                found[ingredient] = allergen

    print('Part 2:', ','.join(sorted(found.keys(), key=lambda ingredient: found[ingredient])))
