import json
import urllib2
import sys
import os


if len(sys.argv) < 2:
	print "Usage:", sys.argv[0], "<download_directory>"
	sys.exit(1)

download_dir = sys.argv[1]

if not os.path.isdir(download_dir) or not os.access(download_dir, os.R_OK):
	print "Error:", download_dir, "is not a valid path"
	sys.exit(1)



app_store_url = 'http://apps.cytoscape.org/'
response = json.load(urllib2.urlopen(app_store_url + 'backend/all_apps'))

for app in response:
	release = app['releases'][-1]
	version = release['version']
	filename = download_dir + '/' + app['fullname'].replace(' ','_') + "-v" + version + ".jar"
	downloadUrl = app_store_url + release['release_download_url']

	print "Downloading", filename
	fileRequest = urllib2.urlopen(downloadUrl)
	output = open(filename,'wb')
	output.write(fileRequest.read())
	output.close()


print "Done"