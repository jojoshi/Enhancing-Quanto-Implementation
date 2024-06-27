import math
from qiskit.circuit import QuantumCircuit
import cost_function

# Calculates the number of possibilities according to Formula (1) and (2) from the Quanto paper
def calculate_possibilities(g, t, n, d):
    res = 0
    for r in range(0, math.floor(n / 2) + 1):
        res += ((math.factorial(n) / (math.factorial(r) * math.factorial(n - 2 * r)))
                * math.pow(g, n - 2 * r) * math.pow(t, r))
    return math.pow(res, d)


# Prints the number of equivalences ant total number of circuits
def db_stats(db: dict[str, list[QuantumCircuit]]):
    sum = 0
    max = 0
    lines = 0
    print("==========DB-STATS==========")
    print("hash: number of circuits")
    for k in db.keys():
        l = len(db[k])
        print(f"{hash(k)}: {l}")
        if l > max: max = l
        sum += l
        if lines > 8:
            print("...")
            break
        lines += 1
    print("--------------------")
    print(f"Total: {sum}")
    print(f"Max. circuits per entry: {max}")
    print(f"Number of Classes: {len(db.keys())}")


# print all entries from database (text-output)
def print_db(db: dict[str, list[QuantumCircuit]]):
    for l in db.values():
        print("====================")
        for i in l:
            print(i.draw(output="text"))
            cost = cost_function.h(i.data)
            print(f"Cost: {cost}")
        print("====================")


# Check if every circuit in src is also in dst
def check_coverage(src: dict[str, list[QuantumCircuit]], dst: dict[str, list[QuantumCircuit]]):
    not_included = 0
    print("==========CHECK-COVERAGE==========")
    for s in src:
        l = list(dst.keys())[0]
        if s not in list(dst.keys()):
            not_included += 1
            print(src[s][0])
    return not_included
