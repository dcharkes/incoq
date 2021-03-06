"""Recompile Distalgo programs."""

import argparse
import sys
import os
from os.path import dirname, join
from multiprocessing import Process
from configparser import ConfigParser
from shutil import copy

import da


def get_benchmark_path():
    """Return the path to the distalgo benchmarks directory.
    Assume current directory is the one containing this file.
    """
    config = ConfigParser()
    config.read('../config.txt')
    dapath = config['python']['DISTALGO_PATH']
    return join(dapath, 'benchmarks')


def compile(dafile, pyfile, incfile, *, use_table34=False):
    """Compile the input dafile to two output files: the main module
    pyfile and the incrementalization interface incfile.
    """
    new_args = [
        sys.argv[0],
        '-o', pyfile,
        '-i', '-m', incfile,
        '--jb-style',
    ]
    if not use_table34:
        new_args += [
            '--no-table3', '--no-table4',
        ]
    new_args += [
        dafile
    ]
    sys.argv = new_args
    
    # Use a separate subprocess because the distalgo compiler
    # doesn't like being called multiple times from the same
    # process.
    p = Process(target=da.compiler.main)
    p.start()
    p.join()

def do_tasks(tasks):
    """Perform several compilation steps. For each task, copy over
    the .da file from the distalgo benchmarks directory to the local
    directory, and do the compilation. Also copy the controller.da
    file to the local directory.
    
    Each task is a pair of the input filename minus the .da suffix,
    relative to the distalgo benchmarks directory; and the output
    file prefix minus the .py or _inc_in.py suffix, relative to the
    local directory.
    """
    mydir = dirname(__file__)
    # Handle case where current dir is the same dir containing
    # this file.
    mydir = join('.', mydir)
    os.chdir(mydir)
    benchpath = get_benchmark_path()
    
    for task in tasks:
        if len(task) == 2:
            inpath, outpath = task
            opts = {}
        elif len(task) == 3:
            inpath, outpath, opts = task
        else:
            assert()
        
        os.makedirs(dirname(outpath), exist_ok=True)
        orig_dafile = join(benchpath, '{}.da'.format(inpath))
        copy(orig_dafile, '{}.da'.format(outpath))
        compile('{}.da'.format(outpath),
                '{}.py'.format(outpath),
                '{}_inc_in.py'.format(outpath),
                **opts)
    
    copy(join(benchpath, 'controller.da'), 'controller.da')


all_tasks = [
    ('clpaxos/spec', 'clpaxos/clpaxos'),
    ('crleader/orig', 'crleader/crleader'),
    ('dscrash/spec', 'dscrash/dscrash'),
    ('hsleader/spec', 'hsleader/hsleader'),
    
    ('lamutex/orig', 'lamutex/lamutex_orig'),
#    ('lamutex/orig', 'lamutex/lamutex_orig_quant',
#     {'use_table34': True}),
    ('lamutex/spec', 'lamutex/lamutex_spec'),
    ('lamutex/spec_lam', 'lamutex/lamutex_spec_lam'),
    
    ('lapaxos/orig', 'lapaxos/lapaxos'),
    ('ramutex/spec', 'ramutex/ramutex'),
    ('ratoken/spec', 'ratoken/ratoken'),
    ('sktoken/orig', 'sktoken/sktoken'),
    ('2pcommit/spec', 'tpcommit/tpcommit'),
#    ('vrpaxos/spec', 'vrpaxos/vrpaxos'),
]


def run(args):
    parser = argparse.ArgumentParser(prog='recompile.py')
    parser.add_argument('target_name', nargs='*', default=None)
    parser.add_argument('--list', action='store_true',
                        help='show available targets')
    parser.add_argument('--all', action='store_true',
                        help='build all tasks')
    
    ns = parser.parse_args(args)
    
    if ns.list:
        print('Available targets:')
        for task in all_tasks:
            print('  ' + task[1])
        return
    
    if len(ns.target_name) == 0 and not ns.all:
        print('No targets specified.\n')
        parser.print_usage()
        return
    
    if ns.all:
        tasks = all_tasks
    else:
        tasks_by_name = {t[1]: t for t in all_tasks}
        tasks = []
        for t_name in ns.target_name:
            if t_name in tasks_by_name:
                tasks.append(tasks_by_name[t_name])
            else:
                raise ValueError('Unknown task "{}"'.format(t_name))
    
    do_tasks(tasks)


if __name__ == '__main__':
    run(sys.argv[1:])
