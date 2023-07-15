import itertools
from math import perm
def sum_greater_or_equal(bidict, variables, k):

    subsets = itertools.combinations(variables, len(variables)-k+1)
    clauses = perm(len(variables), len(variables)-k+1)
    constrainsts = ''
    for subet in subsets:
        for var in subet:
            constrainsts += f'{bidict[var]} '

        constrainsts += '0\n'
    return constrainsts, clauses


def sum_less_or_equal(bidict, variables, k):
    
    subsets = itertools.combinations(variables, k+1)
    clauses = perm(len(variables), k+1)
    constrainsts = ''
    for subet in subsets:
        for var in subet:
            constrainsts += f'-{bidict[var]} '

        constrainsts += '0\n'

    return constrainsts, clauses