#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Run example isotherm calculation with HKUST1 framework."""

import os
import click

from aiida.engine import run
from aiida.plugins import DataFactory, WorkflowFactory
from aiida.orm import Dict, Str
from aiida import cmdline

# Workchain objects
IsothermWorkChain = WorkflowFactory('lsmo.isotherm')  # pylint: disable=invalid-name

# Data objects
CifData = DataFactory('core.cif')  # pylint: disable=invalid-name
NetworkParameters = DataFactory('zeopp.parameters')  # pylint: disable=invalid-name


@click.command('cli')
@cmdline.utils.decorators.with_dbenv()
@click.option('--raspa_code', type=cmdline.params.types.CodeParamType())
@click.option('--zeopp_code', type=cmdline.params.types.CodeParamType())
def main(raspa_code, zeopp_code):
    """Prepare inputs and submit the Isotherm workchain.
    Usage: verdi run run_isotherm_hkust1.py raspa@localhost network@localhost"""

    builder = IsothermWorkChain.get_builder()

    builder.metadata.label = 'test'

    builder.raspa_base.raspa.code = raspa_code
    builder.zeopp.code = zeopp_code

    options = {
        'resources': {
            'num_machines': 1,
            'tot_num_mpiprocs': 1,
        },
        'max_wallclock_seconds': 1 * 60 * 60,
        'withmpi': False,
    }

    builder.raspa_base.raspa.metadata.options = options
    builder.zeopp.metadata.options = options

    builder.structure = CifData(file=os.path.abspath('data/HKUST-1.cif'), label='HKUST-1')
    builder.molecule = Str('co2')
    builder.parameters = Dict(
        {
            'ff_framework': 'UFF',  # Default: UFF
            'temperature': 400,  # (K) Note: higher temperature will have less adsorbate and it is faster
            'zeopp_probe_scaling': 0.8,
            'zeopp_volpo_samples': 1000,  # Default: 1e5 *NOTE: default is good for standard real-case!
            'zeopp_block_samples': 10,  # Default: 100
            'raspa_widom_cycles': 100,  # Default: 1e5
            'raspa_gcmc_init_cycles': 10,  # Default: 1e3
            'raspa_gcmc_prod_cycles': 100,  # Default: 1e4
            'pressure_min': 0.001,  # Default: 0.001 (bar)
            'pressure_max': 3,  # Default: 10 (bar)
        })

    run(builder)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter

# EOF
