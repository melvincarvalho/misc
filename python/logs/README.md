Here are the things you need to know about python logging.

```
import os, sys
import logging

logging.info('logging at INFO')
```
Nothing!
```
logging.warn('logging at WARN')
> WARNING:root:logging at WARN
```
Now, how do I set the loglevel?
```
logging.setLevel(logging.INFO)
> Traceback (most recent call last):
>   File "<stdin>", line 1, in <module>
> AttributeError: 'module' object has no attribute 'setLevel'
```
What the ****???
logging.<func> are just convenience functions. If you read https://docs.python.org/2/library/logging.html closely you will see this. But who wants to read the documentation closely (until you are really frustrated..).
Just always do this (as a basic start):
```
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info('goo')
> INFO:root:goo
```

Q: But I want to log to a file.
Option1: Just redirect the logs that are written out to stderr to a file of your choosing. I always think this is the best. The process really doesn't need to know where logs are being written, etc.

But there are good reasons (such as if you are writing daemons, or servers) that you want the process to write to a file. Perhaps one that can be specified as an argument `--log-file` or some such.

```
handler = logging.FileHandler(os.getenv('MY_LOGFILE', '/tmp/log'))
logger.setHandler(handler)
logger.info('logging to a file!')
> logging to a file!
```
What?? Why did this get printed out?
```
!tail -1 /tmp/log
> logging to a file!
```
So it got printed out and went to the file.

```
logger.handlers
> [<logging.FileHandler at 0x10397ba10>, <logging.StreamHandler at 0x1039618d0>]
```
Ah! Note you *added* an handler. Nowhere in the docs does it say how to easily remove an existing handler. Or rather, how to see what handlers are there. But above is how.
So, if you really want to, you can remove the StreamHandler.
```
logger.removeHandler(logger.handlers[1])
logger.info('only logging to a file!')
> 
!tail -1 /tmp/log
> only logging to a file!
```



