# -*- coding: utf-8 -*-
""" Add ``flask template-test`` command to send template emails with data read from a test file."""
from __future__ import absolute_import, division, print_function
from setuptools import setup

URL = "https://github.com/geodav-tech/flask-mail-template-tester"

readme = open('README.md').read()

setup_requires = [
	'wheel',
	'autosemver>=0.5.3',
]

install_requires = [
    'Flask>=0.12.2',
    'click>=6.7'
]

setup(
	name='flask-mail-template-tester',
	autosemver={
		'bugtracker_url': URL + '/issues'
	},
	url=URL,
	license="MIT",
	author="Shawn Pacarar",
	author_email="shawn@geodav.tech",
	py_modules=['flask_mail_template_tester'],
	include_package_data=True, # idk what do
	zip_safe=False, # idk what do either
	platforms='any',
	description=__doc__,
	long_description=readme,
	long_description_content_type='text/markdown',
	setup_requires=setup_requires,
	install_requires=install_requires,
	entry_points={
		'flask.commands': [
			'template-test=flask_mail_template_tester:test_template'
		]
	},
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: 3.9',
		'Programming Language :: Python :: 3.10',
		'Programming Language :: Python',
	]
)