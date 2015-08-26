#!/usr/bin/env python

from tasks import add

result = add.delay(2,3)
print result.ready()
print result.get(timeout=10)
print result.ready()
