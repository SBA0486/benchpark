
from ramble.appkit import *

import sys

class Globalsums(ExecutableApplication):
    """ Test example Globalsums """
    name = "GLOBALSUMS"

    tags = ['test','mpi','openmp']

    executable('globalsums', 'globalsums', use_mpi=True)

    workload('globalsums', executables=['globalsums'])

  #  workload_variable('lx', default='32',
  #                    description='Dimension of the rank-local lattice in X. (Default: 32)',
  #                    workloads=['globalsums'])
    
  #  figure_of_merit('Figure of Merit (FOM)', log_file='{experiment_run_dir}/{experiment_name}.out', fom_regex=r'etime for so.ler =\s+(?P<fom>[-+]?([0-9]*[.])?[0-9]+([eED][-+]?[0-9]+)?)', group_name='fom', units='')

  #  success_criteria('pass', mode='string', match=r'print timing', file='{experiment_run_dir}/{experiment_name}.out')
