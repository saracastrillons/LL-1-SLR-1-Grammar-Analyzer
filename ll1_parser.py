def build_ll1_table(nonterminals, productions, FIRST, FOLLOW):
    table = {A: {} for A in nonterminals}
    prod_list = []
    ok = True

    for A in productions:
        for rhs in productions[A]:
            prod_list.append((A, rhs))

    for idx, (A, alpha) in enumerate(prod_list):
        firsts = set()
        nullable = True
        for X in alpha:
            if X not in nonterminals:
                firsts.add(X)
                nullable = False
                break
            firsts |= (FIRST[X] - {'e'})
            if 'e' not in FIRST[X]:
                nullable = False
                break
        if nullable:
            firsts.add('e')

        for a in firsts:
            if a == 'e':
                for b in FOLLOW[A]:
                    if b in table[A]:
                        ok = False
                    table[A][b] = idx
            else:
                if a in table[A]:
                    ok = False
                table[A][a] = idx

    return ok, table, prod_list

def parse_ll1(s, nonterminals, table, prod_list, start):

    stack = [start]
    input_stream = list(s) + ['$']
    _, _, prod_list = build_ll1_table(nonterminals, prod_list, {}, {})

    while stack:
        top = stack.pop()
        cur = input_stream[0]

        if top == '$' and cur == '$':
            return True

        if top in nonterminals:
            if cur in table[top]:
                idx = table[top][cur]
                _, rhs = prod_list[idx]
                if rhs != ['e']:
                    stack += reversed(rhs)
            else:
                return False
        else:
            if top == cur:
                input_stream.pop(0)
            else:
                return False
    return False
