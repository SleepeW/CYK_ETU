# Алгоритм CYK (Кока — Янгера — Касами) — простая версия
#
# table[i][j] — множество нетерминалов, из которых выводится
# подстрока words[i..j] (обе границы включительно).

# Правила вида A -> a (нетерминал -> слово)
terminal_rules = {
    "she":  ["NP"],
    "eats": ["V", "VP"],
    "a":    ["Det"],
    "fish": ["N"],
    "fork": ["N"],
    "with": ["P"],
}

# Правила вида A -> B C (нетерминал -> два нетерминала)
binary_rules = {
    ("NP", "VP"):  ["S"],
    ("V", "NP"):   ["VP"],
    ("VP", "PP"):  ["VP"],
    ("P", "NP"):   ["PP"],
    ("Det", "N"):  ["NP"],
    ("NP", "PP"):  ["NP"],
}

def cyk(words):
    n = len(words)
    table = [[set() for _ in range(n)] for _ in range(n)]

    # подстроки из одного слова
    for i in range(n):
        for A in terminal_rules.get(words[i], []):
            table[i][i].add(A)

    # подстроки из слов длиной 2 и более
    for length in range(2, n + 1):            # длина подстроки
        for i in range(n - length + 1):       # где она начинается
            j = i + length - 1                # где заканчивается
            for k in range(i, j):             # где режем на две части
                for B in table[i][k]:
                    for C in table[k + 1][j]:
                        for A in binary_rules.get((B, C), []):
                            table[i][j].add(A)

    return table

def print_table(table, words):
    n = len(words)
    for i in range(n):
        for j in range(i, n):
            cell = ", ".join(sorted(table[i][j])) or "-"
            print(f"«{' '.join(words[i:j+1])}»: {cell}")


sentence = "she eats a fish with a fork"
words = sentence.split()

table = cyk(words)

print_table(table, words)
print()
if "S" in table[0][len(words) - 1]:
    print("Предложение принадлежит языку (S выводится из всей строки)")
else:
    print("Предложение НЕ принадлежит языку")