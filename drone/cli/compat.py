import sys

_ver = sys.version_info

#: Python 2.x
is_py2 = (_ver[0] == 2)

#: Python 3.x
is_py3 = (_ver[0] == 3)


if is_py2:
    try:
        from backports import tempfile
    except ImportError:
        print '\nPlease install the required backports.tempfile dependency ' \
              'via: \npip install backports.tempfile\n\n'
    from urllib2 import urlopen
    input = raw_input

elif is_py3:
    import tempfile
    from urllib.request import urlopen
    input = input
