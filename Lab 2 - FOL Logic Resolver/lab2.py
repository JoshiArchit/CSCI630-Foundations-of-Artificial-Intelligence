"""
Filename : lab2.py
Author : Archit Joshi
Description : CSCI630 Lab 2 - Resolution.
Language : Python 3.11

"""

from sys import argv


def parseInput(path):
    """
    Helper function to parse .cnf input files.

    :param path: path to input file via commandline arguments.
    :return: list of predicates, variables, constants, functions and clauses.
    """

    kb = []
    with open(path) as f:
        predicates = f.readline().split()[1:]
        variables = f.readline().split()[1:]
        constants = f.readline().split()[1:]
        functions = f.readline().split()[1:]
        f.readline()
        for line in f:
            kb.append(line.strip())

    return predicates, variables, constants, functions, kb


def resultClause(ci, cj):
    """
    Formulate a new resultant clause from new knowledge gained.

    :param ci: Clause 1
    :param cj: Clause 2
    :return: new clause for the knowledge base.
    """

    result = []
    delimiter_ci = ''
    delimiter_cj = ''
    temp_ci = ''
    temp_cj = ''

    if ci:
        if len(ci) > 1:
            delimiter_ci = ' '

        temp_ci = ci[0]
        if len(ci) > 1:
            for item in ci[1:]:
                temp_ci += delimiter_ci + item

    if cj:
        if len(cj) > 1:
            delimiter_cj = ' '

        temp_cj = cj[0]
        if len(cj) > 1:
            for item in cj[1:]:
                temp_cj += delimiter_cj + item

    # No new information. Not satisfiable
    if temp_ci == '' and temp_cj == '':
        result.append([])
    # One new clause derived
    elif temp_ci == '' or temp_cj == '':
        result.append(temp_ci + temp_cj)
    # Two clauses combined to get new clause
    else:
        result.append(temp_ci + ' ' + temp_cj)

    return result


def resolutionNoVars(predicates, constants, clauses):
    """
    PL-Resolution function. Pseudocode reference R&N 7.5 pg.228.
    Function to resolve without any variables.

    :param constants: list of constants
    :param predicates: list of predicates
    :param clauses: list of clauses
    :return: True iff no new knowledge gained
    """
    new = []

    # Get all combinations
    while True:
        combos = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j
                  in range(i + 1, len(clauses))]
        for (ci, cj) in combos:
            # Resolve ci & cj
            resolvants = resolveNoVars(predicates, constants, ci, cj)
            if [] in resolvants:
                return True
            for clause in resolvants:
                if clause not in new:
                    new.append(clause)
        if set(new).issubset(clauses):
            return False
        for clause in new:
            if clause not in clauses:
                clauses.append(clause)


def resolveNoVars(predicates, constants, ci, cj):
    """
    Resolve 2 clauses in the knowledge base.

    :param predicates: list of predicates
    :param constants: list of constants
    :param ci: clause 1
    :param cj: clause 2
    :return: resulting/resolved clause
    """
    resolvant = []

    cI = ci.split()
    cJ = cj.split()

    for item1 in cI:
        for item2 in cJ:
            # Check if there are negations which can cancel out
            if item1 == ("!" + item2) or item2 == ("!" + item1):
                temp1 = ci.split(" ")
                temp2 = cj.split(" ")
                temp1.remove(item1)
                temp2.remove(item2)

                # Need to return new clause to update KB
                resolvant = resultClause(temp1, temp2)

    return resolvant


def resolutionWithVars(predicates, variables, constants, functions, clauses):
    """
    PL-Resolution function. Pseudocode reference R&N 7.5 pg.228.
    Function to resolve with variables.

    :param predicates: list of predicates
    :param variables: list of variables
    :param constants: list of constants
    :param functions: list of functions
    :param clauses: list of clauses
    :return: True iff no new knowledge gained
    """
    new = []
    # Get all combinations
    while True:
        combos = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j
                  in range(i + 1, len(clauses))]
        for (ci, cj) in combos:
            # Resolve 2 clauses
            resolvants = resolveWithVars(predicates, variables, functions,
                                         constants, ci, cj)
            if [] in resolvants:
                return True
            for clause in resolvants:
                if clause not in new:
                    new.append(clause)
        if set(new).issubset(clauses):
            return False
        for clause in new:
            if clause not in clauses:
                clauses.append(clause)


def resolveWithVars(predicates, variables, functions, constants, ci, cj):
    """
    Resolve 2 clauses from KB.

    :param predicates: list of predicates
    :param variables: list of variables
    :param functions: list of functions
    :param constants: list of constants
    :param ci: clause 1
    :param cj: clause 2
    :return: resolved clauses
    """
    resolvant = []

    cI = ci.split()
    cJ = cj.split()

    for item1 in cI:
        for item2 in cJ:
            # Unification
            ciUni, cjUni = unification(predicates, variables, functions,
                                       constants, item1, item2)
            if ciUni == ("!" + cjUni) or cjUni == ("!" + ciUni):
                temp1 = ci.split(" ")
                temp2 = cj.split(" ")
                temp1.remove(item1)
                temp2.remove(item2)

                # Need to return new clause to update KB
                resolvant = resultClause(temp1, temp2)

    return resolvant


def unification(predicates, variables, constants, functions, ci, cj):
    """
    Function to unify two clauses iff possible.
    Pseudocode reference R&N Pg.285

    :param predicates: list of predicates
    :param variables: list of variables
    :param constants: list of constants
    :param functions: list of functions
    :param ci: clause 1
    :param cj: clause 2
    :return: unified clauses
    """

    variable_ci = ci[ci.find('(') + 1: ci.find(')')].split(',')
    variable_cj = cj[cj.find('(') + 1: cj.find(')')].split(',')
    predicate_ci = ci[0:ci.find('(')]
    predicate_cj = cj[0:cj.find('(')]

    novarCI = False
    novarCJ = False

    for item1 in variable_ci:
        if item1 not in variables:
            novarCI = True
        else:
            novarCI = False
    for item2 in variable_cj:
        if item2 not in variables:
            novarCJ = True
        else:
            novarCJ = False
    # Substitution not possible
    if novarCI and novarCJ:
        return ci, cj
    # Substitution possible
    elif novarCI is False and novarCJ is True:
        # Both have variables and nouns
        # CJ Noun in CI clause
        nounsForCI = ''
        existingNounsForCI = ''
        for item in ci:
            if item not in variables:
                existingNounsForCI += item + ','
        existingNounsForCI = existingNounsForCI[:len(existingNounsForCI) - 1]
        for item in cj:
            if item not in variables:
                nounsForCI += item + ','
        nounsForCI = nounsForCI[:len(nounsForCI) - 1]
        temp_ci = predicate_ci + '(' + existingNounsForCI + nounsForCI + ')'

        nounsForCJ = ''
        existingNounsForCJ = ''
        for item in cj:
            if item not in variables:
                existingNounsForCJ += item + ','
        existingNounsForCJ = existingNounsForCJ[:len(existingNounsForCJ) - 1]
        for item in ci:
            if item not in variables:
                nounsForCJ += item + ','
        nounsForCJ = nounsForCJ[:len(nounsForCJ) - 1]
        temp_cj = predicate_cj + '(' + existingNounsForCJ + nounsForCJ + ')'

        ci, cj = temp_ci, temp_cj
    elif novarCJ is False and novarCI is True:
        # Variable in CJ can be replaced with Nouns in CI

        output = ''
        for item in variable_ci:
            if item not in variables:
                output += item + ','
        output = output[:len(output) - 1]

        cj = predicate_cj + '(' + output + ')'
    elif novarCI is False and novarCJ is True:
        # Variable in CI can be replaced with Nouns in CJ
        output = ''
        for item in variable_cj:
            if item not in variables:
                output += item + ','
        output = output[:len(output) - 1]

        ci = predicate_ci + '(' + output + ')'

    return ci, cj


def resolutionNoConst(predicates, variables, clauses):
    """
    PL-Resolution function. Pseudocode reference R&N 7.5 pg.228.
    Function to resolve without constants.

    :param predicates: list of predicates
    :param variables: list of variables
    :param clauses: list of clauses
    :return: True iff no new knowledge gained
    """
    new = []
    # Get all combinations
    while True:
        combos = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j
                  in range(i + 1, len(clauses))]
        for (ci, cj) in combos:
            resolvants = resolveNoConst(predicates, variables, ci, cj)
            if [] in resolvants:
                return True
            for clause in resolvants:
                if clause not in new:
                    new.append(clause)
        if set(new).issubset(clauses):
            return False
        for clause in new:
            if clause not in clauses:
                clauses.append(clause)


def resolveNoConst(predicates, variables, ci, cj):
    """
    Resolve 2 clauses from KB without constants.

    :param predicates: list of predicates
    :param variables: list of variables
    :param ci: clause 1
    :param cj: clause 2
    :return: resolved clauses
    """
    resolvant = []

    cI = ci.split()
    cJ = cj.split()

    for item1 in cI:
        for item2 in cJ:
            # Unification
            ciUni, cjUni = unificationNoConst(predicates, variables, item1,
                                              item2)
            if ciUni == ("!" + cjUni) or cjUni == ("!" + ciUni):
                temp1 = ci.split(" ")
                temp2 = cj.split(" ")
                temp1.remove(item1)
                temp2.remove(item2)

                # Need to return new clause to update KB
                resolvant = resultClause(temp1, temp2)

    return resolvant


def unificationNoConst(predicates, variables, ci, cj):
    """
    Function to unify two clauses iff possible.
    Pseudocode reference R&N Pg.285

    :param predicates: list of predicates
    :param variables: list of variables
    :param ci: clause 1
    :param cj: clause 2
    :return: unified clauses
    """
    varCI = ci[ci.find('(') + 1:ci.find(')')].split()
    varCJ = cj[cj.find('(') + 1:cj.find(')')].split()
    predicateCI = ci[:ci.find('(')]
    predicateCJ = cj[:cj.find('(')]

    # Try to match ci and cj
    if len(varCI) == len(varCJ):
        variables = ''
        for item in varCJ:
            variables += item + ','
        variables = variables[:len(variables) - 1]
        ci = predicateCI + '(' + variables + ')'

    return ci, cj


def resolutionConstUni(predicates, variables, constants, clauses):
    """
    PL-Resolution function. Pseudocode reference R&N 7.5 pg.228.
    Function to resolve with constants and universals.

    :param predicates: list of predicates
    :param variables: list of variables
    :param clauses: list of clauses
    :param constants: list of constants
    :return: True iff no new knowledge gained
    """
    new = []
    # Get all combinations
    while True:
        combos = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j
                  in range(i + 1, len(clauses))]
        for (ci, cj) in combos:
            resolvants = resolveConstUni(predicates, constants, variables, ci,
                                         cj)
            if [] in resolvants:
                return True
            for clause in resolvants:
                if clause not in new:
                    new.append(clause)
        if set(new).issubset(clauses):
            return False
        for clause in new:
            if clause not in clauses:
                clauses.append(clause)


def resolveConstUni(predicates, constants, variables, ci, cj):
    """
    Resolve 2 clauses from KB without constants.

    :param predicates: list of predicates
    :param constants: list of constants
    :param variables: list of variables
    :param ci: clause 1
    :param cj: clause 2
    :return: resolved clauses
    """
    resolvant = []

    cI = ci.split()
    cJ = cj.split()

    for item1 in cI:
        for item2 in cJ:
            # Unification
            ciUni, cjUni = unificationConstUni(predicates, variables,
                                               constants, item1, item2)
            if ciUni == ("!" + cjUni) or cjUni == ("!" + ciUni):
                temp1 = ci.split(" ")
                temp2 = cj.split(" ")
                temp1.remove(item1)
                temp2.remove(item2)

                # Need to return new clause to update KB
                resolvant = resultClause(temp1, temp2)

    return resolvant


def unificationConstUni(predicates, constants, variables, ci, cj):
    """
    Function to unify two clauses iff possible.
    Pseudocode reference R&N Pg.285

    :param predicates: list of predicates
    :param variables: list of variables
    :param ci: clause 1
    :param cj: clause 2
    :return: unified clauses
    """
    varCI = ci[ci.find('(') + 1:ci.find(')')].split(',')
    varCJ = cj[cj.find('(') + 1:cj.find(')')].split(',')
    predicateCI = ci[:ci.find('(')]
    predicateCJ = cj[:cj.find('(')]
    ciHasVar = False
    cjHasVar = False

    tempCI = ci
    tempCJ = cj

    if len(varCI) == len(varCJ):
        # Check which clause has variables
        # ci has variable and can be replaced with a constant from CJ
        for item in varCI:
            if item in variables:
                ciHasVar = True
        for item in varCJ:
            if item in variables:
                cjHasVar = True

        if ciHasVar == cjHasVar:
            return tempCI, tempCJ
        elif ciHasVar:
            ciConst = ''
            for item in varCJ:
                ciConst += item + ','
            ciConst = ciConst[:len(ciConst) - 1]
            tempCI = predicateCI + '(' + ciConst + ')'
        elif cjHasVar:
            cjConst = ''
            for item in varCI:
                cjConst += item + ','
            cjConst = cjConst[:len(cjConst) - 1]
            tempCJ = predicateCJ + '(' + cjConst + ')'

    return tempCI, tempCJ


def main():
    """
    Main function
    :return: None
    """
    inputfile = argv[1]
    predicates, variables, constants, functions, kb = parseInput(inputfile)

    if not variables:  # Only constants
        if resolutionNoVars(predicates, constants, kb):
            print('no')
        else:
            print('yes')
    elif not constants:  # Only universals and variables
        if resolutionNoConst(predicates, variables, kb):
            print('no')
        else:
            print('yes')
    elif not functions:  # Universals + constants + variables
        if resolutionConstUni(predicates, constants, variables, kb):
            print('no')
        else:
            print('yes')
    else:  # Functions
        if resolutionWithVars(predicates, variables, constants, functions, kb):
            print('no')
        else:
            print('yes')


if __name__ == "__main__":
    main()
