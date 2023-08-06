from datetime import datetime
import logging
from collections import OrderedDict
import uuid
import time
from contextlib import contextmanager
from rdflib import Namespace
from brickschema.namespaces import BRICK, A
from rdflib import Graph, ConjunctiveGraph
from rdflib.graph import BatchAddGraph
from rdflib import plugin
from rdflib.store import Store
from rdflib_sqlalchemy import registerplugins
import pickle
from .graph import Graph


class PersistentGraph(Graph):
    def __init__(self, store, *args, **kwargs):
        super().__init__("SQLAlchemy", *args, **kwargs)
        super().open(store **kwargs)
        self.store = store
        super()._graph_init()
