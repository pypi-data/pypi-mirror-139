
""" General purpose utility library. """

__author__ = 'Niklas Rosenstein <rosensteinniklas@gmail.com>'
__version__ = "0.6.6"

from ._chaindict import ChainDict
from ._optional import Optional
from ._orderedset import OrderedSet
from ._refreshable import Refreshable
from ._stream import Stream

__all__ = ['ChainDict', 'coalesce', 'Optional', 'OrderedSet', 'Refreshable', 'Stream']


from .functional._coalesce import coalesce
from deprecated import deprecated
coalesce = deprecated('use `nr.util.functional.coalesce()` instead')(coalesce)
