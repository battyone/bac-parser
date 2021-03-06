import csv, codecs
try:
    from cStringIO import StringIO  # CPython 2.x
except ImportError:
    try:
        from StringIO import StringIO # possibly other interpretors
    except ImportError:
        from io import StringIO # Python 3
import os
import sys

from gzip import GzipFile
from bz2 import BZ2File
COMPRESSED_FILE_CLASSES = {'.gz': GzipFile,
                           '.bz2': BZ2File}
try:
    from lzma import LZMAFile
    COMPRESSED_FILE_CLASSES['.xz'] = LZMAFile
except ImportError:
    pass

def open_compressed_file(filename):
    """Open a possibly compressed file. '-' stands for stdin"""
    global COMPRESSED_FILE_CLASSES

    if filename == '-':
        return sys.stdin
    ext = os.path.splitext(filename)[1]
    f = COMPRESSED_FILE_CLASSES.get(ext, open)(filename)
    dir(f) # workaround for https://bugzilla.redhat.com/show_bug.cgi?id=720111
    return f


# taken from http://docs.python.org/library/csv.html
class UnicodeWriter: # TODO make it work in Python 3
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
