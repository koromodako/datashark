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
from helper.logging.logger import Logger
from core.orchestration.task import Task
from core.container.container import Container
from core.orchestration.worker import Worker
from core.plugin.plugin_selector import PluginSelector
from core.orchestration.orchestrator import Orchestrator
# =============================================================================
#  GLOBALS / CONFIG
# =============================================================================
LGR = Logger(Logger.Type.CORE, __name__)
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

    def __init__(self,
                 hash_db,
                 whitelist_db,
                 blacklist_db,
                 dissection_db,
                 examination_db,
                 **kwargs):
        self.plugin_selector = PluginSelector
        conf = {
            'hash_db': hash_db,
            'max_workers': 4,
            'worker_type': Worker.Type.PROCESS,
            'whitelist_db': whitelist_db,
            'blacklist_db': blacklist_db,
            'dissection_db': dissection_db,
            'examination_db': examination_db,
            'plugin_selector': self.plugin_selector,
            'dissect_and_examine': False,
        }
        conf.update(kwargs)
        self.lock = Lock()
        self.conf = Configuration.fromDict(conf)
        self.orchestrator = Orchestrator(self.conf)

    async def process_tasks(self, tasks):
        async with self.lock:
            await self.orchestrator.schedule_tasks(tasks)
            await self.orchestrator.process_tasks()

    async def dissect(self, path, recurse=False):
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
        files = [ path ]
        if path.is_dir():
            files = self.scan_dir(path, recurse)

        tasks = [Task(Task.Category.HASHING,
                      Hash,
                      Container(name=file.name,
                                path=file,
                                original_path=file)) for file in files]

        await self.process_tasks(tasks)
