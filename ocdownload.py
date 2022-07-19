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

parameter_values_dict = {"ocpchannel" :channel, "ocpversion" :args.ocpversion}
input_text = "some text @@ocpchannel@@ some more text @@ocpversion@@ some extra text"
output_text = re.sub(r"@@(\w+?)@@", lambda match: parameter_values_dict[match.group(1)], input_text)
print(output_text)

Utilities.replaceInFile("templates/imageset-config-ocp4.yaml", f'{WORKDIR}/download/imageset-config.yaml', parameter_values_dict)

