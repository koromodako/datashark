# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: datashark.py
#     date: 2018-04-24
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
    def scan_dir(path, recurse):
        '''Scans recursively a directory and returns a list of all path

        Arguments:
            path {[type]} -- [description]
            recurse {[type]} -- [description]
        '''
        if recurse:
            return [f.resolve() for f in path.glob('**/*') if f.is_file()]

        return [f.resolve() for f in path.glob('*') if f.is_file()]

    def __init__(self, conf):
        '''[summary]

        [description]

        Arguments:
            conf {Configuration} -- [description]
        '''
        self.lock = Lock()
        self.conf = conf
        self.orchestrator = None

    async def _init_db(self, conf_key):
        '''[summary]

        [description]
        '''
        db_conf = self.conf.get(conf_key)
        if db_conf is None:
            raise DatabaseInitializationException("Missing configuration key: "
                                                  "{}".format(conf_key))

        conn = PluginSelector.select_db_connector(db_conf.get('connector'),
                                                  db_conf.get('settings'))
        if conn is None:
            raise DatabaseInitializationException("Failed to instanciate "
                                                  "connector. Details above.")

        db = Database(conn)
        if not await db.init():
            raise DatabaseInitializationException("")

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
        worker_category = self.conf.get('worker_category', 'process')
        self.conf['worker_category'] = Worker.Category(worker_category)
        dissect_and_examine = self.conf.get('dissect_and_examine', False)
        self.conf['dissect_and_examine'] = dissect_and_examine
        # initialize databases
        try:
            self.hash_db = await self._init_db('hash_db_conf')
            self.whitelist_db = await self._init_db('whitelist_db_conf')
            self.blacklist_db = await self._init_db('blacklist_db_conf')
            self.dissection_db = await self._init_db('dissection_db_conf')
            self.examination_db = await self._init_db('examination_db_conf')
        except DatabaseInitializationException as e:
            LGR.exception("An exception occured while initializing databases. "
                          "Details below.")
            return False
        # create orchestrator
        self.orchestrator = Orchestrator(self.conf)
        return True

    async def term(self):
        '''[summary]

        [description]
        '''
        # terminate databases
        self.orchestrator.abort()
        await self.hash_db.term()
        await self.whitelist_db.term()
        await self.blacklist_db.term()
        await self.dissection_db.term()
        await self.examination_db.term()

    async def dissect(self, path, recurse=False):
        '''[summary]

        [description]
        '''
        files = [ path ]
        if path.is_dir():
            files = self.scan_dir(path, recurse)

        tasks = [Task(Task.Category.DISSECTOR_SELECTION,
                      self.plugin_selector,
                      Container(name=file.name,
                                path=file,
                                original_path=file)) for file in files]

        await self.process_tasks(tasks)

    async def examine(self, path, recurse=False):
        '''[summary]

        [description]
        '''
        files = [ path ]
        if path.is_dir():
            files = self.scan_dir(path, recurse)

        tasks = [Task(Task.Category.EXAMINER_SELECTION,
                      self.plugin_selector,
                      Container(name=file.name,
                                path=file,
                                original_path=file)) for file in files]

        await self.process_tasks(tasks)

    async def hash(self, path, recurse=False):
        '''[summary]

        [description]
        '''
        files = [ path ]
        if path.is_dir():
            files = self.scan_dir(path, recurse)

        tasks = [Task(Task.Category.HASHING,
                      Hash,
                      Container(name=file.name,
                                path=file,
                                original_path=file)) for file in files]

        await self.process_tasks(tasks)
