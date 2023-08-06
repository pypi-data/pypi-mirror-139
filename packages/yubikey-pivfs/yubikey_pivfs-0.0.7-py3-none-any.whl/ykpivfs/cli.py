#!/usr/bin/env python

import sys
import logging
import argparse

from .fuse import PIVFS


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('mount_point')
    parser.add_argument('--pin', required=True, help='PIN used for private key operations (e.g. "123456")')
    parser.add_argument('--format',
                        required=False,
                        choices=('no', 'yes', 'force'),
                        default='no',
                        help='if the data-slots should be formatted:\n\n\n'
                             '"no" - does not format;\n'
                             '"yes" - formats only if unable to find existing filesystem;\n'
                             '"force" - formats even if filesystem already exists')
    parser.add_argument('--management-key',
                        required=False,
                        default=None,
                        help='key in bytes (e.g. "010203040506070801020304050607080102030405060708")')
    parser.add_argument('--management-key-type',
                        required=False,
                        choices=PIVFS.MANAGEMENT_KEY_TYPES,
                        default=PIVFS.DEFAULT_MANAGEMENT_KEY_TYPE,
                        help='type of key (e.g. "TDES")')
    parser.add_argument('--key-slot',
                        required=False,
                        default=PIVFS.SLOTS_MANAGEMENT_KEY_SLOT,
                        help='PIV-slot containing the private-key used for deriving the encryption-key')
    parser.add_argument('--data-slots',
                        required=False,
                        nargs='+',
                        default=PIVFS.SLOTS_RETIRED,
                        help='PIV-slots used for storing data and that represent the keying-material used in deriving '
                             'the encryption-key')
    parser.add_argument('--block-size',
                        required=False,
                        default=PIVFS.DEFAULT_BLOCK_SIZE,
                        help='maximum amount of data that can fit into each of the data-slots')
    parser.add_argument('--device-serial',
                        required=False,
                        default=None,
                        help='used with multiple devices to select the desired one based on the serial number')
    parser.add_argument('--debug',
                        required=False,
                        default=False,
                        action='store_true',
                        help='shows verbose output')
    parser.description = 'PIV-slots: %s\n\n' % str(PIVFS.SLOTS).replace("'", '').replace('(', '{').replace(')', '}')
    parser.epilog = 'example: "ykpivfs --format yes --pin 123456 --management-key ' \
                    '010203040506070801020304050607080102030405060708 mountpoint"'

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    pivfs_args = parser.parse_args()
    pivfs_args = pivfs_args.__dict__
    mount_point = pivfs_args.pop('mount_point')
    format_fs = pivfs_args.pop('format')
    management_key = bytes.fromhex(pivfs_args.pop('management_key'))
    management_key_type = pivfs_args.pop('management_key_type')
    debug = pivfs_args.pop('debug')

    return {
        'pivfs_args': pivfs_args,
        'mount_point': mount_point,
        'format_fs': format_fs,
        'management_key': management_key,
        'management_key_type': management_key_type,
        'debug': debug
    }


def maybe_format_pivfs(args):
    if args['format_fs'] == 'force':
        PIVFS.format(args['management_key'], args['management_key_type'], **args['pivfs_args'])
    elif args['format_fs'] == 'yes':
        try:
            PIVFS(**args['pivfs_args']).load()
        except:
            PIVFS.format(args['management_key'], args['management_key_type'], **args['pivfs_args'])


def init_pivfs(args):
    """ initializes a new or loads existing filesystem """
    maybe_format_pivfs(args)

    pivfs = PIVFS(**args['pivfs_args'])
    if args['management_key'] and args['management_key_type']:
        pivfs.enable_write(args['management_key'], args['management_key_type'])
    pivfs.load()

    return pivfs


def main():
    args = parse_arguments()
    if args['debug']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    PIVFS.mount(init_pivfs(args), args['mount_point'])
