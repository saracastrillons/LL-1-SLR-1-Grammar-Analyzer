def read_grammar():
    n = int(input().strip())
    nonterminals = []
    productions = {}
    for _ in range(n):
        line = input().strip()
        if not line:
            continue
        left, right = line.split('->')
        A = left.strip()
        nonterminals.append(A)
        alternatives = right.strip().split()
        productions.setdefault(A, [])
        for alt in alternatives:
            if alt == 'e':
                productions[A].append(['e'])
            else:
                productions[A].append(list(alt))  # Cada alternativa se toma como lista de símbolos
    return nonterminals, productions

def extract_terminals(nonterminals, productions):
    terminals = set()
    for lhs in productions:
        for prod in productions[lhs]:
            for symbol in prod:
                if symbol not in nonterminals and symbol != 'e':
                    terminals.add(symbol)
    terminals.add('$')  # símbolo de fin de entrada
    return sorted(terminals)