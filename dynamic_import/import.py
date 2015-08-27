
print "imported as %s\n" % __name__

import os, sys
import imp
import pkgutil # since python 2.3
# import importlib # since python 2.7

import_entries = {
    'g_time': {'from': 'time', 'import': 'time', 'as': 'g_time'}, # from time import time as g_time
    'g_gmtime': {'from': 'time', 'import': 'gmtime', 'as': 'g_gmtime'}, # from time import gmtime as g_gmtime
}

# dynamic import
for key, entry in import_entries.iteritems():
    try:
        _m_ = __import__(entry['from'], fromlist=[entry['import']])
        globals()[entry['as']] = getattr(_m_, entry['import'])
    except ImportError as ex:
        print ex
    else:
        print globals()[entry['as']]()

def foo():
    import_entries = [
        {'from': 'time', 'import': 'time', 'as': 'l_time'}, # from time import time as l_time
        {'from': 'time', 'import': 'gmtime', 'as': 'l_gmtime'}, # from time import gmtime as l_gmtime
    ]
    
    # dynamic import
    for entry in import_entries:
        try:
            _m_ = __import__(entry['from'], fromlist=[entry['import']])
            locals()[entry['as']] = getattr(_m_, entry['import'])
        except ImportError as ex:
            print ex
        else:
            print locals()[entry['as']]()

if __name__ == '__main__':

    foo()

    #print dir(list)
    #print dir(dict)
    
    # pkgutil: check if module installed
    pkg = pkgutil.find_loader('time.zzz')
    print pkg
    
    # imp: check if module installed
    try:
        imp.find_module('time.zzz')
        found = True
    except ImportError:
        found = False
    finally:
        print found
    
    # pkgutils.itermodules(): list if module installed
    for loader, name, ispkg in pkgutil.iter_modules():
        #print (loader, name, ispkg)
        pass
        
    # sys.modules: list if module is imported/loaded
    print sys.path # list python lookup path
    for key, val in sys.modules.iteritems():
        #print (key, val)
        pass
    
