#!/usr/bin/python3

import os
import sys
import getpass

queueName = "normal"
timeString = "01:00:00"
userName = getpass.getuser()
targetName = "stampede2-{0}.slurm".format(queueName)
annexName = "{0}@Stampede2-{1}".format(userName, queueName)
startExtra = 'Owner == \\"{0}\\"'.format(userName)

header = '''
#SBATCH -J osgvo-pilot
#SBATCH -o osgvo-pilot/%j.out
#SBATCH -e osgvo-pilot/%j.err
'''

footer = '''
export GLIDEIN_Site="TACC"
export GLIDEIN_ResourceName="Stampede2"
export OSG_SQUID_LOCATION=""

module load tacc-singularity

singularity run --bind /cvmfs:/cvmfs docker://opensciencegrid/osgvo-docker-pilot:latest
'''

with open(targetName, 'w') as targetFile:
	print('#!/bin/bash', file=targetFile)
	targetFile.write(header)
	print('#SBATCH -p {0}'.format(queueName), file=targetFile)
	print('#SBATCH -N 1', file=targetFile)
	print('#SBATCH -n 1', file=targetFile)
	print('#SBATCH -t {0}'.format(timeString), file=targetFile)
	print('', file=targetFile)
	print('export ANNEX_NAME="{0}"'.format(annexName), file=targetFile)
	print('export TOKEN=`cat ~/token.txt`', file=targetFile)
	print('export GLIDEIN_Start_Extra="{0}"'.format(startExtra), file=targetFile)
	targetFile.write(footer)

os.chmod(targetName, 0o600)

print("SLURM script generated.  Perform the following steps to use it.")
print("    (1) Copy '{0}' to a Stampede2 login node.".format(targetName))
print("    (2) Copy your OSG Connect token (usually '~/token.txt') to '~/token.txt' on a Stampede2 login node.");
print("    (3) Create a directory named 'osgvo-pilot' in the directory to which you copied '{0}'.".format(targetName))
print("    (4) Run 'sbatch {0}'.".format(targetName))
sys.exit(0)
