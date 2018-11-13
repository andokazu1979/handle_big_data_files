#! /usr/bin/env python

import sys
import os
import re
import subprocess
import logging

########################################
# Parameters
########################################

level_ = logging.DEBUG
# level_ = logging.INFO
# level_ = logging.WARNING

server = 'K'
rootdirpath_to = '.'

########################################
# Functions
########################################

def execute_cmd(lst_cmd, shell=False):

    try:
        ret = subprocess.check_output(lst_cmd, shell=shell)
    except subprocess.CalledProcessError as e:
        print("*** Error occured in processing command! ***")
        print("Return code: {0}".format(e.returncode))
        print("Command: {0}".format(e.cmd))
        print("Output: {0}".format(e.output))
        raise e
    return ret


def mkdir_and_scp(server, fpath_from, fpath_to):
    dirpath_to = os.path.dirname(fpath_to)
    execute_cmd('mkdir -p {0}'.format(dirpath_to), shell=True)
    logger.debug('execute scp from: {0}:{1} to: {2}'.format(server, fpath_from, fpath_to))
    execute_cmd('scp {0}:{1} {2}'.format(server, fpath_from, fpath_to), shell=True)

########################################
# Main
########################################

logging.basicConfig(level = level_)
logger = logging.getLogger(__name__)

args = sys.argv
if len(args) == 1:
    raise Exception("Specify md5sum list file!")
elif len(args) >= 3:
    raise Exception("Too many arguments is specified!")

fpath_md5sum_list = args[1]
target_dirname = os.path.basename(fpath_md5sum_list).split('_')[2]

nfiles = int(execute_cmd('wc -l {0}'.format(fpath_md5sum_list), shell=True).split()[0])

for i, line in enumerate(open(fpath_md5sum_list)):
    print('{0} / {1}'.format(i + 1, nfiles))
    items = line.split()
    checksum_from = items[0]
    fpath_from = items[1]
    fpath_to = '{0}/{1}'.format(rootdirpath_to, re.sub('^.*{0}'.format(target_dirname), target_dirname, fpath_from))
    if os.path.exists(fpath_to):
        logger.debug('{0} is existed'.format(fpath_to))
        checksum_to = execute_cmd('md5sum {0}'.format(fpath_to), shell=True).split()[0].decode('utf-8')
        if checksum_from != checksum_to:
            logger.debug('checksum is not matched: {0} != {1}'.format(checksum_from, checksum_to))
            mkdir_and_scp(server, fpath_from, fpath_to)
    else:
        logger.debug('{0} is not existed'.format(fpath_to))
        mkdir_and_scp(server, fpath_from, fpath_to)
