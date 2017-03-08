import pytest
import textwrap
import json

import os

from populus.compilation import (
    compile_project_contracts,
    write_compiled_sources,
)


BASE_DIR= os.path.abspath(os.path.dirname(__file__))

project_dir = os.path.join(BASE_DIR, 'projects', 'test-01')


CONTRACT_A_SOURCE = textwrap.dedent(("""
    import "contracts/ContractB.sol";
    import "contracts/ContractC.sol";

    contract A is C {
        function A() {
            B.doit();
        }
    }
"""))


CONTRACT_B_SOURCE = textwrap.dedent(("""
    library B {
        function doit() {}
    }
"""))


CONTRACT_C_SOURCE = textwrap.dedent(("""
    contract C {
        function C() {}
    }
"""))


def test_compilation(project, write_project_file):
    write_project_file('contracts/ContractA.sol', CONTRACT_A_SOURCE)
    write_project_file('contracts/ContractB.sol', CONTRACT_B_SOURCE)
    write_project_file('contracts/ContractC.sol', CONTRACT_C_SOURCE)

    _, compiled_sources = compile_project_contracts(
        project,
    )
    output_file_path = write_compiled_sources(
        project.compiled_contracts_asset_path,
        compiled_sources,
    )

    with open(output_file_path) as outfile:
        compiled_contract_data = json.load(outfile)

    assert 'A' in compiled_contract_data
    assert 'B' in compiled_contract_data
    assert 'C' in compiled_contract_data
