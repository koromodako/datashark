# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: datashark.py
#     date: 2018-04-24
#   author: koromodako
#  purpose:
#
#  license:
#    Datashark Forensic framework to process data containers.
#    Copyright (C) 2018 koromodako
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
from os import walk
from asyncio import Lock
from plugins.plugins import PLUGINS
from core.db.database import Database
from helper.exception import DatabaseInitializationException
from helper.logging.logger import Logger
from core.orchestration.task import Task
from core.container.container import Container
from core.orchestration.worker import Worker
from core.plugin.plugin_selector import PluginSelector
from helper.filtering.path_filter import PathFilter
from core.orchestration.orchestrator import Orchestrator
# =============================================================================
#  GLOBALS / CONFIG
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================
class Datashark:
    '''[summary]

    [description]
    '''
    @staticmethod
    def scan_dir(path, recurse, include, exclude):
        '''Scans recursively a directory and returns a list of all path

        Arguments:
            path {[type]} -- [description]
            recurse {[type]} -- [description]
        '''
        LGR.info("Scanning {} for files...".format(path))

        keep = PathFilter(include, exclude)

        if recurse:
            files = [f.resolve() for f in path.glob('**/*') if f.is_file() and keep(f)]
        else:
            files = [f.resolve() for f in path.glob('*') if f.is_file() and keep(f)]

        LGR.info("Scan completed! ({} files)".format(len(files)))
        return files

    def __init__(self, conf):
        '''[summary]

        [description]

        Arguments:
            conf {Configuration} -- [description]
        '''
        self.lock = Lock()
        self.conf = conf
        self.orchestrator = None

    async def _init_db(self, conf_key, read_only):
        '''[summary]

        [description]
        '''
        db_conf = self.conf.get(conf_key)
        if db_conf is None:
            raise DatabaseInitializationException("Missing configuration key: "
                                                  "{}".format(conf_key))

        conn = PluginSelector.select_db_connector(db_conf.get('connector'),
                                                  db_conf.get('settings'),
                                                  read_only)
        if conn is None:
            raise DatabaseInitializationException("Failed to instanciate "
                                                  "connector. Details above.")

        db = Database(conn)
        if not await db.init():
            raise DatabaseInitializationException("Failed to initialize "
                                                  "database. Details above.")

        return db

    async def _process_tasks(self, tasks):
        '''[summary]

        [description]
        '''
        async with self.lock:
            await self.orchestrator.schedule_tasks(tasks)
            await self.orchestrator.process_tasks()

    async def init(self):
        '''[summary]

        [description]
        '''
        # apply default configuration
        max_workers = self.conf.get('max_workers', 4)
        self.conf['max_workers'] = max_workers
        worker_category = self.conf.get('worker_category', 'local')
        self.conf['worker_category'] = Worker.Category(worker_category)
        dissect_and_examine = self.conf.get('dissect_and_examine', False)
        self.conf['dissect_and_examine'] = dissect_and_examine
        check_black_or_white = self.conf.get('check_black_or_white', False)
        self.conf['check_black_or_white'] = check_black_or_white
        # initialize databases
        try:
            self.hash_db = await self._init_db('hash_db_conf',
                                               read_only=False)
            self.container_db = await self._init_db('container_db_conf',
                                                    read_only=False)
            self.whitelist_db = await self._init_db('whitelist_db_conf',
                                                    read_only=True)
            self.blacklist_db = await self._init_db('blacklist_db_conf',
                                                    read_only=True)
            self.dissection_db = await self._init_db('dissection_db_conf',
                                                     read_only=False)
            self.examination_db = await self._init_db('examination_db_conf',
                                                      read_only=False)
        except DatabaseInitializationException as e:
            LGR.exception("An exception occured while initializing databases. "
                          "Details below.")
            return False
        # create orchestrator
        self.orchestrator = Orchestrator(self.conf,
                                         self.hash_db,
                                         self.container_db,
                                         self.whitelist_db,
                                         self.blacklist_db,
                                         self.dissection_db,
                                         self.examination_db)
        return True

    async def term(self):
        '''[summary]

        [description]
        '''
        # abort processing if necessary
        if self.orchestrator.processing:
            await self.orchestrator.abort()
        # terminate databases
        await self.hash_db.term()
        await self.container_db.term()
        await self.whitelist_db.term()
        await self.blacklist_db.term()
        await self.dissection_db.term()
        await self.examination_db.term()

    async def hash(self,
                   path,
                   recurse=False,
                   include=[],
                   exclude=[]):
        '''[summary]

        [description]
        '''
        files = [ path ]
        if path.is_dir():
            files = self.scan_dir(path, recurse, include, exclude)

        tasks = [Task(Task.Category.HASHING,
                      None,
                      Container(name=file.name,
                                path=file,
                                original_path=file)) for file in files]

        await self._process_tasks(tasks)

    async def dissect(self,
                      path,
                      recurse=False,
                      include=[],
                      exclude=[]):
        '''[summary]

        [description]
        '''
        files = [ path ]
        if path.is_dir():
            files = self.scan_dir(path, recurse, include, exclude)

        tasks = []
        if self.conf.check_black_or_white:
            tasks += [Task(Task.Category.HASHING,
                           None,
                           Container(name=file.name,
                                     path=file,
                                     original_path=file)) for file in files]

        tasks += [Task(Task.Category.DISSECTOR_SELECTION,
                       None,
                       Container(name=file.name,
                                 path=file,
                                 original_path=file)) for file in files]

        await self._process_tasks(tasks)

    async def examine(self,
                      path,
                      recurse=False,
                      include=[],
                      exclude=[]):
        '''[summary]

        [description]
        '''
        files = [ path ]
        if path.is_dir():
            files = self.scan_dir(path, recurse, include, exclude)

        tasks = []
        if self.conf.check_black_or_white:
            tasks += [Task(Task.Category.HASHING,
                           None,
                           Container(name=file.name,
                                     path=file,
                                     original_path=file)) for file in files]

        tasks += [Task(Task.Category.EXAMINER_SELECTION,
                      None,
                      Container(name=file.name,
                                path=file,
                                original_path=file)) for file in files]

        await self._process_tasks(tasks)
