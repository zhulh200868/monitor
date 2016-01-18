#!/usr/local/python2.7/bin/python
# -*- coding=utf-8 -*-

import commands


def monitor(frist_invoke=1):
    shell_command = 'ps -C salt-master --no-header|wc -l'
    status,result = commands.getstatusoutput(shell_command)
    value_dic = {
        'salt_pg' : result,
        'status' : status
    }
    return value_dic

if __name__ == '__main__':
    print monitor()