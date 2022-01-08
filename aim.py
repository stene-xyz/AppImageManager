#!/usr/bin/env python3
# AIM v0.1.0-beta
#
# AppImageManager (AIM) is a small application for managing installed AppImage files.
# It is currently still in beta, due to a lack of testing and a lack of a lack of features.
#
# TODO:
# - Configurable sources
# - User mode (use w/o root, install for current user only)
# - Store already installed files & their versions
# - Install from a file on disk
# - .desktop files, where applicable

import os, sys, stat # Used for interacting with the system
import requests # Used for downloading files
import json # Used for parsing packages.json

# Prints the usage information of the script
def print_usage():
	print("Usage: aim <install/remove> <package list>")

# Gets package.json
def get_packages():
	sources = ["https://stene.xyz/aim/packages.json"]
	package_list = {}
	for source in sources:
		try:
			package_json = requests.get(source)
			package_list.update(json.loads(package_json.content))
		except Exception as e:
			print("Failed to get packages.json from " + source + ": " + e)
	return package_list

# Actual app code
if __name__ == "__main__":
	if os.geteuid() != 0:
		print("This script must be run as root.")
		sys.exit(-1)

	if len(sys.argv) < 3:
		print_usage()
		sys.exit(-1)

	packages = sys.argv[2:]

	if sys.argv[1] == "install":
		print("Getting package lists...")
		package_list = get_packages()
		for package in packages:
			try:
				if package in package_list:
					print("Downloading " + package + "...")
					package_file = requests.get(package_list[package])
					print("Installing " + package + "...")
					open("/usr/share/aim/" + package, "wb").write(package_file.content)
					os.chmod("/usr/share/aim/" + package, stat.S_IROTH | stat.S_IXOTH)
				else:
					print("Couldn't install " + package + " because it is not in the provided package list.")
			except:
				print("Couldn't install " + package + " because an error occured.")
	elif sys.argv[1] == "remove":
		for package in packages: # Loop through all provided package names and remove them.
			try:
				if(os.path.exists("/usr/share/aim/" + package)):
					print("Removing " + package + "...")
					os.remove("/usr/share/aim/" + package)
				else:
					print("Couldn't remove " + package + " because it is not installed.")
			except:
				print("An error occured while removing " + package + ".")
	else:
		print_usage()
		sys.exit(-1)
