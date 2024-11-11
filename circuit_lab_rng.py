from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator

# Initialize quantum circuit
qreg_q = QuantumRegister(4, 'q')
creg_c = ClassicalRegister(4, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

# Apply Hadamard gate to all qubits
circuit.h(qreg_q)

# Measures all qubits
circuit.measure(qreg_q, creg_c)

# Run circuit on Aer simulator
aer_sim = AerSimulator()
job = aer_sim.run(circuit, shots=1024)
result = job.result()

# Get counts from the result
counts = result.get_counts(circuit)

print('RESULT: ', counts, '\n')