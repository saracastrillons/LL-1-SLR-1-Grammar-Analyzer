def compute_first(nonterminals, productions):
    FIRST = {A: set() for A in nonterminals}
    changed = True

    while changed:
        changed = False
        for A in productions:
            for alpha in productions[A]:
                before = FIRST[A].copy()
                if alpha == ['e']:
                    FIRST[A].add('e')
                else:
                    for symbol in alpha:
                        if symbol not in nonterminals:
                            FIRST[A].add(symbol)
                            break
                        FIRST[A] |= (FIRST[symbol] - {'e'})
                        if 'e' not in FIRST[symbol]:
                            break
                    else:
                        FIRST[A].add('e')
                if FIRST[A] != before:
                    changed = True
    return FIRST

def compute_follow(nonterminals, productions, FIRST, start):
    FOLLOW = {A: set() for A in nonterminals}
    FOLLOW[start].add('$')
    changed = True

    while changed:
        changed = False
        for A in productions:
            for alpha in productions[A]:
                trailer = FOLLOW[A].copy()
                for symbol in reversed(alpha):
                    if symbol in nonterminals:
                        before = FOLLOW[symbol].copy()
                        FOLLOW[symbol] |= trailer
                        if 'e' in FIRST[symbol]:
                            trailer |= (FIRST[symbol] - {'e'})
                        else:
                            trailer = FIRST[symbol].copy()
                        if FOLLOW[symbol] != before:
                            changed = True
                    else:
                        trailer = {symbol}
    return FOLLOW