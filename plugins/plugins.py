# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: plugins.py
#     date: 2018-03-25
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
from core.plugin.plugin import Plugin
from core.plugin.registry import Registry
# -----------------------------------------------------------------------------
#  EXAMINERS
# -----------------------------------------------------------------------------
#from plugins.examiners.class_examiner import ClassExaminer
# -----------------------------------------------------------------------------
#  DISSECTORS
# -----------------------------------------------------------------------------
from plugins.dissectors.evt import EVTDissector
from plugins.dissectors.ewf import EWFDissector
from plugins.dissectors.exe import EXEDissector
from plugins.dissectors.lnk import LNKDissector
from plugins.dissectors.nk2 import NK2Dissector
from plugins.dissectors.pff import PFFDissector
from plugins.dissectors.creg import CREGDissector
from plugins.dissectors.qcow import QCOWDissector
from plugins.dissectors.evtx import EVTXDissector
from plugins.dissectors.regf import REGFDissector
from plugins.dissectors.scca import SCCADissector
from plugins.dissectors.vhdi import VHDIDissector
from plugins.dissectors.vmdk import VMDKDissector
from plugins.dissectors.esedb import ESEDBDissector
from plugins.dissectors.olecf import OLECFDissector
from plugins.dissectors.msiecf import MSIECFDissector
# -----------------------------------------------------------------------------
#  DB CONNECTORS
# -----------------------------------------------------------------------------
from plugins.connectors.fs_connector import FSConnector
from plugins.connectors.redis_connector import RedisConnector
from plugins.connectors.mysql_connector import MySQLConnector
from plugins.connectors.sqlite_connector import SQLiteConnector
from plugins.connectors.dev_null_connector import DevNullConnector
from plugins.connectors.postgresql_connector import PostgreSQLConnector
# =============================================================================
#  GLOBALS
# =============================================================================
PLUGINS = Registry()
# -----------------------------------------------------------------------------
#  EXAMINERS
# -----------------------------------------------------------------------------
#PLUGINS.register(Plugin.Category.EXAMINER, )
# -----------------------------------------------------------------------------
#  DISSECTORS
# -----------------------------------------------------------------------------
PLUGINS.register(Plugin.Category.DISSECTOR, PFFDissector)
PLUGINS.register(Plugin.Category.DISSECTOR, EVTDissector)
PLUGINS.register(Plugin.Category.DISSECTOR, EWFDissector)
PLUGINS.register(Plugin.Category.DISSECTOR, EXEDissector)
PLUGINS.register(Plugin.Category.DISSECTOR, LNKDissector)
PLUGINS.register(Plugin.Category.DISSECTOR, NK2Dissector)
PLUGINS.register(Plugin.Category.DISSECTOR, EVTXDissector)
PLUGINS.register(Plugin.Category.DISSECTOR, CREGDissector)
PLUGINS.register(Plugin.Category.DISSECTOR, QCOWDissector)
PLUGINS.register(Plugin.Category.DISSECTOR, REGFDissector)
PLUGINS.register(Plugin.Category.DISSECTOR, SCCADissector)
PLUGINS.register(Plugin.Category.DISSECTOR, VHDIDissector)
PLUGINS.register(Plugin.Category.DISSECTOR, VMDKDissector)
PLUGINS.register(Plugin.Category.DISSECTOR, ESEDBDissector)
PLUGINS.register(Plugin.Category.DISSECTOR, OLECFDissector)
PLUGINS.register(Plugin.Category.DISSECTOR, MSIECFDissector)
# -----------------------------------------------------------------------------
#  DB CONNECTORS
# -----------------------------------------------------------------------------
PLUGINS.register(Plugin.Category.DB_CONNECTOR, FSConnector)
PLUGINS.register(Plugin.Category.DB_CONNECTOR, RedisConnector)
PLUGINS.register(Plugin.Category.DB_CONNECTOR, MySQLConnector)
PLUGINS.register(Plugin.Category.DB_CONNECTOR, SQLiteConnector)
PLUGINS.register(Plugin.Category.DB_CONNECTOR, DevNullConnector)
PLUGINS.register(Plugin.Category.DB_CONNECTOR, PostgreSQLConnector)
