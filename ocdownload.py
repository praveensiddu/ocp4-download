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

os.chdir(WORKDIR)

class Product(Enum):
    ocp = 'ocp'
    operator = 'operator'

    def __str__(self):
        return self.value

parser = argparse.ArgumentParser(description='Downloads ocp release')
parser.add_argument('--product', help='ocp/operator', type=Product, choices=list(Product), required=True)
parser.add_argument('--ocpversion', help='ex 4.10.10', type=str, required=True)
parser.add_argument('--registryurl', help='ex: docker://registry-dev.example.com', type=str, required=True)
parser.add_argument('--opname', help='examples: compliance-operator or odf-operator and so on', type=str, required=False)
parser.add_argument('--opversion', help='ex: 4.9.6', type=str, required=False)
parser.add_argument('--channel', help='ex: stable-4.9.6', type=str, required=False)

args = parser.parse_args()

channel = args.ocpversion.rsplit('.', 1)[0]

if args.product == Product.operator:
    if args.opname == None:
        print('parameter opname is required when product is operator')
        exit(1)
    if args.opversion == None:
        print('parameter opversion is required when product is operator')
        exit(1)
    if args.channel == None:
        print('parameter channel is required when product is operator')
        exit(1)
    component = args.opname
    component_ver = f'{args.opname}_{args.opversion}'
    iscfilename = "imageset-config-operator.yaml"

    catalogindex = f'registry.redhat.io/redhat/redhat-operator-index:v{channel}'
    parameter_values_dict = {"<ocpchannel>": channel, "<ocpversion>": args.ocpversion, "<opname>": args.opname, "<opversion>": args.opversion, "<channel>": args.channel, "<catalogindex>": catalogindex}

else:
    if args.opname != None or args.opversion != None:
        print('parameter opname and opversion must not be set when product is ocp')
        exit(1)
    component = 'ocp4'
    component_ver = f'ocp4_{args.ocpversion}'
    iscfilename = "imageset-config-ocp4.yaml"
    parameter_values_dict = {"<ocpchannel>": channel, "<ocpversion>": args.ocpversion}


def make_downloadpath(folder: str) -> str:
    mypath = f'{WORKDIR}/download/{folder}'
    if not os.path.isdir(mypath):
        shutil.rmtree(mypath, ignore_errors=True)
        os.makedirs(mypath)
    return mypath


def sortbydest(line) -> str:
    line_fields = line.strip().split('=')
    return line_fields[1]

def createdSortedFile(source: str, dest: str) -> None:
    with open(source,'r') as first_file:
        rows = first_file.readlines()
        rows.sort(key=sortbydest)
        with open(dest,'w') as second_file:
            for row in rows:
                second_file.write(row)

if args.product == Product.operator:
    cmdargs = [f'oc-mirror list operators --catalog=registry.redhat.io/redhat/redhat-operator-index:v{channel} --package={args.opname} --channel={args.channel} > stdout.log 2> stderr.log']
    print(f'Checking if the operator exists:\n{cmdargs}')
    data = run(cmdargs, shell=True, check=True)
    with open(r"stdout.log", 'r') as fp:
        lines = len(fp.readlines())
        if lines <= 1:
            print('operator not found. Please check your input: {cmdargs}')
            exit(1)


download_path = make_downloadpath(f'{component}-dryrun')

Utilities.replaceInFile(f'{script_path}/templates/{iscfilename}', f'{download_path}/{iscfilename}', parameter_values_dict)
print(f'Changing working directory to {download_path}')
os.chdir(download_path)
print("Current working directory: {0}".format(os.getcwd()))
cmdargs = [f'oc-mirror --dry-run --config=./{iscfilename} {args.registryurl} > stdout.log 2> stderr.log']
print(f'run oc-mirror dryrun to create mapping.txt:\n{cmdargs}')
data = run(cmdargs, shell=True, check=True)

createdSortedFile('oc-mirror-workspace/mapping.txt', f'{component_ver}_mapping.txt')

# upload the f'{component_ver}_mapping.txt' to git

download_path = make_downloadpath(f'{component}')
Utilities.replaceInFile(f'{script_path}/templates/{iscfilename}', f'{download_path}/{iscfilename}', parameter_values_dict)
print(f'Changing working directory to {download_path}')
os.chdir(download_path)
print("Current working directory: {0}".format(os.getcwd()))
cmdargs = [f'oc-mirror --config=./{iscfilename} {args.registryurl} > stdout.log 2> stderr.log']
print(f'run oc-mirror to download:\n{cmdargs}')
data = run(cmdargs, shell=True, check=True)

#oc-mirror     docker://registry.swarchpoc.com


