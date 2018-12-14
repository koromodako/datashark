# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: crypto.py
#     date: 2018-04-23
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
from Crypto.Hash import MD2, MD4, MD5, SHA1
from Crypto.Hash import SHA224, SHA256, SHA384, SHA512
from Crypto.Hash import SHA3_224, SHA3_256, SHA3_384, SHA3_512
from helper.logging.logger import Logger
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
HASH_CLASSES = {
    'MD2': MD2,
    'MD4': MD4,
    'MD5': MD5,
    'SHA1': SHA1,
    'SHA-224': SHA224,
    'SHA-256': SHA256,
    'SHA-384': SHA384,
    'SHA-512': SHA512,
    'SHA3-224': SHA3_224,
    'SHA3-256': SHA3_256,
    'SHA3-384': SHA3_384,
    'SHA3-512': SHA3_512,
}
# =============================================================================
#  CLASSES
# =============================================================================
class Crypto:
    '''Provides high-level cryptographic pimitives for Datashark
    '''
    def _instanciate_hash(hash_name):
        hash_cls = HASH_CLASSES.get(hash_name)

        if hash_cls is None:
            raise ValueError("Unhandled hash_name: {}".format(hash_name))

        return hash_cls.new()

    @staticmethod
    def hash(hash_name, container):
        '''[summary]

        Arguments:
            container {Container} -- Container to hash
        '''
        return Crypto.multihash([hash_name], container)[0]

    @staticmethod
    def multihash(hash_names, container):
        '''[summary]

        [description]

        Arguments:
            hashes {[type]} -- [description]
            container {[type]} -- [description]
        '''
        hashes = [Crypto._instanciate_hash(h) for h in hash_names]

        bf = container.bin_file()
        remaining = bf.size()

        if not bf.open():
            LGR.error("Failed to open file for hashing.")
            return None

        while remaining > 0:
            data = bf.read(10240)
            remaining -= len(data)
            for h in hashes:
                h.update(data)

        bf.close()

        return [h.hexdigest() for h in hashes]
