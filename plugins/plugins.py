# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: plugins.py
#     date: 2018-03-25
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
from core.plugin.plugin import Plugin
from core.plugin.registry import Registry
# -----------------------------------------------------------------------------
#  EXAMINERS
# -----------------------------------------------------------------------------
#from ${MODULE} import ${CLASS}
# -----------------------------------------------------------------------------
#  DISSECTORS
# -----------------------------------------------------------------------------
#from ${MODULE} import ${CLASS}
# -----------------------------------------------------------------------------
#  DB CONNECTORS
# -----------------------------------------------------------------------------
from plugins.connectors.fs_connector import FSConnector
from plugins.connectors.dev_null_connector import DevNullConnector
# =============================================================================
#  GLOBALS
# =============================================================================
PLUGINS = Registry()
# -----------------------------------------------------------------------------
#  EXAMINERS
# -----------------------------------------------------------------------------
#PLUGINS.register()
# -----------------------------------------------------------------------------
#  DISSECTORS
# -----------------------------------------------------------------------------
#PLUGINS.register()
# -----------------------------------------------------------------------------
#  DB CONNECTORS
# -----------------------------------------------------------------------------
PLUGINS.register(Plugin.Category.DB_CONNECTOR, FSConnector)
PLUGINS.register(Plugin.Category.DB_CONNECTOR, DevNullConnector)
