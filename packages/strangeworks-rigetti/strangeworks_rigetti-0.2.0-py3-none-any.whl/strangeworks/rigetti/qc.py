from ctypes import cast
from typing import Union
import pyquil
from pyquil import Program
from pyquil.api import QuantumComputer
from pyquil.api._abstract_compiler import EncryptedProgram
from typing import List, Mapping, Optional, Sequence
import networkx as nx
import numpy as np
from rpcq.messages import ParameterAref
from pyquil.api._qam import QAM, QAMExecutionResult
from pyquil.paulis import PauliTerm
from pyquil.experiment._main import Experiment
from pyquil.experiment._result import ExperimentResult, bitstrings_to_expectations
from pyquil.experiment._memory import merge_memory_map_lists
from pyquil.experiment._setting import ExperimentSetting
from strangeworks.errors.error import StrangeworksError
import strangeworks


class QuantumComputer(QuantumComputer):
    def __init__(self, ogc: QuantumComputer, as_qvm: bool):
        super().__init__(name=ogc.name, qam=ogc.qam, compiler=ogc.compiler)
        self.as_qvm = "True" if as_qvm else "False"

    def run(
        self, program: Union[Program, EncryptedProgram], shots: int = 1
    ) -> QAMExecutionResult:
        payload = {}
        if isinstance(program, Program):
            payload = self.__serialize_program(program)
            shots = program.num_shots
        elif isinstance(program, EncryptedProgram):
            payload = self.__serialize_executable(program)
        else:
            raise StrangeworksError.invalid_argument(
                "must pass either a program or encrypted program to execute"
            )

        job = strangeworks.client.circuit_runner.run(
            payload=payload, shots=shots, backend=f"rigetti.{self.name}"
        )

        return self.__read_response(program=program, response=job.results())

    def __serialize_executable(self, qe: EncryptedProgram) -> dict:
        return {
            "as_qvm": self.as_qvm,
            "circuit": qe.program,
            "circuit_type": "pyquil.EncryptedProgram",
            "version": pyquil.pyquil_version,
        }

    def __serialize_program(self, p: Program) -> dict:
        return {
            "as_qvm": self.as_qvm,
            "circuit": p.out(),
            "circuit_type": "pyquil.Program",
            "version": pyquil.pyquil_version,
        }

    def __read_response(self, program: Program, response: dict) -> QAMExecutionResult:
        if "data" not in response:
            raise StrangeworksError.bad_response("no data returned from server")
        readout_data = {}
        res = response["data"]
        for i in res:
            readout_data[i] = np.asarray(res[i])
        return QAMExecutionResult(executable=program, readout_data=readout_data)
