import re
import argparse
import os
import subprocess
from pathlib import Path
parser = argparse.ArgumentParser(description='Downloads ocp release')
parser.add_argument('--ocpversion', type=str, required=True)
args = parser.parse_args()


channel = args.ocpversion.split('.', 2)[0]

parameter_values_dict = {"ocpchannel" :channel, "ocpversion" :args.ocpversion}
input_text = "some text @@ocpchannel@@ some more text @@ocpversion@@ some extra text"
output_text = re.sub(r"@@(\w+?)@@", lambda match: parameter_values_dict[match.group(1)], input_text)
print(output_text)

