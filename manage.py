#!/usr/bin/env python
import sys
import logging
try:
    from halicea import hal
    print "Hal web is not located in your python path"
except:
    print "accessing halweb thru path /home/costa/DevApps/halicea"
    sys.path.append("/home/costa/DevApps/halicea")
    import hal
if __name__=='__main__':
    hal.main_safe(sys.argv)
