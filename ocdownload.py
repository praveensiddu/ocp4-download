import re
import argparse
from dotenv import load_dotenv
import shutil
from subprocess import run



import os
import subprocess
from pathlib import Path
from common.utilities import Utilities

load_dotenv()
home = str(Path.home())
WORKDIR = os.getenv('WORKDIR', default=home)
print("Current working directory: {0}".format(os.getcwd()))

parser = argparse.ArgumentParser(description='Downloads ocp release')
parser.add_argument('--ocpversion', help='ocp version example 4.10.10', type=str, required=True)
parser.add_argument('--registryurl', help='example docker://registry-dev.example.com ', type=str, required=True)
args = parser.parse_args()

channel = args.ocpversion.rsplit('.', 1)[0]

parameter_values_dict = {"<ocpchannel>" :channel, "<ocpversion>" :args.ocpversion}

def make_downloadpath(product: str) -> str:
    mypath = f'{WORKDIR}/download/{product}'
    if not os.path.isdir(mypath):
        shutil.rmtree(mypath)
        os.makedirs(mypath)
    return mypath

download_path = make_downloadpath("ocp4-dryrun")
iscfilename ="imageset-config-ocp4.yaml"
Utilities.replaceInFile(f'templates/{iscfilename}', f'{download_path}/{iscfilename}', parameter_values_dict)
print(f'Changing working directory to {download_path}')
os.chdir(download_path)
print("Current working directory: {0}".format(os.getcwd()))
print('running oc-mirror with dryrun to create mapping.txt')
data = run([f'oc-mirror --dry-run --config=./{iscfilename} {args.registryurl} > stdout.log 2> stderr.log'], shell=True, check=True)

# upload the mapping.txt to git

download_path = make_downloadpath("ocp4")
Utilities.replaceInFile(f'templates/{iscfilename}', f'{download_path}/{iscfilename}', parameter_values_dict)
print(f'Changing working directory to {download_path}')
os.chdir(download_path)
print("Current working directory: {0}".format(os.getcwd()))
print('running oc-mirror with dryrun to create mapping.txt')
data = run([f'oc-mirror --config=./{iscfilename} {args.registryurl} > stdout.log 2> stderr.log'], shell=True, check=True)


#oc-mirror     docker://registry.swarchpoc.com


