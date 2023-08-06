import braket._sdk
from braket.circuits import Circuit


def braket_to_sw(circuit: Circuit) -> dict:
    if not isinstance(circuit, Circuit):
        raise Exception(
            f"strangeworks-braket does not know how to serialize the type {type(circuit)}"
        )

    return {
        "circuit": circuit.to_ir().json(),
        "circuit_type": "braket.circuits.Circuit",
        "version": braket._sdk.__version__,
    }
