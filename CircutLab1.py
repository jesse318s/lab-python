from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit import transpile
from qiskit_aer import AerSimulator

qreg_q = QuantumRegister(3, 'q')
creg_c = ClassicalRegister(2, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

circuit.h(qreg_q[0])
circuit.h(qreg_q[1])
circuit.ccx(qreg_q[0], qreg_q[1], qreg_q[2])

state = Statevector.from_int(0, 2**3)
state = state.evolve(circuit)

meas = QuantumCircuit(3, 3)
meas.barrier(range(3))
meas.measure(range(3), range(3))
qc = meas.compose(circuit, range(3), front=True)

aer_sim = AerSimulator()
qc_compiled = transpile(qc, aer_sim)
job = aer_sim.run(qc_compiled, shots=1024)
result = job.result()

counts = result.get_counts(qc_compiled)

print(counts)