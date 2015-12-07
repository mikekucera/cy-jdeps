# find_package.py
import os
from collections import defaultdict


def command_output(command):
	import subprocess
	p = subprocess.Popen(command, stdout=subprocess.PIPE)
	while(True):
		retcode = p.poll()
		line = p.stdout.readline()
		yield line
		if(retcode is not None):
			break


def jdeps_command(folder, jar):
	try:
		java_home = os.environ['JAVA_HOME']
	except KeyError:
		print "Error: JAVA_HOME environment variable not set"
	return [java_home + "/bin/jdeps", folder + '/' + jar]


def get_and_validate_commandline_options():
	import sys
	if len(sys.argv) < 3:
		print "Usage:", sys.argv[0], "<package-name> <directory-containing-jars>"
		print "<package-name> must be in the format a.b.c"
		sys.exit(1)
	if not os.path.exists(sys.argv[1]):
		print "Error:", sys.argv[1], "is not a valid path"
		sys.exit(1)
	return (sys.argv[2], sys.argv[1])


def get_files_in_dir(path):
	from os import listdir
	from os.path import isfile, join
	files = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith(".jar")]
	return files


def get_package_name(jdeps_output_line):
	import re
	match = re.match(r'\s*->\s(\S+).*', jdeps_output_line)
	if match:
		return match.group(1)
	else:
		return None


def get_all_subpackages(package_name):
	if package_name is None:
		return
	subpackage = ''
	for segment in package_name.split('.'):
		if subpackage != '':
			subpackage += '.'
		subpackage += segment
		yield subpackage


# main

search_package, jar_dir = get_and_validate_commandline_options()
jar_files = get_files_in_dir(jar_dir)
index = defaultdict(set)

for jar in jar_files:
	jdeps = jdeps_command(jar_dir, jar)
	for line in command_output(jdeps):
		package_name = get_package_name(line)
		for subpackage in get_all_subpackages(package_name):
			if subpackage.startswith(search_package):
				index[subpackage].add(jar)

for key in sorted(index):
	jars = list(index[key])
	jars.sort()
	print key
	for jar in jars:
		print "  ", jar
	print

