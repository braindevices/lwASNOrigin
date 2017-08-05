#Overview

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

### successful query will not stop looping through all asn_methods

One would expect avoiding `http` method if the `whois` method works. However, the current code will repeat the lookup query with `get_http_raw()`. Thus it slow down the process dramatically.
 
# test results

* Use ipwhois stable version:
 
    > 59868 function calls (58079 primitive calls) in 8.768 seconds
    >>   Ordered by: cumulative time
    
    >>   List reduced from 428 to 10 due to restriction <10>

    |   ncalls |   pcalls |   tottime |   tt percall |   cumtime | ct percall                                  |
    |---------:|---------:|----------:|-------------:|----------:|:--------------------------------------------|
    |        2 |        1 |  0.000226 |         8.77 |      4.38 | {built-in method builtins.exec}             |
    |        1 |        1 |  3.4e-05  |         8.77 |      8.77 | test_asnoriginlookup.py:33(test2)           |
    |        1 |        1 |  1.6e-05  |         8.76 |      8.76 | test_asnoriginlookup.py:21(getAllroutesOld) |
    |        1 |        1 |  0.000555 |         8.75 |      8.75 | asn.py:779(lookup)                          |
    |        1 |        1 |  7.5e-05  |         7.3  |      7.3  | net.py:866(get_http_raw)                    |
    |        1 |        1 |  2.7e-05  |         5.83 |      5.83 | request.py:508(open)                        |
    |        1 |        1 |  5e-06    |         5.83 |      5.83 | request.py:536(_open)                       |
    |        2 |        2 |  3e-06    |         5.83 |      2.91 | request.py:497(_call_chain)                 |
    |        1 |        1 |  6e-06    |         5.83 |      5.83 | request.py:1345(http_open)                  |
    |        1 |        1 |  5.3e-05  |         5.83 |      5.83 | request.py:1276(do_open)                    |

* After moving `get_asn_origin_whois()` and `get_http_raw()` out from ipwhois.net.Net, I also make ASNOrigin as a module instead of class. It works now. Also fixed the `asn_methods` bug.

    >53021 function calls (51514 primitive calls) in 4.161 seconds
    >>   Ordered by: cumulative time
    
    >>   List reduced from 339 to 10 due to restriction <10>

    |   ncalls |   pcalls |   tottime |   tt percall |   cumtime | ct percall                                       |
    |---------:|---------:|----------:|-------------:|----------:|:-------------------------------------------------|
    |        1 |        1 |  4.3e-05  |         4.16 |    4.16   | {built-in method builtins.exec}                  |
    |        1 |        1 |  3.3e-05  |         4.16 |    4.16   | <string>:1(<module>)                             |
    |        1 |        1 |  2.7e-05  |         4.16 |    4.16   | test_asnoriginlookup.py:29(test1)                |
    |        1 |        1 |  7e-06    |         4.16 |    4.16   | test_asnoriginlookup.py:17(getAllroutes)         |
    |        1 |        1 |  0.000638 |         4.15 |    4.15   | ASNOrigin.py:408(lookup)                         |
    |        1 |        1 |  5.3e-05  |         2.97 |    2.97   | ASNOrigin.py:181(get_http_raw)                   |
    |       23 |       23 |  6.04e-06 |         2.2  |    0.0957 | socket.py:572(readinto)                          |
    |       23 |       23 |  0.0957   |         2.2  |    0.0957 | {method 'recv_into' of '_socket.socket' objects} |
    |        1 |        1 |  2.9e-05  |         1.91 |    1.91   | client.py:438(read)                              |
    |        1 |        1 |  0.00321  |         1.91 |    1.91   | client.py:558(_readall_chunked)                  |

* When using `add_query_params='-K -T route'` The whois only return primary keys and ipv4. This is must faster than getting entire object from RADB.

    >22394 function calls (20952 primitive calls) in 0.857 seconds
    
    >>   Ordered by: cumulative time
    
    >>   List reduced from 181 to 10 due to restriction <10>
    
    |   ncalls |   pcalls |   tottime |   tt percall |   cumtime | ct percall                                     |
    |---------:|---------:|----------:|-------------:|----------:|:-----------------------------------------------|
    |        1 |        1 |  4.2e-05  |      0.857   |  0.857    | {built-in method builtins.exec}                |
    |        1 |        1 |  3.1e-05  |      0.857   |  0.857    | <string>:1(<module>)                           |
    |        1 |        1 |  1.8e-05  |      0.857   |  0.857    | test_asnoriginlookup.py:46(test1b)             |
    |        1 |        1 |  7e-06    |      0.85    |  0.85     | test_asnoriginlookup.py:17(getAllroutes)       |
    |        1 |        1 |  0.00047  |      0.843   |  0.843    | ASNOrigin.py:415(lookup)                       |
    |        1 |        1 |  0.000149 |      0.828   |  0.828    | ASNOrigin.py:72(get_asn_origin_whois)          |
    |        1 |        1 |  0.573    |      0.573   |  0.573    | {method 'connect' of '_socket.socket' objects} |
    |        4 |        4 |  0.0636   |      0.254   |  0.0636   | {method 'recv' of '_socket.socket' objects}    |
    |      113 |      113 |  1.73e-05 |      0.00753 |  6.67e-05 | ASNOrigin.py:287(parse_fields)                 |
    |        1 |        1 |  0.00078  |      0.00732 |  0.00732  | ASNOrigin.py:354(get_nets_radb)                |
