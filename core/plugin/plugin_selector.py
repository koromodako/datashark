# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: plugin_selector.py
#     date: 2018-04-28
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
from plugins.plugins import PLUGINS
from core.plugin.plugin import Plugin
from helper.logging.logger import Logger
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================
class PluginSelector:

    @staticmethod
    def select_db_connector(name, settings, read_only):
        '''[summary]
        '''
        conn = PLUGINS.instanciate(Plugin.Category.DB_CONNECTOR,
                                   name,
                                   settings,
                                   read_only=read_only)
        LGR.debug("Connector selected: {}".format(conn))
        return conn

    @staticmethod
    def select_examiners_for(container):
        '''[summary]

        Arguments:
            container {[type]} -- [description]
        '''
        count = 0
        examiners = []

        for name, plugin in PLUGINS.plugins(Plugin.Category.EXAMINER):
            count += 1
            examiner = plugin.instance(None)

            if examiner.can_examine(container):
                LGR.debug("Examiner selected: {}".format(name))
                examiners.append(examiner)

        if count == 0:
            LGR.warning("No examiner plugin registered.")

        return examiners

    @staticmethod
    def select_dissectors_for(container):
        '''[summary]

        Arguments:
            container {[type]} -- [description]
        '''
        count = 0
        dissectors = []

        for name, plugin in PLUGINS.plugins(Plugin.Category.DISSECTOR):
            count += 1
            dissector = plugin.instance(None)

            if dissectors.can_dissect(container):
                LGR.debug("Dissector selected: {}".format(name))
                dissectors.append(dissector)

        if count == 0:
            LGR.warning("No dissector plugin registered.")

        return dissectors
