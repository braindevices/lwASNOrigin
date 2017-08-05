# Overview

This small project  demonstrates several issues in ASNOrigin of current ipwhois package.

# Structure Issues

## The ASNOrigin initiation should not require Net object

The ASN origin lookup does not require any IP or network parameter. Thus the ASNOrigin should not require this. However, in current code, we have to initiate an ASNOrigin object by passing a Net object. It can be any Net object which is completely irrelevant to target ASN. So it is very confusing. The only reason, that the current code has it, is because it requires several member methods from Net class.

## The ASN lookup related functions should not be in net.py at all.

As we said before the ASN lookup has nothing to do with IP/network, thus the get_asn_origin_whois and get_htp_raw should not located in net.py as member methods. The only resources shared in Net class is timeout and the proxy_opener, which can easily be passed as arguments.

## The ASNOrigin may not be class at all.

Since the only shared member in ASNOrigin class is the useless/unwanted Net object. After we move the needed functions out, we can avoid define the ASNOrigin as class. The entire thing will be much more clear.

# Other bugs

## the ASNOrigin.lookup()

### successful query does not stop looping through all asn_methods

One would expect avoiding `http` method if the `whois` method works. However, the current code repeats the lookup query with `get_http_raw()`. Thus it slows down the process dramatically (normally 2-4 times slower than os `whois` command)
 
# test results

* Use ipwhois stable version:
 
    > 59857 function calls (58068 primitive calls) in 3.505 seconds 
    >>   Ordered by: cumulative time
    
    >>   List reduced from 428 to 10 due to restriction <10>

    |   ncalls |   pcalls |   tottime |   tt percall |   cumtime |   ct percall | filename:lineno(function)                        |
    |---------:|---------:|----------:|-------------:|----------:|-------------:|:-------------------------------------------------|
    |        2 |        1 |  0.000433 |     0.000216 |      3.5  |     1.75     | {built-in method builtins.exec}                  |
    |        1 |        1 |  3.1e-05  |     3.1e-05  |      3.5  |     3.5      | test_asnoriginlookup.py:76(test2)                |
    |        1 |        1 |  1.5e-05  |     1.5e-05  |      3.5  |     3.5      | test_asnoriginlookup.py:57(getAllroutesOld)      |
    |        1 |        1 |  0.000458 |     0.000458 |      3.49 |     3.49     | asn.py:779(lookup)                               |
    |        1 |        1 |  3.4e-05  |     3.4e-05  |      2.35 |     2.35     | net.py:866(get_http_raw)                         |
    |       29 |       29 |  0.000151 |     5.21e-06 |      1.72 |     0.0594   | socket.py:572(readinto)                          |
    |       29 |       29 |  1.72     |     0.0594   |      1.72 |     0.0594   | {method 'recv_into' of '_socket.socket' objects} |
    |        1 |        1 |  1.3e-05  |     1.3e-05  |      1.5  |     1.5      | client.py:438(read)                              |
    |        1 |        1 |  0.00298  |     0.00298  |      1.5  |     1.5      | client.py:558(_readall_chunked)                  |
    |     2716 |     2716 |  0.00732  |     2.7e-06  |      1.49 |     0.000547 | client.py:596(_safe_read)                        |


* After moving `get_asn_origin_whois()` and `get_http_raw()` out from ipwhois.net.Net, I also make ASNOrigin as a module instead of class. It works now. Also fixed the `asn_methods` bug. The speed is about 2-3 times faster than stable version.

    >29395 function calls (27629 primitive calls) in 0.822 seconds
    >>   Ordered by: cumulative time
    
    >>   List reduced from 339 to 10 due to restriction <10>

    |   ncalls |   pcalls |   tottime |   tt percall |   cumtime |   ct percall | filename:lineno(function)                      |
    |---------:|---------:|----------:|-------------:|----------:|-------------:|:-----------------------------------------------|
    |        1 |        1 |  4.4e-05  |     4.4e-05  |   0.822   |     0.822    | {built-in method builtins.exec}                |
    |        1 |        1 |  3.8e-05  |     3.8e-05  |   0.822   |     0.822    | <string>:1(<module>)                           |
    |        1 |        1 |  3.3e-05  |     3.3e-05  |   0.822   |     0.822    | test_asnoriginlookup.py:66(test1)              |
    |        1 |        1 |  7e-06    |     7e-06    |   0.812   |     0.812    | test_asnoriginlookup.py:42(getAllroutes)       |
    |        1 |        1 |  0.000564 |     0.000564 |   0.804   |     0.804    | ASNOrigin.py:418(lookup)                       |
    |        1 |        1 |  0.000294 |     0.000294 |   0.783   |     0.783    | ASNOrigin.py:72(get_asn_origin_whois)          |
    |       15 |       15 |  0.521    |     0.0347   |   0.521   |     0.0347   | {method 'recv' of '_socket.socket' objects}    |
    |        1 |        1 |  0.261    |     0.261    |   0.261   |     0.261    | {method 'connect' of '_socket.socket' objects} |
    |      140 |      140 |  0.00536  |     3.83e-05 |   0.012   |     8.57e-05 | ASNOrigin.py:290(parse_fields)                 |
    |        1 |        1 |  6e-06    |     6e-06    |   0.00919 |     0.00919  | pprint.py:47(pprint)                           |

* When using `add_query_params='-K -T route'` The database only returns primary keys and ipv4. This is much faster than getting entire object from RADB.

    >19290 function calls (17934 primitive calls) in 0.511 seconds
    
    >>   Ordered by: cumulative time
    
    >>   List reduced from 181 to 10 due to restriction <10>
    
    |   ncalls |   pcalls |   tottime |   tt percall |   cumtime |   ct percall | filename:lineno(function)                      |
    |---------:|---------:|----------:|-------------:|----------:|-------------:|:-----------------------------------------------|
    |        1 |        1 |  5.3e-05  |     5.3e-05  |   0.511   |     0.511    | {built-in method builtins.exec}                |
    |        1 |        1 |  2.9e-05  |     2.9e-05  |   0.511   |     0.511    | <string>:1(<module>)                           |
    |        1 |        1 |  2e-05    |     2e-05    |   0.511   |     0.511    | test_asnoriginlookup.py:71(test1b)             |
    |        1 |        1 |  9e-06    |     9e-06    |   0.505   |     0.505    | test_asnoriginlookup.py:42(getAllroutes)       |
    |        1 |        1 |  0.000388 |     0.000388 |   0.497   |     0.497    | ASNOrigin.py:418(lookup)                       |
    |        1 |        1 |  0.000123 |     0.000123 |   0.487   |     0.487    | ASNOrigin.py:72(get_asn_origin_whois)          |
    |        1 |        1 |  0.243    |     0.243    |   0.243   |     0.243    | {method 'connect' of '_socket.socket' objects} |
    |        4 |        4 |  0.243    |     0.0608   |   0.243   |     0.0608   | {method 'recv' of '_socket.socket' objects}    |
    |        1 |        1 |  0.000144 |     0.000144 |   0.00793 |     0.00793  | test_asnoriginlookup.py:54(<listcomp>)         |
    |      113 |      113 |  0.000176 |     1.56e-06 |   0.00779 |     6.89e-05 | ipaddress.py:57(ip_network)                    |
