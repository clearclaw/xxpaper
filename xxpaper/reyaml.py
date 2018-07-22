import sys
import yaml

d = yaml.safe_load (file (sys.argv[1]))
print yaml.dump (d, width = 70, indent = 2,
                 default_flow_style = False)
                      