from typing import Union
import generator_base
import utils
from qiskit.circuit.library import *
from qiskit.circuit.singleton import SingletonGate, SingletonControlledGate
from qiskit.quantum_info import Operator

single_gate_set: list[Union[Operator, SingletonGate]] = [
    # PUT SINGLE-GATE DEFINITIONS HERE
    # TEMPLATE: Operator([[,...], ...])
    HGate(),
    #XGate(),
    #ZGate(),
    Operator([[1, 0], [0, 1]])
    #YGate()
]

two_gate_set: list[Union[Operator, SingletonControlledGate]] = [
    # PUT TWO-QUBIT-GATE DEFINITIONS HERE
    # TEMPLATE: Operator([[,...], ...])
    CXGate(),
    iSwapGate()
]

if __name__ == '__main__':
    n = 2
    d = 3
    database = generator_base.generate_database(single_gate_set, two_gate_set, n, d);
    print(utils.calculate_possibilities(len(single_gate_set), len(two_gate_set), n, d))
    utils.db_stats(database)