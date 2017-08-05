#!/usr/bin/env python
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
Created on 8/5/17-3:17 PM

@author: Ling Wang<lingwangneuraleng@gmail.com>

"""
import os
import pprint
import io
import ASNOrigin
import ipaddress
import cProfile, pstats

from debugutils import stats_to_markdownstr


def getAllroutes(asn, add_query_params=''):
    """obtain all possible routes of a target ASN.

    Args:
        asn (str): target ASN with or without "AS"
        add_query_params (:obj:`str`, optional): additional RIPE query flags from ASN lookup

    Returns:
        list: the list of CIDRs
    """
    #ipaddress.IPv4Network, ipaddress.IPv6Network
    results = ASNOrigin.lookup(asn, add_query_params=add_query_params)
    return [ipaddress.ip_network(_net['cidr']) for _net in results['nets']]


def getAllroutesOld(asn):
    from ipwhois.net import Net
    from ipwhois.asn import ASNOrigin as ASNOriginCls
    net = Net('108.160.160.0')
    obj = ASNOriginCls(net)
    results = obj.lookup(asn)
    return [ipaddress.ip_network(_net['cidr']) for _net in results['nets']]


def test1():
    cidrs = getAllroutes('19679')
    pprint.pprint(cidrs)


def test1b():
    cidrs = getAllroutes('19679', '-K -T route')
    pprint.pprint(cidrs)


def test2():
    cidrs = getAllroutesOld('19679')
    pprint.pprint(cidrs)


def runtest(testFn, prtRowNum = 10):
    """Run target test.

    Args:
        testFn (str): test name
    """
    testResult = '/tmp/{}_stats.dat'.format(testFn)
    if not os.path.isfile(testResult):
        cProfile.run(testFn + "()", testResult)


    # p = pstats.Stats(testResult, stream=s)
    p = pstats.Stats(testResult)
    p.strip_dirs()  # this should be before sort, otherwise it will reset the order
    p.sort_stats('cumtime')
    resultstr = stats_to_markdownstr(p, prtRowNum)
    print(resultstr)
    return resultstr





def main():
    import logging, debugutils
    # logging.basicConfig(level=debugutils.DEBUGV)
    logging.basicConfig(level=logging.DEBUG)
    testFns = ["test2", "test1", "test1b"]
    for _test in testFns:
        runtest(_test)


if __name__ == '__main__':
    main()
