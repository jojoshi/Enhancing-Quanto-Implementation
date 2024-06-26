from typing import Union
import generator_base
import utils
import cost_function
from qiskit.circuit.library import *
from qiskit.circuit.singleton import SingletonGate, SingletonControlledGate
from qiskit.quantum_info import Operator

# Single Qubit Gate set
single_gate_set: list[Union[Operator, SingletonGate]] = [
    # PUT SINGLE-GATE DEFINITIONS HERE
    # Operator([[1, 0], [0, 1]]),
    IGate(),
    HGate(),
    XGate(),
    #YGate()
]

# Two Qubit Gate set
two_gate_set: list[Union[Operator, SingletonControlledGate]] = [
    # PUT TWO-QUBIT-GATE DEFINITIONS HERE
    CXGate(),
    # iSwapGate()
]

if __name__ == '__main__':
    n = 2   # number of qubits
    d = 3   # max depth of the circuit
    database = generator_base.generate_database(single_gate_set, two_gate_set, n, d)            # Original Quanto-Algorithm
    database_p = generator_base.generate_database_pruned(single_gate_set, two_gate_set, n, d)   # Pruning Approach

    # for checking the database size
    print(utils.calculate_possibilities(len(single_gate_set), len(two_gate_set), n, d))

    # Compare both databases
    print("==========BASE==========")
    utils.db_stats(database)
    print("==========PRUNED==========")
    utils.db_stats(database_p)
    print(utils.check_coverage(database_p, database))
