from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford, Pauli

_QISKIT_GATE = {"H": "h", "S": "s", "CNOT": "cx"}


def propagate(pauli, name, targets, n):
    qc = QuantumCircuit(n)
    getattr(qc, _QISKIT_GATE[name])(*targets)
    cl = Clifford(qc)
    sign = "-" if pauli[0] == "-" else ""
    body = pauli.lstrip("+-").replace("_", "I")
    p = Pauli(sign + body[::-1])  # big-endian -> qiskit little-endian
    out = p.evolve(cl, frame="s").to_label()  # frame='s' is C P C+
    ph = "-" if out[0] == "-" else "+"
    return ph + out.lstrip("+-")[::-1].replace("I", "_")  # back to big-endian
