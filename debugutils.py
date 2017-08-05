# -*- coding: UTF-8 -*-
# Copyright (c) 2017, Ling Wang<lingwangneuraleng@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
Created on 8/5/17-6:09 PM

@author: Ling Wang<lingwangneuraleng@gmail.com>

Add an additional logging level: DEBUGV
Provide stats_to_markdownstr()

"""

import logging

import pstats
import io
import tabulate

DEBUGV = 5 #verbose debug info


def debugv(self, message, *args, **kwds):
    if self.isEnabledFor(DEBUGV):
        self._log(DEBUGV, message, args, **kwds)

logging.addLevelName(DEBUGV, 'DEBUGV')
logging.Logger.debugv = debugv


def stats_to_markdownstr(p: pstats.Stats, prtRowNum: int) -> str:
    """convert pstats result to markdown table

    Args:
        p (pstats.Stats): pstats result
        prtRowNum (int): only print several functions

    Returns:
        str: the markdown string with table

    """
    s = io.StringIO()
    p.stream = s
    p.print_stats(prtRowNum)
    sumlines = []
    _line = ''
    flag = True
    fp = 0
    s.seek(0)
    while flag:
        fp = s.tell()
        _line = s.readline()
        _pl = _line.rstrip()
        flag = _line.find("   ncalls  tottime") != 0 and _line
        if _pl and flag:
            sumlines.append(_pl)
    s.seek(fp)  # rewind before table
    width, fncs = p.get_print_list((prtRowNum,))
    results = []
    for func in fncs:
        cc, nc, tt, ct, callers = p.stats[func]

        results.append((nc,
                        cc,
                        tt / nc,
                        ct,
                        ct / nc,
                        pstats.func_std_string(func)
                        )
                       )
    headers = ['ncalls',
               'pcalls',
               'tottime',
               'tt percall',
               'cumtime',
               'ct percall',
               'filename:lineno(function)'
               ]
    sumstr = '\n'.join(sumlines)
    tablestr = tabulate.tabulate(results,
                                 headers=headers,
                                 floatfmt='.3g',
                                 tablefmt='pipe')  # for markdown
    resultstr = sumstr + '\n' + tablestr
    return resultstr