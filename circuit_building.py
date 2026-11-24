from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
import numpy as np
import matplotlib.pyplot as plt
from decoder_building import decoder_table, error_to_vector, H_z, logical_x, H_x, recovery
from main import x_gate, z_gate
from qiskit_aer.noise import pauli_error

# initialize a quantum circuit with 4 ancilla qubit, 9 data qubits, and 4 classical bit
qubits = QuantumRegister(13, "q")
syndrome_bits = ClassicalRegister(4, "syndrome")
verification_bits = ClassicalRegister(4, "verification")

qc = QuantumCircuit(qubits, syndrome_bits, verification_bits)


# prepare the data qubits in product of 9 |+>
for q in range(9):
    qc.h(q)

# adding phase-flip noise to each data qubit
p = 0.5
z_noise = pauli_error([("I", 1 - p), ("Z", p)])
noise_instruction = z_noise.to_instruction()

for q in range(9):
    qc.append(noise_instruction, [q])


# add ancilla qubits and build the main structure
for i, row in enumerate(H_x):
    a = 9 + i

    # prepare the ancilla in |+>
    qc.h(a)

    for q in np.flatnonzero(row):

        # apply CNOT as ancilla qubit is control, data qubits are target
        qc.cx(a,q)

    # apply Hadamard to the ancilla
    qc.h(a)

    # measure the ancilla and store the result in syndrome set
    qc.measure(a, syndrome_bits[i])


# correction
for syndrome, correction in decoder_table.items():
    # syndrome[0] is stored in classical bit 0
    value = sum(int(bit) * 2**i for i, bit in enumerate(syndrome))

    # apply the Z gates in 'correction' set
    if "Z" in correction:
        # comparing the syndrome bits with value
        with qc.if_test((syndrome_bits, value)):
            for q, symbol in enumerate(correction):
                if symbol == "Z":
                    qc.z(q)


# rebuild the initial circuit without errors to verify the syndrome
for i, row in enumerate(H_x):
    a = 9 + i
    qc.reset(a)
    qc.h(a)

    for q in np.flatnonzero(row):
        qc.cx(a, q)

    qc.h(a)
    qc.measure(a, verification_bits[i])

# run the circuit including correction and verification.
verification = AerSimulator().run(qc, shots=1024).result()
print("Residual syndrome counts:", verification.get_counts(qc))

verification_counts = {}

for measured_bits, count in verification.get_counts(qc).items():
    verification_string, syndrome_string = measured_bits.split()

    verification_counts[verification_string] = (verification_counts.get(verification_string, 0) + count)

print("Verification counts:", verification_counts)

qc.draw(output="mpl")
plt.show()
