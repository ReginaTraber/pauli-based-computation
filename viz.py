from IPython.display import Math
from qiskit import QuantumCircuit
from pbc import propagate

_QGATE = {"H": "h", "S": "s", "T": "t", "Tdg": "tdg", "CNOT": "cx"}


def to_qiskit(circuit, n):
    qc = QuantumCircuit(n)
    for name, targets in circuit:
        getattr(qc, _QGATE[name])(*targets)
    return qc


def draw_circuit(circuit, n, scale=1.2, **kw):
    kw.setdefault(
        "style", {"displaycolor": {"t": ["gold", "black"], "tdg": ["gold", "black"]}}
    )
    return to_qiskit(circuit, n).draw("mpl", scale=scale, **kw)


# ---- LaTeX rendering of the normal-form derivation --------------------------

_CLIFFORD = ("H", "S", "CNOT")


def _gate_tex(name, targets):
    sub = "".join(str(q) for q in targets)
    g = rf"\mathrm{{CNOT}}_{{{sub}}}" if name == "CNOT" else rf"{name}_{{{sub}}}"
    return rf"\textcolor{{green}}{{{g}}}" if name in _CLIFFORD else g


def _pauli_tex(label):
    sign = "-" if label[0] == "-" else ""
    body = label.lstrip("+-")
    terms = [f"{ch}_{{{i}}}" for i, ch in enumerate(body) if ch != "_"]
    return sign + ("".join(terms) if terms else "I")


def _render(items):
    parts = [
        rf"R({_pauli_tex(v)})" if kind == "R" else _gate_tex(*v) for kind, v in items
    ]
    return r"\,".join(parts) if parts else "I"


def normal_form_steps_to_latex(circuit, n, lhs="U"):
    ops = list(reversed(circuit))  # operator order
    rows = [(r"\,".join(_gate_tex(nm, q) for nm, q in ops), "")]

    items = []  # ('R', pauli_label) or ('C', (name, targets))
    for name, targets in ops:
        if name in ("T", "Tdg"):
            j = targets[0]
            sign = "+" if name == "T" else "-"
            items.append(("R", sign + "_" * j + "Z" + "_" * (n - j - 1)))
        else:
            items.append(("C", (name, targets)))
    rows.append((_render(items), r"&& \text{all } T \to R(Z)"))

    pushing = True
    while pushing:
        pushing = False
        for k in range(len(items) - 1):
            (k1, v1), (k2, v2) = items[k], items[k + 1]
            if k1 == "C" and k2 == "R":
                name, targets = v1
                items[k] = ("R", propagate(v2, name, targets, n))  # g P g+
                items[k + 1] = ("C", (name, targets))
                rows.append(
                    (
                        _render(items),
                        rf"&& \text{{push }} {_gate_tex(name, targets)} \text{{ right}}",
                    )
                )
                pushing = True
                break

    body = rf"{lhs} &= {rows[0][0]} {rows[0][1]}"
    for rhs, note in rows[1:]:
        body += rf" \\ &= {rhs} {note}"
    return Math(r"\begin{aligned}" + body + r"\end{aligned}")
