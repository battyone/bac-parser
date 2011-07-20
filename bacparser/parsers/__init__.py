from .. import BacParserUnsupportedYear
from .parser2006 import Parser2006
from .parser2007 import Parser2007
from .parser2009 import Parser2009
from .parser2010 import Parser2010

SUPPORTED_YEARS = range(2006, 2011+1)

def get_parser(year):
    if year > 2011:
        raise BacParserUnsupportedYear('Unsupported year')
    if year >= 2010:
        return Parser2010
    if year >= 2009:
        return Parser2009
    if year >= 2007:
        return Parser2007
    if year >= 2006:
        return Parser2006
    # year < 2006
    raise BacParserUnsupportedYear('Unsupported year')