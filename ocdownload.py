import re
import argparse
from dotenv import load_dotenv
import shutil
from subprocess import run
import os
from enum import Enum
from pathlib import Path
from common.utilities import Utilities

load_dotenv()
home = str(Path.home())
script_path = Path(os.path.realpath(__file__)).parent

WORKDIR = os.getenv('WORKDIR', default=home)
print("Current working directory: {0}".format(os.getcwd()))


class Product(Enum):
    ocp = 'ocp'
    operator = 'operator'

    def __str__(self):
        return self.value

parser = argparse.ArgumentParser(description='Downloads ocp release')
parser.add_argument('product', type=Product, choices=list(Product))
parser.add_argument('--ocpversion', help='ocp version example 4.10.10', type=str, required=True)
parser.add_argument('--registryurl', help='example docker://registry-dev.example.com ', type=str, required=True)
args = parser.parse_args()

channel = args.ocpversion.rsplit('.', 1)[0]

parameter_values_dict = {"<ocpchannel>" :channel, "<ocpversion>" :args.ocpversion}

def make_downloadpath(product: str) -> str:
    mypath = f'{WORKDIR}/download/{product}'
    if not os.path.isdir(mypath):
        shutil.rmtree(mypath, ignore_errors=True)
        os.makedirs(mypath)
    return mypath

download_path = make_downloadpath("ocp4-dryrun")
iscfilename ="imageset-config-ocp4.yaml"
Utilities.replaceInFile(f'{script_path}/templates/{iscfilename}', f'{download_path}/{iscfilename}', parameter_values_dict)
print(f'Changing working directory to {download_path}')
os.chdir(download_path)
print("Current working directory: {0}".format(os.getcwd()))
print('running oc-mirror with dryrun to create mapping.txt')
data = run([f'oc-mirror --dry-run --config=./{iscfilename} {args.registryurl} > stdout.log 2> stderr.log'], shell=True, check=True)

# upload the mapping.txt to git

download_path = make_downloadpath("ocp4")
Utilities.replaceInFile(f'{script_path}/templates/{iscfilename}', f'{download_path}/{iscfilename}', parameter_values_dict)
print(f'Changing working directory to {download_path}')
os.chdir(download_path)
print("Current working directory: {0}".format(os.getcwd()))
print('running oc-mirror to download')
data = run([f'oc-mirror --config=./{iscfilename} {args.registryurl} > stdout.log 2> stderr.log'], shell=True, check=True)


#oc-mirror     docker://registry.swarchpoc.com


