# File: main.py 
# Author(s): Saswati Ray, Vedant Sanil
# Created: Wed Feb 17 06:44:20 EST 2021 
# Description:
# Acknowledgements:
# Copyright (c) 2021 Carnegie Mellon University
# This code is subject to the license terms contained in the code repo.

import logging
from multiprocessing import set_start_method
set_start_method("spawn", force=True)
from concurrent import futures
import time
import sys
import os
import shutil
import warnings
import subprocess

warnings.filterwarnings("ignore")
sys.path.append(f'{os.getcwd()}/autonml/')

import grpc
from multiprocessing import cpu_count

# AutonML imports
import autonml.search as search
from autonml.api_v3 import core

TA2_API_HOST = '[::]'
TA2_API_PORT = 45042

def garbage_collect():

    # TODO (vedant) : garbage collection for NBeats is being done
    # for kungfuai primitives. This needs to be resolved within
    # kungfuai NBeats
    if os.path.exists(os.path.join(os.getcwd(), "nbeats_weights")):
        shutil.rmtree(os.path.join(os.getcwd(), "nbeats_weights"))

def main_run():
    '''Main API to invoke complete AutoML pipeline'''

    # Remove all files in output directory
    output_dir = sys.argv[2]
    for search_dir in os.listdir(output_dir):
        search_dir_path = os.path.join(output_dir, search_dir)
        shutil.rmtree(search_dir_path)

    # Search is invoked first to create optimal pipelines
    main_search()

    # Fit and evaluate across searched pipelines
    # TODO (vedant) : error checks here
    fit_and_evaluate(output_dir)

    # Garbage collect any leftover intermediate variables
    garbage_collect()


def fit_and_evaluate(output_dir):

    # TODO (vedant) : Error checking on valid directory paths?
    # Code to score the output, and write to the $D3MOUTPUTDIR directory
    for search_dir in os.listdir(output_dir):
        search_dir_path = os.path.join(output_dir, search_dir)
        pipeline_dir_path = os.path.join(search_dir_path, 'pipelines_ranked')

        for idx, jsonfile in enumerate(os.listdir(pipeline_dir_path)):
            jsonfile_path = os.path.join(pipeline_dir_path, jsonfile)
            prediction_name = jsonfile.replace('.json', '')
            print(f'Evaluating over JSON File {idx+1}/{len(os.listdir(pipeline_dir_path))}: {jsonfile_path}\n')

            p = subprocess.Popen([sys.executable, '-m', 'd3m', 'runtime', '-v',
                                  os.environ['D3MSTATICDIR'], 'fit-produce', '-p',
                                  jsonfile_path, '-r', os.path.join(os.environ['D3MINPUTDIR'], 'TRAIN/problem_TRAIN/problemDoc.json'),
                                  '-i', os.path.join(os.environ['D3MINPUTDIR'], 'TRAIN/dataset_TRAIN/datasetDoc.json'), '-t',
                                  os.path.join(os.environ['D3MINPUTDIR'], 'TEST/dataset_TEST/datasetDoc.json'), '-o',
                                  os.path.join(search_dir_path, 'predictions', f'{prediction_name}.predictions.csv')], 
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            output, error = p.communicate()
            if p.returncode != 0:
                print(output.decode())
                raise RuntimeError(error.decode())

            # Generate code that converts JSON to python code
            src_dir = os.path.dirname(os.path.abspath(__file__))

            pipeline_proc = subprocess.Popen([sys.executable, os.path.join(src_dir, 'mkpline.py'), 
                                                jsonfile_path, os.path.join(search_dir_path, 'executables', f'{prediction_name}.code.py')],
                                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            _, error = pipeline_proc.communicate()
            if p.returncode != 0:
                raise RuntimeError(error.decode())


def main_search():
    '''API called only during search'''
    # TODO (vedant) : error handling if number of args provided is less than zero? 
    # is this very necessary ?

    # TODO (vedant) : pass D3m specific variables directly instead of environment 
    # variables
    logging.info('RUNNING SEARCH')

    os.environ['D3MINPUTDIR'] = sys.argv[1]
    os.environ['D3MOUTPUTDIR'] = sys.argv[2]
    os.environ['D3MTIMEOUT'] = sys.argv[3]
    os.environ['D3MCPU'] = sys.argv[4]
    os.environ['D3MPROBLEMPATH'] = sys.argv[5]
    os.environ['D3MSTATICDIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

    search.search_phase()

def main(argv):
    mode = argv[0]
    logging.info("Running in mode %s", mode)

    if mode == "search":
        search.search_phase()
    else:
        threadpool = futures.ThreadPoolExecutor(max_workers=cpu_count())
        server = grpc.server(threadpool)
        core.add_to_server(server)
        server_string = '{}:{}'.format(TA2_API_HOST, TA2_API_PORT)
        server.add_insecure_port(server_string)
        logging.critical("Starting server on %s", server_string)
        server.start()
        logging.critical("Server started, waiting.")
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            server.stop(0)

if __name__ == '__main__':
    main(sys.argv[1:])
