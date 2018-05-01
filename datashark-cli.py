#!/usr/bin/env python3
# -!- encoding:utf8 -!-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: main.py
#     date: 2018-04-28
#   author: paul.dautry
#  purpose:
#
#  license:
#    Datashark Forensic framework to process data containers.
#    Copyright (C) 2018 paul.dautry
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  IMPORTS
# =============================================================================
from pathlib import Path
from asyncio import get_event_loop
from argparse import ArgumentParser
from core.datashark import Datashark
from plugins.plugins import PLUGINS
from core.configuration import Configuration
from helper.logging.logger import Logger
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  FUNCTIONS
# =============================================================================
def parse_args():
    '''[summary]

    [description]
    '''
    p = ArgumentParser()
    # - add main parser arguments
    p.add_argument('--debug', '-d', action='store_true', help="Enables debug output.")
    p.add_argument('--silent', '-s', action='store_true', help="Disables console output.")
    p.add_argument('--config', '-c', type=Path,  help="Configuration file.")
    # -- add subparsers
    sp = p.add_subparsers(dest='command')
    sp.required = True
    # --- hash
    hash_p = sp.add_parser('hash')
    hash_p.add_argument('--recurse', '-r', action='store_true',
                        help="Tells datashark to walk recursively if input is "
                             "a folder.")
    hash_p.add_argument('input', type=Path, help="File or directory to process")
    # --- dissect
    dissect_p = sp.add_parser('dissect')
    dissect_p.add_argument('--recurse', '-r', action='store_true',
                           help="Tells datashark to walk recursively if input is "
                             "a folder.")
    dissect_p.add_argument('--examine', help="Perform examination for each "
                                             "container extracted during "
                                             "dissection process.")
    dissect_p.add_argument('input', type=Path, help="File or directory to process")
    # --- examine
    examine_p = sp.add_parser('examine')
    examine_p.add_argument('--recurse', '-r', action='store_true',
                           help="Tells datashark to walk recursively if input is "
                             "a folder.")
    examine_p.add_argument('input', type=Path, help="File or directory to process")
    # --- plugins
    plugins_p = sp.add_parser('plugins')
    # --- version
    version_p = sp.add_parser('version')
    # - parse arguments now
    return p.parse_args()

async def main():
    '''[summary]

    [description]
    '''
    args = parse_args()

    conf = Configuration.load(args.config)

    args.debug = args.debug or conf.get('debug', False)
    args.silent = args.silent or conf.get('silent', False)
    args.logfile_fmt = conf.get('logfile_fmt')
    args.console_fmt = conf.get('console_fmt')

    Logger.configure(Path('/tmp/datashark'),
                     args.debug,
                     args.silent,
                     args.logfile_fmt,
                     args.console_fmt)

    LGR.debug("Arguments: {}".format(args))
    LGR.debug("Configuration: {}".format(conf))

    if args.command == 'version':
        print("Datashark v1.0.0")
        return

    if args.command == 'plugins':
        print(PLUGINS.list())
        return

    LGR.debug(PLUGINS.list())

    ds = Datashark(conf)

    if not await ds.init():
        LGR.error("Datashark.init() failed. Details above.")
        return

    if args.command == 'hash':
        await ds.hash(args.input, args.recurse)

    elif args.command == 'dissect':
        await ds.dissect(args.input, args.recurse)

    elif args.command == 'examine':
        await ds.examine(args.input, args.recurse)

    await ds.term()
# =============================================================================
#  SCRIPT
# =============================================================================
if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(main())
    loop.close()
