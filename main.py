import sys
from tabulate import tabulate
from grammar_utils import read_grammar, extract_terminals
from first_follow import compute_first, compute_follow
from ll1_parser import build_ll1_table, parse_ll1
from slr1_parser import build_slr_tables, parse_slr

def print_ll1_table(table, terminals):
    print("\nTabla LL(1):")
    headers = ["NoTerminal"] + terminals
    rows = []
    for nonterm in sorted(table):
        row = [nonterm]
        for term in terminals:
            val = f"#{table[nonterm][term]}" if term in table[nonterm] else ""
            row.append(val)
        rows.append(row)
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def print_action_goto_tables(ACTION, GOTO, terminals):
    print("\nTabla ACTION:")
    headers = ["Estado"] + terminals
    rows = []
    for i, row in enumerate(ACTION):
        r = [str(i)]
        for sym in terminals:
            acts = row.get(sym, [])
            text = ", ".join(
                f"s{a[1]}" if a[0] == 's' else f"r{a[1]}" if a[0] == 'r' else "acc"
                for a in acts
            )
            r.append(text)
        rows.append(r)
    print(tabulate(rows, headers=headers, tablefmt="grid"))

    print("\nTabla GOTO:")
    all_nonterms = sorted({sym for row in GOTO for sym in row})
    headers = ["Estado"] + all_nonterms
    rows = []
    for i, row in enumerate(GOTO):
        r = [str(i)]
        for sym in all_nonterms:
            val = row.get(sym, "")
            r.append(str(val) if val != "" else "")
        rows.append(r)
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def main():
    nonterminals, prods = read_grammar()
    if not nonterminals:
        print("Error: no se leyó ningún no terminal.")
        return

    terminals = extract_terminals(nonterminals, prods)
    start = nonterminals[0]
    FIRST = compute_first(nonterminals, prods)
    FOLLOW = compute_follow(nonterminals, prods, FIRST, start)
    is_ll1, ll1_table, prod_list = build_ll1_table(nonterminals, prods, FIRST, FOLLOW)

    is_slr1, slr_ACTION, slr_GOTO, prods_aug = build_slr_tables(nonterminals, prods, FIRST, FOLLOW, start)

    if is_ll1:
        print_ll1_table(ll1_table, terminals)
    if is_slr1:
        print_action_goto_tables(slr_ACTION, slr_GOTO, terminals)

    if is_ll1 and is_slr1:
        while True:
            choice = input("Seleccionar un analizador (T: para LL(1), B: para SLR(1), Q: salir):").strip().upper()
            if choice == 'Q':
                break
            elif choice == 'T':
                while True:
                    line = input().strip()
                    if not line:
                        break
                    print("yes" if parse_ll1(line, nonterminals, ll1_table, prods, start) else "no")
            elif choice == 'B':
                while True:
                    line = input().strip()
                    if not line:
                        break
                    print("yes" if parse_slr(line, slr_ACTION, slr_GOTO, prods_aug) else "no")
    elif is_ll1:
        print("Grammar is LL(1).")
        while True:
            line = input().strip()
            if not line:
                break
            print("yes" if parse_ll1(line, nonterminals, ll1_table, prod_list, start) else "no")

    elif is_slr1:
        print("Grammar is SLR(1).")
        while True:
            line = input().strip()
            if not line:
                break
            print("yes" if parse_slr(line, slr_ACTION, slr_GOTO, prods_aug) else "no")
    else:
        print("Grammar is neither LL(1) nor SLR(1).")

if __name__ == '__main__':
    main()
