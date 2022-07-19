import argparse
import os
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser(description='Downloads oc-mirror executable')
parser.add_argument('--ocpversion', type=str, required=False, default="4.10")
# Parse the argument
args = parser.parse_args()
# Print "Hello" + the user input argument
print('Downloading OCP version=', args.ocpversion)

if os.path.isfile('oc-mirror.tar.gz'):
    os.remove('oc-mirror.tar.gz')

result = subprocess.run(['wget', f'https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/latest-{args.ocpversion}/oc-mirror.tar.gz'], stdout=subprocess.PIPE)

result = subprocess.run(['tar', 'xvzf', 'oc-mirror.tar.gz'], stdout=subprocess.PIPE)
home = str(Path.home())

result = subprocess.run(['mv', 'oc-mirror', f'{home}/bin'], stdout=subprocess.PIPE)

result = subprocess.run(['chmod', '755', f'{home}/bin/oc-mirror'], stdout=subprocess.PIPE)
print('oc mirror is ready to use')
print(f'it was downloaded from https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable-{args.ocpversion}/oc-mirror.tar.gz')