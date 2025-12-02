def closure(items, prods_index):
    C = set(items)
    added = True
    while added:
        added = False
        for A, alpha, dot in list(C):
            if dot < len(alpha):
                B = alpha[dot]
                for beta in prods_index.get(B, []):
                    item = (B, tuple(beta), 0)
                    if item not in C:
                        C.add(item)
                        added = True
    return C

def goto(items, X, prods_index):
    G = set()
    for A, alpha, dot in items:
        if dot < len(alpha) and alpha[dot] == X:
            G.add((A, alpha, dot+1))
    return closure(G, prods_index)

def build_slr_tables(nonterminals, productions, FIRST, FOLLOW, start):
    prods_index = {}
    prod_list = []

    for A in productions:
        for rhs in productions[A]:
            prod_list.append((A, rhs))
            prods_index.setdefault(A, []).append(rhs)

    augmented = [("S'", [start])] + prod_list
    prods_index["S'"] = [[start]]

    C = [closure({("S'", tuple([start]), 0)}, prods_index)]
    added = True
    while added:
        added = False
        for I in list(C):
            symbols = list({x for A, alpha, dot in I if dot < len(alpha) for x in [alpha[dot]]})
            for X in symbols:
                J = goto(I, X, prods_index)
                if J and J not in C:
                    C.append(J)
                    added = True

    ACTION = [{} for _ in C]
    GOTO = [{} for _ in C]
    ok = True

    for i, I in enumerate(C):
        for A, alpha, dot in I:
            if dot < len(alpha):
                a = alpha[dot]
                if a not in nonterminals and a != 'e':
                    j = C.index(goto(I, a, prods_index))
                    ACTION[i].setdefault(a, []).append(('s', j))
            else:
                if A == "S'":
                    ACTION[i].setdefault('$', []).append(('acc',))
                else:
                    idx = augmented.index((A, list(alpha)))
                    for a in FOLLOW[A]:
                        ACTION[i].setdefault(a, []).append(('r', idx))
        for A in nonterminals:
            J = goto(I, A, prods_index)
            if J in C:
                GOTO[i][A] = C.index(J)

    for row in ACTION:
        for acts in row.values():
            if len(acts) > 1:
                ok = False

    return ok, ACTION, GOTO, augmented

def parse_slr(s, ACTION, GOTO, augmented):
    stack = [0]
    inp = list(s) + ['$']
    while True:
        state = stack[-1]
        a = inp[0]
        if a not in ACTION[state]:
            return False
        act = ACTION[state][a][0]
        if act[0] == 's':
            stack.append(act[1])
            inp.pop(0)
        elif act[0] == 'r':
            A, alpha = augmented[act[1]]
            if alpha != ['e']:
                for _ in alpha:
                    stack.pop()
            state = stack[-1]
            stack.append(GOTO[state][A])
        else:
            return True
