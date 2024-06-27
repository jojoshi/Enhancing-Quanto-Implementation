# Prototype for Pruning Techniques in Quantum Circuit Optimization
Authors: 
- Max von Storch : Technische Universität München
- Johannes Schielein : Technische Universität München

This prototype was created as part of the Quantum Software Systems Seminar at [TUM](https://www.tum.de/) and is accompanying a report on Pruning Techniques for [Quanto](https://arxiv.org/abs/2111.11387), a quantum circuit optimizer with automatic circuit identity generation.
This software features both an implementation based on the original approach by Quanto and an improved version on it utilizing pruning techniques which are further discussed in the Report.
The program is written in python using the [Numpy](https://numpy.org/) and [IBM Qiskit](https://www.ibm.com/quantum/qiskit) Frameworks.

## Usage
The prototype doesn't take any arguments. All parameters need to be hard-coded in the main.py file. `n` refers to the used number of Qubits in all circuits and `d` to the maximum
depth the database generation algorithm traverses. The used gate set can be set by Inserting gates in the respective `single_gate_set` and `two_gate_set` arrays. The main method runs both the original and
the optimized algorithm and after that compares both generated databases and prints stats about them.

With the `lookup(c, db)` function you can provide a circuit and database and get the optimal equivalent circuit in the database. Example code for this is provided as comments in the main method.

## Limitations
In contrast to the original Paper this program only features the database generation part and doesn't implement the actual optimizer including tiling since that part wasn't changed 
in our optimization approach. We also don't generate a fingerprint lookup for the base implementation.

