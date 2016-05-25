Here are the things you need to know about python logging.

```
import os, sys
import logging

logging.info('logging at INFO')
```
Nothing!
```
logging.warn('logging at WARN')
WARNING:root:logging at WARN
```
Now, how do I set the loglevel?
```
logging.setLevel(logging.INFO)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'module' object has no attribute 'setLevel'
```
What the ****???
logging.<func> are just convenience functions. If you read https://docs.python.org/2/library/logging.html closely you will see this. But who wants to read the documentation closely (until you are really frustrated..).
Just always do this (as a basic start):
```
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info('goo')
INFO:root:goo
```

```
