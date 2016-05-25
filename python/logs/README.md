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
Just always do this (as a basic start)
(Also before doing below, kill the current python shell and start a new shell, the previous commands have polluted your logging as you will see.):
```
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info('foo')
> INFO:root:foo
```
All is well in the world.
But next time you start a new python shell (try it), and you happen to do:
```
logger = logging.getLogger()
logger.warn('bar')
> No handlers could be found for logger "root"
```
What??? What handlers? I didn't set any handlers last time and it printed out the log fine!
So... this is a great example of messing up the users mental model of how something works by trying to create shortcuts. When logging.info('logging at INFO') was called, this under the hood created StreamHandler (by calling basicConfig... more on this later). But the second time, I didn't call logging.info (or logging.warn etc) and so this was not created.

(The nice thing is all the source code is available in your install (`help(logging)` to see where the library is installed).)

It gets somewhat worse, because if you continue to test:
```
logger.warn('please log')
> 
logger.info('what is going on??')
>
```
Now you don't see any errors about handlers etc. So what exactly is going on?? Are there handlers? Are there logs? Should I just use print??

Unfortunately, the logging module suppresses printing out the error message 'No handlers could be found for logger "root"' after it has printed it out once. This is really bad and really makes the user have no idea what may be going on. But, internally, there are no spoons, I mean handlers.

Ok lets create a handler always and move ahead in life.
```
logger = logging.getLogger()
hander = logging.StreamHandler()
logger.addHandler(handler)
logger.warn('foo')
> foo
logger.info('bar')
>
```
Ok this is better, although you notice that logging just printed 'foo' and not 'INFO:root:foo' as previously. Well this is because under the hood logging also created a default formatter, which you have not. Lets leave that... right now all we want is to get some logs to happen, damnit!

```
logger.setLevel(logging.INFO)
logger.info('baz')
> baz
```

You can declare victory at this point, because right now, without further spending time on this, you can basically get a *lot* of the necessities of life (or logging) by just doing this in your python code.

Create a file mylogging.py
```
import logging
logger = logging.getLogger()
_handler = logging.StreamHander()
logger.addHandler(_handler)
logger.setLevel(os.getenv('MY_LOGLEVEL',20))
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



