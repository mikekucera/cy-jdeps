import sys
#add lib folder to import paths
sys.path.insert(0, sys.path[0] + '/lib')

import re
import jarfile


file_name = sys.argv[1]

mf = jarfile.ReadManifest(file_name)
import_package = mf.main_section['Import-Package']

# really basic way of parsing package imports
import_package = re.sub(r'\"(.+?)\"', '', import_package)
imports = import_package.split(',')
imports = [imp[0:imp.find(';')] if imp.find(';') > 0 else imp for imp in imports]


# remove
for imp in imports:
	print imp


