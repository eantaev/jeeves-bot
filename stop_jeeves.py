#!/usr/bin/env python3

import os
import psutil
from jeeves import Jeeves


def main():
    own_pid = os.getpid()
    for pid in psutil.pids():
        p = psutil.Process(pid)
        if own_pid != pid and Jeeves.is_jeeves_process(p):
            print('Found jeeves process', p)
            p.kill()
    print('done')


if __name__ == '__main__':
    main()
