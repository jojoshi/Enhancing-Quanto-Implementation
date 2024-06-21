import math
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator


def compute_row_db(single_gate_set, two_gate_set, qubits) -> list[QuantumCircuit]:
    db: list[QuantumCircuit] = []
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
    if r == 0: return enumerate_single_qubit_gates(
        db,
        single_gate_set,
        qc,
        n - 1,
        b
    )

    for i in range(0, n):
        for j in range(0, n):
            if (i == j) or (i in b) or (j in b): continue
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

    # enumerate all possible gates
    for i in single_gate_set:
        new_qc = qc.copy()
        new_qc.append(i, [n])
        enumerate_single_qubit_gates(db, single_gate_set, new_qc, n - 1, b)


def generate_database(single_gate_set, two_gate_set, n, d) -> dict[str, list[QuantumCircuit]]:
    db = dict()

    row_db = compute_row_db(single_gate_set, two_gate_set, n)
    # print(len(row_db))
    temp_db = row_db.copy()

    for i in range(0, d - 1):
        for j in range(0, len(temp_db)):
            qc_base = temp_db.pop(0)
            for r in row_db:
                temp_db.append(qc_base.compose(r))

    for i in temp_db:
        matrix = Operator(i).data
        if str(matrix) in db:
            db[str(matrix)].append(i)
        else:
            db[str(matrix)] = [i]

    return db
