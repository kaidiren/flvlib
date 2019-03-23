import sys
import logging

from optparse import OptionParser

from flvlib import __versionstr__
from flvlib import tags
from flvlib import helpers
from flvlib.astypes import MalformedFLV

log = logging.getLogger('flvlib.fix-flv')
log.setLevel(logging.ERROR)


def fix_flv(filename, quiet=False, metadata=False):
    try:
        f = open(filename, 'rb')
    except IOError, (strerror):
        log.error("Failed to open `%s': %s", filename, strerror)
        return False

    flv = tags.FLV(f)

    if not quiet:
        print "=== `%s' ===" % filename
    offset = 0
    try:
        tag_generator = flv.iter_tags()
        for i, tag in enumerate(tag_generator):
            offset = tag.offset
            if quiet:
                # If we're quiet, we just want to catch errors
                continue
            # Print the tag information
            print "#%05d %s" % (i + 1, tag)
            # Print the content of onMetaData tags
            if (isinstance(tag, tags.ScriptTag)
                and tag.name == "onMetaData"):
                helpers.pprint(tag.variable)
                if metadata:
                    return True
    except MalformedFLV, e:
        message = e[0] % e[1:]
        log.error("The file `%s' is not a valid FLV file: %s",
                  filename, message)
        return False, offset
    except tags.EndOfFile:
        #log.error("Unexpected end of file on file `%s'", filename)
        return True, offset

    f.close()

    return False, offset
