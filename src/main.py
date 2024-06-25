from typing import Union
import generator_base
import utils
import cost_function
from qiskit.circuit.library import *
from qiskit.circuit.singleton import SingletonGate, SingletonControlledGate
from qiskit.quantum_info import Operator

single_gate_set: list[Union[Operator, SingletonGate]] = [
    # PUT SINGLE-GATE DEFINITIONS HERE
    # Operator([[1, 0], [0, 1]]),
    IGate(),
    HGate(),
    XGate(),
    #YGate()
]

two_gate_set: list[Union[Operator, SingletonControlledGate]] = [
    # PUT TWO-QUBIT-GATE DEFINITIONS HERE
    CXGate(),
    # iSwapGate()
]

if __name__ == '__main__':
    n = 2
    d = 3
    database = generator_base.generate_database(single_gate_set, two_gate_set, n, d)
    database_p = generator_base.generate_database_pruned(single_gate_set, two_gate_set, n, d)

    print(utils.calculate_possibilities(len(single_gate_set), len(two_gate_set), n, d))
    # utils.print_db(database)
    # e = list(database.values())[20][0]
    # print(e.draw(output="text"))
    # print(cost_function.h(e.data))
    print("==========BASE==========")
    utils.db_stats(database)
    print("==========PRUNED==========")
    utils.db_stats(database_p)
    print(utils.check_coverage(database_p, database))
