import math
from qiskit.circuit import QuantumCircuit
import cost_function

def calculate_possibilities(g, t, n, d):
    res = 0
    for r in range(0, math.floor(n / 2) + 1):
        res += ((math.factorial(n) / (math.factorial(r) * math.factorial(n - 2 * r)))
                * math.pow(g, n - 2 * r) * math.pow(t, r))
    return math.pow(res, d)


def db_stats(db: dict[str, list[QuantumCircuit]]):
    sum = 0
    max = 0
    print("==========DB-STATS==========")
    for k in db.keys():
        l = len(db[k])
        print(f"{hash(k)}: {l}")
        if l > max: max = l
        sum += l
    print("--------------------")
    print(f"Sum: {sum}")
    print(f"Max: {max}")
    print(f"Number of Classes: {len(db.keys())}")


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
