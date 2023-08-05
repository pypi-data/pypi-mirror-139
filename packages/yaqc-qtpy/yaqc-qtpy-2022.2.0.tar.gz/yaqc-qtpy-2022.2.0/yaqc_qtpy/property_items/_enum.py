__all__ = ["Enum"]


import time
from functools import partial

import qtypes


def options_updated(value, item):
    item.set({"allowed": value})


def value_updated(value, item):
    item.set({"value": value})


def set_daemon(value, property):
    property(value["value"])


def Enum(key, property, qclient):
    # disabled
    if property._property.get("setter", None):
        disabled = False
    else:
        disabled = True
    # make item
    item = qtypes.Enum(disabled=disabled, label=key)
    # signals and slots
    property.updated.connect(partial(value_updated, item=item))
    property()
    property.options.finished.connect(partial(options_updated, item=item))
    property.options()
    item.edited.connect(partial(set_daemon, property=property))
    return item
