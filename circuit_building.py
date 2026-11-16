from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# initialize a quantum circuit with 1 ancilla qubit, 2 data qubits, and 1 classical bit
qc = QuantumCircuit(3, 1)

# prepare the ancilla in |+>
qc.h(0)

# prepare the data in |++>
qc.h(1)
qc.h(2)

# introduce Z error on the second data qubit
qc.z(2)

# apply CNOT as ancilla qubit is control, data qubits are target
qc.cx(0, 1)
qc.cx(0, 2)

# apply Hadamard to the ancilla
qc.h(0)

# measure the ancilla and store the result in classical bit
qc.measure(0, 0)


# simulate the circuit
backend = AerSimulator().run(qc, shots = 1024)
result = backend.result()

# extract the counts
counts = result.get_counts(qc)
print("measurement counts:", counts)


