__author__ = "Patrick Godwin (patrick.godwin@ligo.org)"
__description__ = "a module for client utilities"

#-------------------------------------------------
### imports

from collections import namedtuple

from . import utils
from .io import influx


#-------------------------------------------------
### classes

class Client(object):
    """A general-purpose client to write and query time-based metrics.

    Parameters
    ----------
    uri : `str`
        the URI to connect to, in the form: protocol://host:port
    auth :
        if specified, use authentication
    config : `str`
        if specified, load schemas from config

    """
    def __init__(self, uri, auth=None, config=None):
        self.uri = utils.uriparse(uri)
        self.auth = auth

        ### set up client
        if self.uri.protocol == 'influx':
            self._client = influx.create_client(
                host=self.uri.hostname,
                port=self.uri.port,
                auth=self.auth
            )

        ### set up schema store
        self._schema = {}


    def register(self, name, schema):
        """Registers a schema by name for performing writes and queries.

        Parameters
        ----------
        name : `str`
            the schema name
        schema : `Schema`
            the schema to register

        """

    def write(self, schema, **kwargs):
        """Writes data to a datastore corresponding to a schema.

        Parameters
        ----------
        schema : `str` or `Schema`
            the schema to write data to
        **kwargs
            named data columns to store
         
        """

    def query(self, schema, start=None, end=None, limit=None, **kwargs):
        """Query a datastore for data corresponding to a schema.

        Parameters
        ----------
        schema : `str` or `Schema`
            the schema to query
        start : `int`
            if specified, the start time
        end : `int`
            if specified, the end time
        limit : `int`
            if specified, limit to N rows

        Returns
        -------
        `namedtuple`
            columns and/or tags, accessed by name

        """

InfluxSchema = namedtuple('InfluxSchema', 'database measurement columns tags aggregate dt')
