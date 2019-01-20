#!/usr/bin/env python3

import sys
import argparse


def main():
    print(sys.argv)
    parser = argparse.ArgumentParser()
    parser.add_argument('--silent-start',
                        dest='silent_start',
                        action='store_const',
                        const=True,
                        default=False)
    args = parser.parse_args()
    print(args)
    print(args.silent_start)


if __name__ == '__main__':
    main()
