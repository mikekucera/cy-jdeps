# find_package.py
import os
from collections import defaultdict


try:
	java_home = os.environ['JAVA_HOME']
except KeyError:
	print "Error: JAVA_HOME environment variable not set"
	sys.exit(1)


def command_output(command):
	import subprocess
	p = subprocess.Popen(command, stdout=subprocess.PIPE)
	while(True):
		retcode = p.poll()
		line = p.stdout.readline()
		yield line
		if(retcode is not None):
			break


def jdeps_command(folder, jar, class_level):
	jdeps = java_home + "/bin/jdeps"
	path = folder + '/' + jar
	if class_level:
		return [jdeps, "-verbose:class", path]
	else:
		return [jdeps, path]


def get_and_validate_commandline_options():
	import sys
	class_level = False
	p = 1
	if len(sys.argv) < 3:
		print "Usage:", sys.argv[0], "[-c] <directory-containing-jars> <package-name>"
		print "<package-name> must be in the format a.b.c"
		sys.exit(1)
	if sys.argv[1] == "-c":
		class_level = True
		p += 1
	if not os.path.exists(sys.argv[p]):
		print "Error:", sys.argv[p], "is not a valid path"
		sys.exit(1)
	return (sys.argv[p], sys.argv[p+1], class_level)


def get_files_in_dir(path):
	from os import listdir
	from os.path import isfile, join
	files = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith(".jar")]
	return files


def get_package_name(jdeps_output_line):
	match = jdeps_output_line.split()
	if len(match) >= 2:
		return match[1]
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

jar_dir, search_package, class_level = get_and_validate_commandline_options()
jar_files = get_files_in_dir(jar_dir)
index = defaultdict(set)

for jar in jar_files:
	jdeps = jdeps_command(jar_dir, jar, class_level)
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

