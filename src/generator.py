import math
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
import cost_function


# Compute all possible column circuits
def generateColumns(single_gate_set, two_gate_set, qubits) -> list[QuantumCircuit]:
    db: list[QuantumCircuit] = []

    # iterate over number of occurring two-qubit gates (up do ⎣n/2⎦)
    for i in range(0, math.floor(qubits / 2) + 1):
        enumerate_two_qubit_gates(
            db,
            single_gate_set,
            two_gate_set,
            QuantumCircuit(qubits),
            i,
            qubits,
            []
        )
    return db


def enumerate_two_qubit_gates(db: list[QuantumCircuit], single_gate_set, two_gate_set, qc: QuantumCircuit, r, n,
                              b: list[int]):
    # base case call single qubit gate enumeration
    if r == 0: return enumerate_single_qubit_gates(
        db,
        single_gate_set,
        qc,
        n - 1,
        b
    )

    for i in range(0, n):
        for j in range(0, n):
            # Check if there already exists a two-qubit gate for this qubit
            if (i == j) or (i in b) or (j in b): continue

            # insert new gate
            for k in two_gate_set:
                new_qc = qc.copy()
                new_qc.append(k, [i, j])

                new_b = b.copy()
                new_b.extend([i,j])

                enumerate_two_qubit_gates(
                    db,
                    single_gate_set,
                    two_gate_set,
                    new_qc,
                    r - 1,
                    n,
                    new_b
                )


def enumerate_single_qubit_gates(db: list[QuantumCircuit], single_gate_set, qc: QuantumCircuit, n, b: list[int]):
    # Base case if all qubits are filled
    if (n < 0):
        db.append(qc)
        return

    # Check if qubit is already used for two-qubit gate
    if n in b:
        return enumerate_single_qubit_gates(db, single_gate_set, qc, n - 1, b)

    # enumerate all possible single qubit gates
    for i in single_gate_set:
        new_qc = qc.copy()
        new_qc.append(i, [n])
        enumerate_single_qubit_gates(db, single_gate_set, new_qc, n - 1, b)


# generate un-pruned database with n qubits and depth d based in single- and two-qubit gate-set
def generate_database(single_gate_set, two_gate_set, n, d) -> dict[str, list[QuantumCircuit]]:
    db = dict()

    column_db = generateColumns(single_gate_set, two_gate_set, n)  # Generate Column database
    temp_db = column_db.copy()                                     # Temporary (working set) database

    for i in range(0, d - 1):                                      # Iterate over depth levels
        for j in range(0, len(temp_db)):                           # iterate over columns

            # remove circuits from previous rounds from the front
            # and insert newly generated ones in the back
            qc_base = temp_db.pop(0)
            for r in column_db:
                temp_db.append(qc_base.compose(r))

    # Group results from temp db based on fingerprint
    # and store them in db
    for i in temp_db:
        matrix = Operator(i).data
        if str(matrix) in db:
            db[str(matrix)].append(i)
        else:
            db[str(matrix)] = [i]

    return db


# pruning approach with n qubits and max depth of d
def generate_database_pruned(single_gate_set, two_gate_set, n, d):
    db = dict()

    column_db = generateColumns(single_gate_set, two_gate_set, n)
    print("finished generating row db")
    working_set = dict()
    working_set[1] = column_db.copy()

    reduced = 0     # for stats

    # insert columns into database (are always optimal)
    for r in column_db:
        db[str(Operator(r).data)] = [r]

    for i in range(2, d + 1):
        working_set[i] = list()     # Init working-set for this iteration

        for c in working_set[i - 1]:    # Iterate over circuits from last working set (only include optimal ones)
            for r in column_db:            # Iterate over column circuits
                l_p = c.compose(r)      # Append column circuit
                if str(Operator(l_p).data) not in list(db.keys()):      # Is the circuit new?
                    db[str(Operator(l_p).data)] = [l_p]
                    working_set[i].append(l_p)
                    continue
                if cost_function.h(l_p.data) < cost_function.h((db[str(Operator(l_p).data)][-1]).data):     # Is the circuit cheaper than existing equivalents? (= isOptimal)
                    m = db[str(Operator(l_p).data)][-1]     # Get currently optimal circuit
                    db[str(Operator(l_p).data)] = [l_p]     # Replace current circuit with new one

                    if m in working_set[i]:
                        working_set[i].remove(m)            # Remove m if it got added this round

                    working_set[i].append(l_p)              # insert l_p into working set
                else: reduced += 1                          # For stats
    return db