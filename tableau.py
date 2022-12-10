
MAX_CONSTANTS = 10
VAR = ('x', 'y', 'z', 'w')
PRED = ('P', 'Q', 'R', 'S')
PROP = ('p', 'q', 'r', 's')
NEGATEDPROP = ('-p', '-q', '-r', '-s')
LITERAL = ('p', 'q', 'r', 's', '-p', '-q', '-r', '-s')
BINCON = ('^', 'v', '>')
CONSTANTS = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')

# Change it to True to see the working of the code
PRINT = False

def _print(*args):
    s = ''
    if PRINT:
        for i in args:
            s += str(i) + ' '
        print(s)

def checkBalancedBrackets(fmla):
    brackets = []
    for s in fmla:
        if s == '(':
            brackets.append(s)
        if s == ')':
            try:
                brackets.pop()
            except IndexError:
                return False

    if brackets == []:
        return True
    else:
        return False

def isFormulaExp(theory):
    for i in theory:
        if isLiteral(i):
            continue
        else:
            return False

    return True


def getNegationOfProp(prop):
    if prop in PROP:
        return '-' + prop
    elif prop in NEGATEDPROP:
        return prop.replace('-', '')

def getNegation(fmla):
    if fmla[0] == '-':
        return fmla[1:]
    else:
        return '-' + fmla


def isFormulaContradictory(theory):
    usedLiterals = []
    for i in theory:
        if isLiteral(i):
            if getNegation(i) in usedLiterals:
                return True
            else:
                usedLiterals.append(i)

    return False


def isFormulaPredicate(fmla):
    for p in PRED:
        for i in (CONSTANTS + VAR):
            for j in (CONSTANTS + VAR):
                pred = p + '(' + i + ',' + j + ')'
                if fmla.find(pred) != -1:
                    return True
    return False



def isFormulaQuantified(fmla):

    return fmla[0] in ['A', 'E'] and fmla[1] in VAR


def removeQuantifiers(fmla):
    quantifiers = ['Ax', 'Ay', 'Az', 'Aw', 'Ex', 'Ey', 'Ez', 'Ew']

    for q in quantifiers:
        fmla = fmla.replace(q, '')

    return fmla


def removeNegations(fmla):

    return fmla.replace('-', '')


def isFormulaFOL(fmla):
    new_fmla = removeQuantifiers(fmla)
    if new_fmla != fmla:
        return True

    for p in PRED:
        for c1 in CONSTANTS:
            for c2 in CONSTANTS:
                sub_str = p + '(' + c1 + ',' + c2 + ')'
                if fmla.find(sub_str) != -1:
                    return True

    return False


def isFormulaNegation(fmla):

    return fmla[0] == '-'

def isFormulaDoubleNegation(fmla):

    return fmla[0] == '-' and fmla[1] == '-'


def isFormulaBinaryConnective(fmla):
    fmla = removeQuantifiers(fmla)
    fmla = removeNegations(fmla)

    return con(fmla) is not None


def isFormulaValid(fmla):
    if not checkBalancedBrackets(fmla):
        return False

    fmla = removeQuantifiers(fmla)
    fmla = removeNegations(fmla)

    if len(fmla) == 1 and fmla in PROP:
        return True

    if len(fmla) == 3:
        if isFormulaQuantified(fmla) and fmla[2] in PROP:
            return True

    if len(fmla) == 6:
        if isFormulaPredicate(fmla):
            return True

    if len(fmla) == 8:
        if isFormulaQuantified(fmla[:2]) and isFormulaPredicate(fmla[2:]):
         return True

    else:
        _lhs = lhs(fmla)
        _rhs = rhs(fmla)
        if  _lhs != '' and _rhs != '':
                return isFormulaValid(_lhs) and isFormulaValid(_rhs)
        else:
            return False


# Parse a formula, consult parseOutputs for return values.
def parse(fmla):
    try:
        if isFormulaValid(fmla):
            if len(fmla) == 1 and fmla in PROP:
                return 6

            if len(fmla) == 6 and isFormulaPredicate(fmla):
                return 1

            if len(fmla) >= 2 and isFormulaQuantified(fmla):
                if fmla[0] == 'A':
                    return 3
                elif fmla[0] == 'E':
                    return 4

            if isFormulaNegation(fmla):
                if isFormulaFOL(fmla):
                    return 2
                else:
                    return 7
            if isFormulaBinaryConnective(fmla):
                if isFormulaFOL(fmla):
                    return 5
                else:
                    return 8

        else:
            return 0

    except:
        return 0


# Return the LHS of a binary connective formula
def lhs(fmla):
    i = con_index(fmla)

    if i is not None and fmla[0] == '(':
        lhs = fmla[1 : i]
        return lhs
    else:
        return ""


# Return the connective symbol of a binary connective formula
def con(fmla):
    brackets = []

    if fmla[0] == '-':
        return None

    for s in fmla:
        if s == '(':
            brackets.append(s)
        if s == ')':
            brackets.pop()
        if s in BINCON and brackets == ['(']:
            return s


def con_index(fmla):
    brackets = []

    if fmla[0] == '-':
        return None

    for i in range(len(fmla)):
        if fmla[i] == '(':
            brackets.append(fmla[i])
        if fmla[i] == ')':
            brackets.pop()
        if fmla[i] in BINCON and brackets == ['(']:
            return i


# Return the RHS symbol of a binary connective formula
def rhs(fmla):
    i = con_index(fmla)

    if i is not None and fmla[-1] == ')':
        rhs = fmla[i + 1 : len(fmla) - 1]
        return rhs
    else:
        return ""


def isVarInTheory(theory):
    for i in theory:
        if i in VAR:
            return True

    return True


def isLiteral(phi):

    return phi in LITERAL or parse(phi) == 1 or parse(getNegation(phi)) == 1


def pickPhi(theory):
        for i in theory:
            if not isLiteral(i):
                theory.remove(i)
                return i


def isCaseAlpha(phi):
    parsed = parse(phi)
    connective = con(phi)

    if parsed in [5, 8] and connective == '^':
        return True
    elif parsed in [2, 7] and con(getNegation(phi)) == 'v' and phi[1] not in ['A', 'E']:
        return True
    elif parsed in [2, 7] and con(getNegation(phi)) == '>' and phi[1] not in ['A', 'E']:
        return True
    elif isFormulaDoubleNegation(phi):
        return True
    else:
        return False

def applyAlpha(phi):
    parsed = parse(phi)
    connective = con(phi)

    if parsed in [5, 8] and connective == '^':
        alpha_1 = lhs(phi)
        alpha_2 = rhs(phi)
    elif parsed in [2, 7] and con(getNegation(phi)) == 'v' and phi[1] not in ['A', 'E']:
        _print('here1')
        alpha_1 = getNegation(lhs(getNegation(phi)))
        alpha_2 = getNegation(rhs(getNegation(phi)))
    elif parsed in [2, 7] and con(getNegation(phi)) == '>' and phi[1] not in ['A', 'E']:
        _print('here2', phi[1 : -1])
        alpha_1 = lhs(getNegation(phi))
        alpha_2 = getNegation(rhs(getNegation(phi)))
    elif isFormulaDoubleNegation(phi):
        alpha_1 = phi.replace('-', '', 2)
        alpha_2 = ''

    if alpha_2 != '':
        return [alpha_1, alpha_2]
    else:
        return [alpha_1]


def isCaseBeta(phi):
    parsed = parse(phi)
    connective = con(phi)

    if parsed in [5, 8] and connective == 'v':
        return True
    elif parsed in [5, 8] and connective == '>':
        return True
    elif parsed in [2, 7] and con(getNegation(phi)) == '^' and phi[1] not in ['A', 'E']:
        return True
    else:
        return False


def applyBeta(phi):
    parsed = parse(phi)
    connective = con(phi)

    if parsed in [5, 8] and connective == 'v':
        _print('beta1')
        beta_1 = lhs(phi)
        beta_2 = rhs(phi)
    elif parsed in [5, 8] and connective == '>':
        _print('beta2')
        beta_1 = getNegation(lhs(phi))
        beta_2 = rhs(phi)
    elif parsed in [2, 7] and con(getNegation(phi)) == '^' and phi[1] not in ['A', 'E']:
        _print('beta3')
        beta_1 = getNegation(lhs(getNegation(phi)))
        beta_2 = getNegation(rhs(getNegation(phi)))

    return (beta_1, beta_2)


def isCaseDelta(phi):
    parsed = parse(phi)
    connective = con(phi)

    if parsed == 4:
        return True
    elif parsed == 2:
        if phi[1] == 'A' and phi[2] in VAR:
            return True


def applyQuantifier(phi, quantifier_type, quantifiedVar, constant):
    new_fmla = phi.replace(quantifier_type + quantifiedVar, '', 1)
    next_quant_index = new_fmla.find(quantifier_type + quantifiedVar)

    if next_quant_index != -1:
        new_fmla = new_fmla[:next_quant_index].replace(quantifiedVar, constant) + new_fmla[next_quant_index:]
        return new_fmla

    return new_fmla.replace(quantifiedVar, constant)


def applyDelta(phi, closedTerms):
    parsed = parse(phi)

    if parsed == 4:
        quantifiedVar = phi[1]
        for c in CONSTANTS:
            if (quantifiedVar, c) not in closedTerms:
                delta = applyQuantifier(phi, 'E', quantifiedVar, c)
                delta = delta.replace('A' + c, 'A' + quantifiedVar)
                closedTerms.append((quantifiedVar, c))
                return [delta]
    elif parsed == 2:
        quantifiedVar = phi[2]
        if phi[1] == 'A' and phi[2] in VAR:
            for c in CONSTANTS:
                if c not in closedTerms:
                    delta = applyQuantifier(phi, 'A', quantifiedVar, c)
                    delta = delta.replace('E' + c, 'E' + quantifiedVar)
                    closedTerms.append(c)
                    return [delta] #we didn't remove negation from theory so no need to negate while returning


def isCaseGamma(phi):
    parsed = parse(phi)

    if parsed == 3:
        return True
    elif parsed == 2:
        if phi[1] == 'E' and phi[2] in VAR:
            return True


def applyGamma(phi, closedTerms, usedConstants):
    parsed = parse(phi)
    gammaList = []
    if parsed == 3:
        quantifiedVar = phi[1]
        for c in CONSTANTS:
            gamma = applyQuantifier(phi, 'A', quantifiedVar, c)
            gamma = gamma.replace('E' + c, 'E' + quantifiedVar)
            if gamma not in gammaList:
                gammaList.append(gamma)
        return gammaList
    elif parsed == 2:
        quantifiedVar = phi[2]
        if phi[1] == 'E' and phi[2] in VAR:
            for c in CONSTANTS:
                gamma = applyQuantifier(phi, 'E', quantifiedVar, c)
                gamma = gamma.replace('A' + c, 'A' + quantifiedVar)
                if getNegation(gamma) not in gammaList:
                    gammaList.append(getNegation(gamma))

            return gammaList


# You may choose to represent a theory as a set or a list
def theory(fmla):#initialise a theory with a single formula in it
    theory = [fmla]

    return theory


#check for satisfiability
def sat(tableau):
#output 0 if not satisfiable, output 1 if satisfiable, output 2 if number of constants exceeds MAX_CONSTANTS
    closedTerms = []
    usedConstants = []
    while tableau != []:
        _print("tableau: ", tableau)
        sigma = tableau.pop(0)

        if isFormulaExp(sigma) and not isFormulaContradictory(sigma):
            return 1

        elif len(closedTerms) >= 10:

            return 2

        phi = pickPhi(sigma)
        _print('phi: ', phi)
        if isCaseAlpha(phi):
            _print("phi at case alpha: ", phi)
            alpha = applyAlpha(phi) #returns list of 1 or 2 strings
            _print("alpha: ", alpha)
            sigma = sigma + alpha
            if not isFormulaContradictory(sigma) and sigma not in tableau:
                tableau.append(sigma)
        elif isCaseBeta(phi):
            _print("phi at case beta: ", phi)
            beta_1, beta_2 = applyBeta(phi) #returns tuple of 2 strings
            _print("beta_1: ", beta_1, "   beta_2: ", beta_2)
            sigma_1 = sigma + [beta_1]
            sigma_2 = sigma + [beta_2]
            if not isFormulaContradictory(sigma_1) and sigma_1 not in tableau:
                tableau.append(sigma_1)

            if not isFormulaContradictory(sigma_2) and sigma_2 not in tableau:
                tableau.append(sigma_2)
        elif isCaseDelta(phi):
            _print('phi at case delta: ', phi)
            delta = applyDelta(phi, closedTerms)
            _print("delta: ", delta)
            sigma = sigma + delta
            if not isFormulaContradictory(sigma) and sigma not in tableau:
                tableau.append(sigma)
        elif isCaseGamma(phi):
            _print('phi at case gamma: ', phi)
            gammaList = applyGamma(phi, closedTerms, usedConstants)
            _print("gamma: ", gammaList)
            sigma = sigma + gammaList
            if not isFormulaContradictory(sigma) and sigma not in tableau:
                tableau.append(sigma)

    return 0


#DO NOT MODIFY THE CODE BELOW
f = open('input.txt')

parseOutputs = ['not a formula',
                'an atom',
                'a negation of a first order logic formula',
                'a universally quantified formula',
                'an existentially quantified formula',
                'a binary connective first order formula',
                'a proposition',
                'a negation of a propositional formula',
                'a binary connective propositional formula']

satOutput = ['is not satisfiable', 'is satisfiable', 'may or may not be satisfiable']



firstline = f.readline()

PARSE = False
if 'PARSE' in firstline:
    PARSE = True

SAT = False
if 'SAT' in firstline:
    SAT = True

for line in f:
    if line[-1] == '\n':
        line = line[:-1]
    parsed = parse(line)

    if PARSE:
        output = "%s is %s." % (line, parseOutputs[parsed])
        if parsed in [5,8]:
            output += " Its left hand side is %s, its connective is %s, and its right hand side is %s." % (lhs(line), con(line) ,rhs(line))
        print(output)

    if SAT:
        if parsed:
            tableau = [theory(line)]
            print('%s %s.' % (line, satOutput[sat(tableau)]))

        else:
            print('%s is not a formula.' % line)
