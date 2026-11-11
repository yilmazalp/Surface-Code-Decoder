# Surface Code Decoding

In this notebook, we aim to develop a minimum-weight decoder for nine-qubit rotated surface code. We will begin with creating binary representations (vectors) of stabilizers and logical operators. Then, we will build decoding graphs and evaluate recovery for every $Z$-error pattern.

Now, the current model uses $Z$-only errors and syndrome measurements. Each qubit independently has a $Z$-error with probability $p$. Next, we are going to reveal circuit-based syndrome extraction in Qiskit.

**Content**

1. Define the code and binary representation
2. Identify stabilizers and logical operators
3. Construct the decoding graph
4. Generate all Z-errors
5. Build the minimum-weight decoder table
6. Evaluate recovery and logical failure probability

