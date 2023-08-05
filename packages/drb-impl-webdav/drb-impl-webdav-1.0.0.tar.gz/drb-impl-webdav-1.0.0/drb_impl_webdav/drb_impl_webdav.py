import io
from typing import Any, Optional, List, Dict, Tuple
from drb import AbstractNode, DrbNode
from drb.exceptions import DrbException, DrbNotImplementationException
from drb.path import ParsedPath
from requests.auth import AuthBase, HTTPBasicAuth
from webdav3.client import Client
from webdav3.urn import Urn

from drb_impl_webdav.utility_auth import CertAuth, TokenAuth


class Download(io.BytesIO):

    def __init__(self, path: str, webdav: Client):
        self._buff = bytearray(0)
        self._webdav = webdav
        self.__res = self._webdav.execute_request(
            'download',
            Urn(path).quote()
        )
        self._iter = None
        super().__init__(self.__res.content)

    def __init_generator(self):
        self._iter = self.__res.iter_content(self._webdav.chunk_size)

    def read(self, *args, **kwargs):
        if not (len(args) > 0 and isinstance(
                args[0],
                int
        ) and args[0] > 0):
            with self.__res as resp:
                return resp.content
        if self._iter is None:
            self.__init_generator()
        try:
            self._buff.extend(bytearray(next(self._iter)))
            res = self._buff[0:args[0]]
            del (self._buff[0:args[0]])
            return res
        except StopIteration:
            if len(self._buff) > 0:
                if args[0] < len(self._buff):
                    res = self._buff[0:args[0]]
                    del (self._buff[0:args[0]])
                    return res
                else:
                    return self._buff
            else:
                return bytes(0)

    def close(self) -> None:
        super().close()
        self.__res.close()


class WebdavConnection:
    # TODO: Check If you cannot do with another methods !
    webdav = None

    def __new__(cls, options: dict, auth: AuthBase):
        if cls.webdav is None or cls.webdav.get_url(
                cls.webdav.root
        ) != options.get('webdav_hostname'):
            if isinstance(auth, HTTPBasicAuth):
                options['webdav_login'] = auth.username
                options['webdav_password'] = auth.password
            elif isinstance(auth, CertAuth):
                options['webdav_login'] = auth.username
                options['webdav_password'] = auth.password
                options['cert_path'] = auth.cert_path
                options['key_path'] = auth.key_path
            elif isinstance(auth, TokenAuth):
                options['webdav_token'] = auth.token

            cls.webdav = Client(options)

        return cls.webdav

    def quit(self):
        self.webdav = None


class DrbWebdavNode(AbstractNode):
    """
    Drb node to access webdav server

    Parameters:
         webdav_hostname: url for WebDAV server should contain protocol
                          and ip address or domain name.
         webdav_login: (optional) Login name for WebDAV server.
                       Can be empty when using token auth.
         webdav_password: (optional) Password for WebDAV server.
                          Can be empty when using token auth.
         webdav_token: (optional) Authentication token for WebDAV server.
                       Can be empty when using login/password auth.
         webdav_root: (optional) Root directory of WebDAV server.
                      Default is `/`.
         webdav_cert_path: (optional) Path to client certificate.
         webdav_key_path: (optional) Path to private key of the client
                          certificate.
         webdav_recv_speed: (optional) Rate limit of data download speed in
                            Bytes per second, defaults to unlimited speed.
         webdav_send_speed: (optional) Rate limit of data upload speed
                            in Bytes per second. Defaults to unlimited speed.
         webdav_timeout: (optional) Timeout in seconds used in HTTP connection
                         managed by requests, defaults to 30 seconds.
         webdav_verbose: (optional) Set verbose mode on/off. By default
                         verbose mode is off.

    """

    def __init__(self, webdav_hostname: str, auth: AuthBase = None, **kwargs):
        super().__init__()
        if 'options' in kwargs.keys():
            self.options = kwargs.get('options')
        else:
            self.options = {
                'webdav_hostname': webdav_hostname,
                'webdav_root': kwargs.get('webdav_root', None),
                'webdav_recv_speed': kwargs.get('webdav_recv_speed', None),
                'webdav_send_speed': kwargs.get('webdav_send_speed', None),
                'webdav_timeout': kwargs.get('webdav_timeout', 30),
                'webdav_verbose': kwargs.get('webdav_verbose', False),
            }
        self._attributes: Dict[Tuple[str, str], Any] = kwargs.get(
            'attributes',
            None
        )
        self._children: List[DrbNode] = None
        self._parent: DrbNode = kwargs.get('parent', None)
        self._path: DrbNode = kwargs.get('path', None)
        if self.parent:
            self.webdav = self.parent.webdav
        else:
            self.webdav = None
        self.auth = auth

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        self.webdav = WebdavConnection(self.options, self.auth)
        if self._attributes is None:
            self._attributes = self.webdav.info(self.path.path)
        return self._attributes

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        if name in self.attributes.keys() and namespace_uri is None:
            return self.attributes[name]
        raise DrbException(f'Attribute not found name: {name}, '
                           f'namespace: {namespace_uri}')

    @property
    def parent(self) -> Optional[DrbNode]:
        return self._parent

    @property
    def path(self) -> ParsedPath:
        self.webdav = WebdavConnection(self.options, self.auth)
        if self._path is None:
            self._path = self.webdav.root
        return ParsedPath(self._path)

    @property
    def children(self) -> List[DrbNode]:
        self.webdav = WebdavConnection(self.options, self.auth)
        if self._children is None:
            self._children = []
            children_attributes = self.webdav.list(
                self.path.path,
                get_info=True
            )
            for attribute in children_attributes:
                child = DrbWebdavNode(
                    webdav_hostname=self.options.get('webdav_hostname'),
                    options=self.options,
                    parent=self,
                    path=attribute.get('path')
                )
                self._children.append(child)
        return self._children

    def close(self) -> None:
        pass

    @property
    def name(self) -> str:
        return self.get_attribute('name')

    @property
    def namespace_uri(self) -> Optional[str]:
        return None

    @property
    def value(self) -> Optional[Any]:
        return None

    def has_impl(self, impl: type) -> bool:
        return impl == io.BytesIO

    def get_impl(self, impl: type, **kwargs) -> Any:
        self.webdav = WebdavConnection(self.options, self.auth)
        if self.has_impl(impl) and self.attributes.get('size') is not None:
            return Download(
                self.path.path,
                self.webdav,
            )
        raise DrbNotImplementationException(
            f'no {impl} implementation found')

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        if namespace is None:
            if name is None:
                return len(self.children) > 0
            return name in list(map(lambda x: x.name, self.children))
        return False
