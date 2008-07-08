
import logging

from twisted.python import reflect
from twisted.python.log import addObserver, removeObserver

def _safeFormat(fmtString, fmtDict):
    """
    Try to format the string C{fmtString} using C{fmtDict} arguments,
    swallowing all errors to always return a string.
    """
    # There's a way we could make this if not safer at least more
    # informative: perhaps some sort of str/repr wrapper objects
    # could be wrapped around the things inside of C{fmtDict}. That way
    # if the event dict contains an object with a bad __repr__, we
    # can only cry about that individual object instead of the
    # entire event dict.
    try:
        text = fmtString % fmtDict
    except KeyboardInterrupt:
        raise
    except:
        try:
            text = ('Invalid format string or unformattable object in log message: %r, %s' % (fmtString, fmtDict))
        except:
            try:
                text = 'UNFORMATTABLE OBJECT WRITTEN TO LOG with fmt %r, MESSAGE LOST' % (fmtString,)
            except:
                text = 'PATHOLOGICAL ERROR IN BOTH FORMAT STRING AND MESSAGE DETAILS, MESSAGE LOST'
    return text

def textFromEventDict(eventDict):
    """
    Extract text from an event dict passed to a log observer. If it cannot
    handle the dict, it returns None.

    The possible keys of eventDict are:
     - C{message}: by default, it holds the final text. It's required, but can
       be empty if either C{isError} or C{format} is provided (the first
       having the priority).
     - C{isError}: boolean indicating the nature of the event.
     - C{failure}: L{failure.Failure} instance, required if the event is an
       error.
     - C{why}: if defined, used as header of the traceback in case of errors.
     - C{format}: string format used in place of C{message} to customize
       the event. It uses all keys present in C{eventDict} to format
       the text.
    Other keys will be used when applying the C{format}, or ignored.
    """
    edm = eventDict['message']
    if not edm:
        if eventDict['isError'] and 'failure' in eventDict:
            text = ((eventDict.get('why') or 'Unhandled Error')
                    + '\n' + eventDict['failure'].getTraceback())
        elif 'format' in eventDict:
            text = _safeFormat(eventDict['format'], eventDict)
        else:
            # we don't know how to log this
            return
    else:
        text = ' '.join(map(reflect.safe_str, edm))
    return text

class PythonLoggingObserver(object):
    """
    Output twisted messages to Python standard library L{logging} module.

    WARNING: specific logging configurations (example: network) can lead to
    a blocking system. Nothing is done here to prevent that, so be sure to not
    use this: code within Twisted, such as twisted.web, assumes that logging
    does not block.
    """

    def __init__(self, loggerName="twisted"):
        """
        @param loggerName: identifier used for getting logger.
        @type loggerName: C{str}
        """
        self.logger = logging.getLogger(loggerName)

    def emit(self, eventDict):
        """
        Receive a twisted log entry, format it and bridge it to python.

        By default the logging level used is info; log.err produces error
        level, and you can customize the level by using the C{logLevel} key::

        >>> log.msg('debugging', logLevel=logging.DEBUG)

        """
        if 'logLevel' in eventDict:
            level = eventDict['logLevel']
        elif eventDict['isError']:
            level = logging.ERROR
        else:
            level = logging.INFO
        text = textFromEventDict(eventDict)
        if text is None:
            return
        self.logger.log(level, text)

    def start(self):
        """
        Start observing log events.
        """
        addObserver(self.emit)

    def stop(self):
        """
        Stop observing log events.
        """
        removeObserver(self.emit)
