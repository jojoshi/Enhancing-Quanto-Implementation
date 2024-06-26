from qiskit.circuit import CircuitInstruction, Instruction, Qubit


# Circuit-Depth as cost function
def h(instructions: list[CircuitInstruction]):
    depth = dict()
    max = 0
    for i in instructions:
        op: Instruction = i.operation
        qb: list[Qubit] = i.qubits
        if op.name == 'id':
            continue
        for j in qb:
            if j._index in list(depth.keys()):
                depth[j._index] += 1
            else:
                depth[j._index] = 1

            if depth[j._index] > max:
                max = depth[j._index]

    return max