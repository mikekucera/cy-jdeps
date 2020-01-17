# Functions for working with the jdeps command and java packages

import os

try:
	java_home = os.environ['JAVA_HOME']
except KeyError:
	print "Error: JAVA_HOME environment variable not set"
	sys.exit(1)


# Parse command line arguments
def readable_dir(d):
	import argparse
	if os.path.isdir(d) and os.access(d, os.R_OK):
		return d
	else:
		raise argparse.ArgumentTypeError("%s is not a valid path" % d)

def command_output(command):
	import subprocess
	p = subprocess.Popen(command, stdout=subprocess.PIPE)
	while(True):
		retcode = p.poll()
		line = p.stdout.readline()
		yield line
		if(retcode is not None):
			break


def jdeps_command(jar_path, class_level):
	jdeps = os.path.join(java_home, 'bin', 'jdeps')
	if class_level:
		return [jdeps, "-verbose:class", jar_path]
	else:
		return [jdeps, jar_path]


def run_jdeps(jar_path, class_level):
	lines = command_output(jdeps_command(jar_path, class_level))
	return map(get_package_name, lines)


def get_files_in_dir(path):
	from os import listdir
	from os.path import isfile, join
	files = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith(".jar")]
	return files


def get_package_name(jdeps_output_line):
	match = jdeps_output_line.split()
	if len(match) >= 2:
		return match[2]
	else:
		return None


def get_all_subpackages(package_name):
	"""Returns a generator of all package prefixes for the given package"""
	if package_name is None:
		return
	subpackage = ''
	for segment in package_name.split('.'):
		if subpackage != '':
			subpackage += '.'
		subpackage += segment
		yield subpackage


def manifest_imports(jar_path):
	"""Returns a set of the Import-Package imports for a app jar"""
	import jarfile
	import re
	mf = jarfile.ReadManifest(jar_path)
	if not 'Import-Package' in mf.main_section:
		print 'Import-Package not found in ' + jar_path
		return set()
	import_package = mf.main_section['Import-Package']
	# really basic way of parsing package imports
	import_package = re.sub(r'\"(.+?)\"', '', import_package)
	imports = import_package.split(',')
	imports = [imp[0:imp.find(';')] if imp.find(';') > 0 else imp for imp in imports]
	return set(imports)

def has_manifest_header(jar_path, header):
	import jarfile
	mf = jarfile.ReadManifest(jar_path)
	return header in mf.main_section





