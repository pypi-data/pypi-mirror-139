from setuptools import setup, find_packages

classifiers = [
	'Development Status :: 5 - Production/Stable',
	'Intended Audience :: Education',
	'Operating System :: Microsoft :: Windows :: Windows 10',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 3'
]

setup(
	name='crocopy',
	version='0.0.1',
	description='Tools to process CROCO',
	long_description=open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
	url='',
	author='Gustav Rautenbach',
	author_email='gustavrautenbach80@gmail.com',
	license='',
	classifiers=classifiers,
	keywords='croco',
	packages=find_packages(),
	install_requires=['numpy','netCDF4','sys','scipy','time','math']
	)