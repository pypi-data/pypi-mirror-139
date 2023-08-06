#!/usr/bin/env python

"""
No rights reserved. All files in this repository are released into the public domain.
"""

from setuptools import setup

setup(
	# Some general metadata. By convention, a plugin is named: 
	# 'opensesame-plugin-[plugin name]'
	name = 'opensesame-plugin-RSVP-copy',
	version = '0.0.1',
	description = 'Add an RSVP task to an OpenSesame experiment',
	author = 'Lot Wolters',
	author_email = 'l.m.wolters.1@student.rug.nl',
	url = 'https://github.com/lotwolters/c-opensesame-plugin-RSVP',
	# Classifiers used by PyPi if you upload the plugin there
	classifiers = [
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering',
		'Environment :: MacOS X',
		'Environment :: Win32 (MS Windows)',
		'Environment :: X11 Applications',
		'License :: OSI Approved :: Apache Software License',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
	],
	# The important bit that specifies how the plugin files should be installed
	# so that they are found by OpenSesame. This is a bit different from normal 
	# Python modules, because an OpenSesame plugin is not a (normal) Python
	# module.
	data_files = [
		# First the target folder
		('share/opensesame_plugins/c_RSVP_plugin',
		# Then a list of files that are copied into the target folder. Make sure that
		# these files are also included in MANIFEST.in!
		[
			'c_opensesame_plugins/c_RSVP_plugin/c_RSVP_plugin.md',
			'c_opensesame_plugins/c_RSVP_plugin/c_RSVP_plugin.png',
			'c_opensesame_plugins/c_RSVP_plugin/c_RSVP_plugin_large.png',
			'c_opensesame_plugins/c_RSVP_plugin/c_RSVP_plugin.py',
			'c_opensesame_plugins/c_RSVP_plugin/info.yaml',
			]
		)]
	)

