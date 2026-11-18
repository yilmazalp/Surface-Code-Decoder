from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np
import matplotlib.pyplot as plt
from decoder_building import decoder_table, error_to_vector, H_z, logical_x, H_x, recovery

# initialize a quantum circuit with 4 ancilla qubit, 9 data qubits, and 4 classical bit
qc = QuantumCircuit(13, 4)


# prepare the data qubits in product of 9 |+>
for q in range(9):
    qc.h(q)

# set errors on the qubits 0, 2, 4, 5
qc.z(0)
qc.z(2)
qc.z(4)
qc.z(5)


for i, row in enumerate(H_x):
    a = 9 + i

    # prepare the ancilla in |+>
    qc.h(a)

    for q in np.flatnonzero(row):

        # apply CNOT as ancilla qubit is control, data qubits are target
        qc.cx(a,q)

    # apply Hadamard to the ancilla
    qc.h(a)

    # measure the ancilla and store the result in classical bit
    qc.measure(a, i)


# simulate the circuit
backend = AerSimulator().run(qc, shots = 1024)
result = backend.result()

# extract the counts
counts = result.get_counts(qc)
print("Measurement counts:", counts)

# reveal the syndrome
measured_bits = next(iter(counts))
syndrome = tuple(int(bit) for bit in measured_bits[::-1])

# the syndrome
print("Syndrome: ", syndrome)

correction = decoder_table[syndrome]

# the Pauli string that we need to apply for correction
print("Correction we need to apply: ", correction)


# correction
for q in range(len(correction)):
    if correction[q] == 'Z':
        qc.z(q)

# rebuild the initial circuit without errors to verify the syndrome
for i, row in enumerate(H_x):
    a = 9 + i
    qc.reset(a)
    qc.h(a)

    for q in np.flatnonzero(row):
        qc.cx(a, q)

    qc.h(a)
    qc.measure(a, i)

# run the circuit including correction and verification.
verification = AerSimulator().run(qc, shots=1024).result()
print("Residual syndrome counts:", verification.get_counts(qc))

# Z-error is ZIZIZZIII
error = np.array([1, 0, 1, 0, 1, 1, 0, 0, 0])

# compute residual
residual = (error + error_to_vector(correction))%2

# evaluate the recovery operation
print("Is the code space preserved: ", recovery(H_z, residual, logical_x, H_x))


qc.draw(output="mpl")
plt.show()
