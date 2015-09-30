#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import random

read_interval = 10

def conf(cfg):
    global read_interval
    
    collectd.info("conf(%s)" % cfg) # a config root node
    for node in cfg.children:
        collectd.info("conf: %s = %s" % (node.key, node.values[0]))
        if node.key == "MyInterval":
            read_interval = int(node.values[0])
            
def init():
    collectd.info("MyInterval = %s" % read_interval)
    collectd.register_read(read, interval=read_interval)

def read(data=None):
    vl = collectd.Values(type='gauge')
    vl.plugin='python.test'
    
    my_val = random.random() * 100
    collectd.info("dispatch(%f)" % my_val)
    vl.dispatch(values=[my_val]) # dispatch to collectd and its registered write functions
    
if __name__ == '__main__':
    pass
else:
    import collectd
    
    collectd.register_config(conf)
    collectd.register_init(init)
    
    # callback execution sequence: conf() -> init() -> read()
    
    