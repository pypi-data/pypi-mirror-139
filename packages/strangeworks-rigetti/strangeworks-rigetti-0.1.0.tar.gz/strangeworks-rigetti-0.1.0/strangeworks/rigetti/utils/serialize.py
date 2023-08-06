import pyquil

from pyquil import Program


def rigetti_to_sw(program: Program) -> dict:
    if not isinstance(program, Program):
        raise Exception(
            f"strangeworks-rigetti does not know how to serialize the type {type(program)}"
        )

    return {
        "circuit": program.out(),
        "circuit_type": "pyquil.Program",
        "version": pyquil.pyquil_version,
    }
