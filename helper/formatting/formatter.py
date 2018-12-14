# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: formatter.py
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
from termcolor import colored
from helper.logging.logger import Logger
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================

class Formatter:
    '''Formatter class

    Provides many useful static methods to print bytefield using different
    representations
    '''
    TAB = ' ' * 4

    @staticmethod
    def printable(byte):
        '''Returns a character if it's part of ASCII printable caracters

        Arguments:
            byte {bytes} -- Byte to convert as a char if possible

        Returns:
            str -- Single ASCII char value for given byte
        '''
        return "." if (byte < 0x20 or byte > 0x7e) else chr(byte)

    @staticmethod
    def format_size(size, suffix="B"):
        '''[summary]

        Arguments:
            size {number} -- [description]

        Keyword Arguments:
            suffix {str} -- [description] (default: {'B'})
        '''
        for unit in ["","K","M","G","T","P","E","Z"]:

            if abs(size) < 1024.0:
                return "{:3.1f}{}{}".format(size, unit, suffix)

            size /= 1024.0

        return "{:.1f}{}{}".format(size, "Y", suffix)

    @staticmethod
    def hexdump_lines(data, col_sz=2, col_num=4, human=True, max_lines=10):
        '''[summary]

        Arguments:
            data {bytes or bytearray} -- [description]

        Keyword Arguments:
            col_sz {int} -- [description] (default: {2})
            col_num {int} -- [description] (default: {4})
            human {bool} -- [description] (default: {True})
            max_lines {int} -- [description] (default: {10})
        '''
        lines = []
        row_sz = col_sz * col_num
        r = len(data) % row_sz

        for k in range(0, (len(data) // row_sz) + 1):
            lhex = "{:#08x}: ".format(k * row_sz)
            lhum = " |"
            d = data[k * row_sz:(k + 1) * row_sz]

            for i in range(0, col_num):
                lhex += " "

                for j in range(0, col_sz):
                    idx = i * col_sz + j
                    if idx < len(d):    # len(d) might be smaller than row_sz
                        c = d[idx]
                        lhex += "{:02x}".format(c)
                        lhum += Formatter.printable(c)
                    else:
                        lhex += " " * 2
                        lhum += " "

            if human:
                lhex += lhum + "|"
            lines.append(lhex)

        if max_lines > 1:
            if len(lines) > max_lines:
                ml = max_lines // 2
                lines = lines[0:ml] + ["[snip]"] + lines[-ml:]

        return lines

    @staticmethod
    def hexdump(data, col_sz=2, col_num=4, human=True, max_lines=10):
        '''[summary]

        Arguments:
            data {bytes or bytearray} -- [description]

        Keyword Arguments:
            col_sz {int} -- [description] (default: {2})
            col_num {int} -- [description] (default: {4})
            human {bool} -- [description] (default: {True})
            max_lines {int} -- [description] (default: {10})
        '''
        return "\n".join(Formatter.hexdump_lines(data,
                                                 col_sz, col_num,
                                                 human, max_lines))

    @staticmethod
    def hexdiff_lines(d1, d2, col_sz=2, col_num=4, human=True):
        '''[summary]

        Arguments:
            d1 {bytes or bytearray} -- First bytefield
            d2 {bytes or bytearray} -- Second bytefield

        Keyword Arguments:
            col_sz {int} -- [description] (default: {2})
            col_num {int} -- [description] (default: {4})
            human {bool} -- [description] (default: {True})
        '''
        lines = []

        if len(d1) != len(d2):
            LGR.error("d1 and d2 sizes differs => no diff returned.")
            return lines

        row_sz = col_sz * col_num
        r = len(d1) % row_sz

        for k in range(0, (len(d1) // row_sz) + 1):
            lhead = "{:#08x}: ".format(k * row_sz)
            l1hex = ""
            l2hex = ""
            l1hum = " |"
            l2hum = " |"

            sd1 = d1[k * row_sz:(k + 1) * row_sz]
            sd2 = d2[k * row_sz:(k + 1) * row_sz]

            for i in range(0, col_num):
                l1hex += " "
                l2hex += " "

                for j in range(0, col_sz):
                    idx = i * col_sz + j
                    if idx < len(sd1):  # len(sd1) might be smaller than row_sz
                        c1 = sd1[idx]
                        c2 = sd2[idx]

                        color = 'green' if c1 == c2 else 'red'

                        l1hex += colored("{:02x}".format(c1), color)
                        l1hum += colored(Formatter.printable(c1), color)
                        l2hex += colored("{:02x}".format(c2), color)
                        l2hum += colored(Formatter.printable(c2), color)
                    else:
                        l1hex += " " * 2
                        l1hum += " "
                        l2hex += " " * 2
                        l2hum += " "

            if human:
                l1hex += l1hum + "|"
                l2hex += l2hum + "|"

            sep = "\\" if (k+1) % 2 == 0 else "/"
            line = lhead + l1hex + sep + l2hex
            lines.append(line)

        return lines

    @staticmethod
    def hexdiff(d1, d2, col_sz=2, col_num=4, human=True):
        '''[summary]

        Arguments:
            d1 {bytes or bytearray} -- [description]
            d2 {bytes or bytearray} -- [description]

        Keyword Arguments:
            col_sz {int} -- [description] (default: {2})
            col_num {int} -- [description] (default: {4})
            human {bool} -- [description] (default: {True})
        '''
        return "\n".join(Formatter.hexdiff_lines(d1, d2,
                                                 col_sz, col_num,
                                                 human))

    @staticmethod
    def pretty_str(obj, indent=0):
        '''[summary]

        Arguments:
            obj {Typing.Any} -- [description]

        Keyword Arguments:
            indent {int} -- [description] (default: {0})
s
        Returns:
            str -- [description]
        '''
        text = ''
        indent_str = indent * Formatter.TAB

        if isinstance(obj, dict):
            for k, v in obj.items():
                text += "\n{}+ {}: {}".format(indent_str, k,
                                              Formatter.pretty_str(v,
                                                                   indent+1))

        elif isinstance(obj, list):
            k = 0
            for e in obj:
                text += "\n{}- [{}]: {}".format(indent_str, k,
                                                Formatter.pretty_str(e,
                                                                     indent+1))
                k += 1

        elif isinstance(obj, (bytes, bytearray)):
            lines = Formatter.hexdump_lines()
            for line in lines:
                text += '\n{}{}'.format(indent_str, line)
        else:
            text += '{}'.format(obj)

        return text

    @staticmethod
    def pretty_print(obj, indent=0):
        '''[summary]

        Arguments:
            obj {Typing.Any} -- [description]

        Keyword Arguments:
            indent {int} -- [description] (default: {0})
        '''
        print(Formatter.pretty_str(obj, indent))




