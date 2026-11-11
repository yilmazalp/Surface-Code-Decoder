import numpy as np

# generating all binary sums of the matrix rows, representing products of generators
def row_space(check_matrix):
    n = check_matrix.shape[1]
    span = {tuple([0] * n)}

    for row in check_matrix:
        new_vectors = set()

        for vector in span:
            vector = (vector + row) % 2
            new_vectors.add(tuple(vector))

        span.update(new_vectors)

    return span

# check whether a candidate belongs to the row space
def check_stabilizer(stab_matrix, stabilizer):
    return tuple(stabilizer) in row_space(stab_matrix)

# check whether a candidate commutes with the opposite-type generators and is outside its own stabilizer row space
def check_logical_operator(check_matrix, logical_op, stab_matrix):
    # is it outside the stabilizer row space
    if not check_stabilizer(stab_matrix, logical_op):
        for stabilizer in check_matrix:
            # check commuting with the generators
            if np.vdot(logical_op, stabilizer) %2 != 0:
                return False
            else:
                continue
        return True
    else:
        return False

# validating the logical operator, then checking the residual syndrome and logical effect
def recovery(H_check, r, logical_op, stab_matrix):

    if check_logical_operator(H_check, logical_op, stab_matrix=stab_matrix):
        residual_syndrome = (stab_matrix @ r) % 2
        logical_flip = (logical_op @ r) % 2

        if (residual_syndrome == 0).all() and (logical_flip == 0).all():
            return True
        else:
            return False
    else:
        return None



r = np.array([1, 1, 0, 0, 0, 1, 0, 0, 0])


H_x = np.array([[1, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 1, 1, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 1]])

H_z = np.array([[1, 1, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 1, 1]])

logical_x = np.array([1, 0, 0, 1, 0, 0, 1, 0, 0])

print(recovery(H_z, r, logical_x, H_x))


span_x = row_space(H_x)

print(len(span_x))  # Expected: 16
print(check_stabilizer(H_x, [1, 1, 0, 0, 0, 0, 0, 0, 0]))
print(check_stabilizer(H_x, [1, 0, 0, 1, 0, 0, 1, 0, 0]))

# print the X-checks that detect each single-qubit Z error
for q in range(H_x.shape[1]):
    checks = np.flatnonzero(H_x[:, q])
    print(q, checks)


# build the edges such that A_i's represent internal vertices, qubits (values from 0 to 8) are edges, left and right are boundaries
edges = [
    (0, "left", "A0"),
    (1, "A0", "A1"),
    (2, "A1", "right"),
    (3, "left", "A2"),
    (4, "A1", "A2"),
    (5, "A1", "right"),
    (6, "left", "A2"),
    (7, "A2", "A3"),
    (8, "A3", "right")
]

e = [0, 0, 0, 0, 0, 1, 0, 0, 0]

syndrome = (H_x @ e) % 2
error = (H_x.transpose() @ syndrome)
print(syndrome)

qubits = []
for edge in edges:
    if "A1" in edge and ("left" in edge or "right" in edge):
        qubits.append(edge[0])

print(qubits)

c = [0, 0, 1, 0, 0, 0, 0, 0, 0]
print((H_x @ c) % 2)




