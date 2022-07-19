import re
import argparse
from dotenv import load_dotenv

import os
import subprocess
from pathlib import Path
from common.utilities import Utilities

load_dotenv()
home = str(Path.home())
WORKDIR = os.getenv('WORKDIR', default=home)



parser = argparse.ArgumentParser(description='Downloads ocp release')
parser.add_argument('--ocpversion', type=str, required=True)
args = parser.parse_args()


channel = args.ocpversion.rsplit('.', 1)[0]

parameter_values_dict = {"<ocpchannel>" :channel, "<ocpversion>" :args.ocpversion}

ocp4path = f'{WORKDIR}/download/ocp4'
if not os.path.isdir(ocp4path):
    os.makedirs (ocp4path)

Utilities.replaceInFile("templates/imageset-config-ocp4.yaml", f'{ocp4path}/imageset-config.yaml', parameter_values_dict)
print(f'{ocp4path}/imageset-config.yaml')