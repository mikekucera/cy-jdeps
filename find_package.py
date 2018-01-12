import sys
sys.path.insert(0, sys.path[0] + '/lib') #add lib folder to import paths
import os
import jdeps # from lib folder
from collections import defaultdict
import argparse


# Parse command line arguments
parser = argparse.ArgumentParser(description='Find Cytoscape App Dependencies')
parser.add_argument('-c', dest='class_level', action='store_true', help='find class level dependencies (default: package level)')
parser.add_argument('-f', dest='filter_import', action='store_true', help='use Import-Package to filter dependencies')
parser.add_argument('-s', dest='use_as_subpackage', action='store_true', help='find all packages for which search_package is a subpackage')
parser.add_argument('-v', dest='verbose', action='store_true', help='print verbose debugging output to stdout')
parser.add_argument('jar_dir', type=jdeps.readable_dir, help='directory containing jar files')
parser.add_argument('search_package', nargs='*', help='package(s) to find (must be in the format a.b.c)')

args = parser.parse_args()


# main

jar_files = jdeps.get_files_in_dir(args.jar_dir)
index = defaultdict(set)

# print args.search_package

# perform search
for jar in jar_files:	
    jar_path = os.path.join(args.jar_dir, jar)

    jdeps_imports = jdeps.run_jdeps(jar_path, args.class_level)
    manifest_imports = jdeps.manifest_imports(jar_path) if args.filter_import else set()

    if args.verbose:
        print 'jar: ' + jar
        print 'jdeps_imports: %s' % jdeps_imports
        print 'manifest_imports: %s' % manifest_imports
        print

    for package_name in jdeps_imports:
        if not args.filter_import or package_name in manifest_imports:
            if args.use_as_subpackage:
                for subpackage in jdeps.get_all_subpackages(package_name):
                    for search_package in args.search_package:
                        if subpackage.startswith(search_package):
                            index[subpackage].add(jar)
            else:
                for search_package in args.search_package:
                    if package_name == search_package:
                        index[package_name].add(jar)

# print results
print
for key in sorted(index):
    jars = list(index[key])
    jars.sort()
    print key
    for jar in jars:
        print "  ", jar
    print

