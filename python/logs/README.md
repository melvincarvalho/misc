Guide to python logging using logging.

You are writing some python, and you want to get beyond print to use some type of logging.

The first section here deals with your first steps to using logging. Subsequent sections will deal with servers and libraries. Note that some of the suggestions in the first section are not be suitable for logging in servers and libraries.

## First look at logging

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
logger.setLevel(int(os.getenv('MY_LOGLEVEL',20)))
```
Import mylogging.py everywhere (or in some top level __init__.py file), and just use logger.[debug|info|warn|error] all over your code, and control the loglevel by using MY_LOGLEVEL env var. You are done.

Go away now if you don't want to waste any more time with logging. Just do the above until you *need* to read on.

### I want to format my logs: RTFM (for now I am not delving in this - you got some text right?)

### I want to log to a file.
Option1: Just redirect the logs that are written out to stderr to a file of your choosing. I always think this is the best. The process really doesn't need to know where logs are being written, etc. Especially if you're just writing some stand-alone script - just let the user decide using standard redirections of stderr stream. Don't make decisions about "I will overwrite the logfile given to me / I will append" etc etc.

But there are good reasons (such as if you are writing daemons, or servers) that you want the process to write to a file. Perhaps one that can be specified as an argument `--log-file` or some such.

First, lets just make sure we can make logging write to a file. Now, if you do below, you may get something like:
```
logger = logging.getLogger()
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

This is probably because you somehow have multiple handlers set up on your root logger. If you don't get anything printed out, just to file, then you didn't have the extra handler set up.

If you do, you can look at what handlers are set up.
```
logger.handlers
> [<logging.FileHandler at 0x10397ba10>, <logging.StreamHandler at 0x1039618d0>]
```
Ah! Note you *added* an handler. Nowhere in the docs does it say how to easily remove an existing handler. Or rather, how to see what handlers are there. But above is how.
So, you can remove the StreamHandler. Of course, best is to never create it. But remember, using some convenience functions `logging.<func>` will under the hood create this handler.
```
logger.removeHandler(logger.handlers[1])
logger.info('only logging to a file!')
> 
!tail -1 /tmp/log
> only logging to a file!
```

## Logging from a server

If you are writing a server, you want to rotate the server logs. You can't really do this if you are redirecting stderr. Try it:
test.py:
```
import sys, os
import time

print "starting"
while True:
    print >> sys.stderr, "the time is now %s" % (time.time(),)
    time.sleep(1)
print "done"
```

Then
```
python test.py 2> /tmp/log &
mv /tmp/log /tmp/log.1
tail -f /tmp/log.1
```
Of course, the process you started will still keep writing to the underlying file which now you called /tmp/log.1. And you can't (easily at least, I guess anything is possible with enough bit twidlling) make it stop, without killing the process.

So you want to write to a file which you can rotate (i.e. take all the logs at a point in time, move them to some other file, or copy them and truncate this file so it doesn't keep getting bigger, all while letting the process keep logging to the file, and of course not lose anything). This is logrotate - read about it elsewhere.

One way logrotate is done by many servers (I believe by mysql / postgres and possibly apache? do this), you send the process a signal (HUP), they handle this signal by doing, amongst other things, closing the log filehandle they are writing to, and reopening it. So the sequence is `mv /tmp/log /tmp/log.<datetime>; kill -HUP <pid>;` and now the process will reopen (and recreate /tmp/log and log to this new file.

I'm guessing there is a way to make logging do this - possibly by getting the FileHandler that it is using, and closing and reopening the file and giving the new filehandle back or some such). But logger provides a easier way to do this.

#### logging.handlers.WatchedFileHander
https://docs.python.org/2/library/logging.handlers.html#module-logging.handlers

```
import logging
import logging.handlers

logger = logging.getLogger()
handler = logging.handlers.WatchedFileHandler('/tmp/log')
logger.addHandler(handler)
```
Read the docs on WatchedFileHandler to see how it works, but it does exactly what we want. I think in some ways this is better than the RotatingFileHandler, because it lets you use logrotate to control the logrotation and backup, vs having it controlled by the python process.

### Logging within multi-threaded apps.
The logging documentation says loggers are thread-safe, I don't have much more to add here.

### Logging within multi-process apps.







