import argparse
import subprocess
parser = argparse.ArgumentParser(description='Downloads oc-mirror executable')
parser.add_argument('--ocpversion', type=str, required=False, default="4.10")
# Parse the argument
args = parser.parse_args()
# Print "Hello" + the user input argument
print('Downloading OCP version=', args.ocpversion)
result = subprocess.run(['wget', f'https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable-{args.ocpversion}/oc-mirror.tar.gz', 'oc-mirror.tar.gz'], stdout=subprocess.PIPE)

result = subprocess.run(['tar', 'xvzf', 'oc-mirror.tar.gz'], stdout=subprocess.PIPE)

result = subprocess.run(['mv', 'oc-mirror', '~/bin'], stdout=subprocess.PIPE)

result = subprocess.run(['chmod', '755', '~/bin/oc-mirror'], stdout=subprocess.PIPE)
