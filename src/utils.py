import math
from qiskit.circuit import QuantumCircuit
def calculate_possibilities(g, t, n, d):
    res = 0
    for r in range(0, math.floor(n / 2) + 1):
        res += (math.factorial(n) / (math.factorial(r) * math.factorial(n - 2*r))) * math.pow(g, n - 2 * r) * math.pow(t, r)
    return math.pow(res, d)

def db_stats(db: dict[str, list[QuantumCircuit]]):

    sum = 0
    max = 0
    for k in db.keys():
        # print("-----------------------------");
        l = len(db[k])
        print(f"{hash(k)}: {l}")
        # print(db[k][0].draw(output="text"))
        if l > max: max = l
        sum += l
    print("-----------------------------")
    print(f"Sum: {sum}")
    print(f"Max: {max}")
    print(f"Number of Classes: {len(db.keys())}")
