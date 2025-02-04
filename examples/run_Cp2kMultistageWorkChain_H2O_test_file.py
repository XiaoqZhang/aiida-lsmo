# -*- coding: utf-8 -*-
""" Test/example for the Cp2kMultistageWorkChain"""

import os
import click
import ase.build

from aiida.engine import run
from aiida.orm import Dict, StructureData, SinglefileData
from aiida.plugins import WorkflowFactory
from aiida import cmdline

Cp2kMultistageWorkChain = WorkflowFactory('lsmo.cp2k_multistage')  # pylint: disable=invalid-name


def run_multistage_h2o_testfile(cp2k_code):
    """Example usage: verdi run thistest.py cp2k@localhost"""

    print('Testing CP2K multistage workchain on H2O')
    print('>>> Loading a custom protocol from file testfile.yaml')

    atoms = ase.build.molecule('H2O')
    atoms.center(vacuum=2.0)
    structure = StructureData(ase=atoms)

    thisdir = os.path.dirname(os.path.abspath(__file__))

    # Construct process builder
    builder = Cp2kMultistageWorkChain.get_builder()
    builder.structure = structure
    builder.protocol_yaml = SinglefileData(
        file=os.path.abspath(os.path.join(thisdir, 'data', 'test_multistage_protocol.yaml')))
    builder.cp2k_base.cp2k.code = cp2k_code
    builder.cp2k_base.cp2k.metadata.options.resources = {
        'num_machines': 1,
        'num_mpiprocs_per_machine': 1,
    }
    builder.cp2k_base.cp2k.metadata.options.max_wallclock_seconds = 1 * 3 * 60
    builder.cp2k_base.cp2k.parameters = Dict({
        'GLOBAL': {
            'PREFERRED_DIAG_LIBRARY': 'SL'
        },
    })

    run(builder)


@click.command('cli')
@cmdline.utils.decorators.with_dbenv()
@click.option('--cp2k-code', type=cmdline.params.types.CodeParamType())
def cli(cp2k_code):
    """Click interface"""
    run_multistage_h2o_testfile(cp2k_code)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
