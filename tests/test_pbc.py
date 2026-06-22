import pytest

from pbc import propagate

# (gate, P, g P g+) for the single-qubit Cliffords H and S
HS_RULES = [
    ("H", "+_", "+_"),
    ("H", "+X", "+Z"),
    ("H", "+Y", "-Y"),
    ("H", "+Z", "+X"),
    ("H", "-X", "-Z"),
    ("S", "+X", "+Y"),
    ("S", "+Y", "-X"),
    ("S", "+Z", "+Z"),
]

# (P, CNOT P CNOT) with control = qubit 0, target = qubit 1
CNOT_RULES = [
    ("+__", "+__"),
    ("+X_", "+XX"),
    ("+_X", "+_X"),
    ("+Y_", "+YX"),
    ("+_Y", "+ZY"),
    ("+Z_", "+Z_"),
    ("+_Z", "+ZZ"),
]


@pytest.mark.parametrize("gate, pauli, expected", HS_RULES)
def test_propagate_single_qubit(gate, pauli, expected):
    assert propagate(pauli, gate, [0], 1) == expected


@pytest.mark.parametrize("pauli, expected", CNOT_RULES)
def test_propagate_cnot(pauli, expected):
    assert propagate(pauli, "CNOT", [0, 1], 2) == expected
