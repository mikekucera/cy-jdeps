import sys
sys.path.insert(0, sys.path[0] + '/lib') #add lib folder to import paths
import argparse
import os
import jdeps

parser = argparse.ArgumentParser(description='Print Import-Package Dependencies')
parser.add_argument('jar_dir', type=jdeps.readable_dir, help='directory containing jar files')
args = parser.parse_args()


jar_files = jdeps.get_files_in_dir(args.jar_dir)

for jar in jar_files:
	jar_path = os.path.join(args.jar_dir, jar)

	simple_app = jdeps.has_manifest_header(jar_path, 'Cytoscape-App')
	#simple_app = not jdeps.has_manifest_header(jar_path, 'Bundle-SymbolicName')

	if simple_app:
		print jar
