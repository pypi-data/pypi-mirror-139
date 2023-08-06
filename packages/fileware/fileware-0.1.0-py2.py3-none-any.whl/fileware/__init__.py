import functools
import os
import ssl
import warnings
from http.server import HTTPServer
from multiprocessing import Process
from socket import AF_INET, SOCK_DGRAM, socket
from typing import AnyStr, Union
from uuid import UUID

from . import cert, env, models, ngrok
from .server import Authenticator

logger = models.server_logger()


class FileWare:
    """Class to instantiate FileWare object, and run the file server in a thread.

    >>> FileWare

    """

    def __init__(self, port: Union[int, str] = None, username: AnyStr = None, password: AnyStr = None,
                 host_dir: AnyStr = None, ngrok_auth: Union[UUID, str] = None, gmail_user: str = None,
                 gmail_pass: str = None, recipient: str = None) -> None:
        """Initiates the ``FileWare``.

        Args:
            port: Port number in which the file server is running.
            username: Username to access fileserver.
            password: Password to access fileserver.
            host_dir: Takes the path to serve as an argument. Can also be loaded via env vars.
            ngrok_auth: Ngrok auth token for tunneling.
            gmail_user: Username for email notification.
            gmail_pass: Password for email notification.
            recipient: Email address to receive notification.

        See Also:
            - All these arguments can be loaded via env vars by placing the key-value pairs in a ``.env`` file.
            - The ``.env`` file should be stored in the current working directory.
        """
        if port:
            env.port = port
        if gmail_user:
            env.gmail_user = gmail_user
        if gmail_pass:
            env.gmail_pass = gmail_pass
        if recipient:
            env.recipient = recipient
        if username:
            env.username = username
        if password:
            env.password = password
        if ngrok_auth:
            env.ngrok_auth = ngrok_auth
        if host_dir:
            if os.path.isdir(host_dir):
                env.host_dir = host_dir
            else:
                warnings.warn(f"The specified path: {host_dir} doesn't exist. Defaulting to {env.host_dir}")

        self._ngrok_object = ngrok.Ngrok()
        self._public_url = self._ngrok_object.connect()
        self._ngrok_process = Process(target=self._ngrok_object.tunnel)
        ssh_dir = env.home_dir + os.path.sep + os.path.join('.ssh')
        self._cert_file = os.path.expanduser(ssh_dir) + os.path.sep + "cert.pem"
        self._key_file = os.path.expanduser(ssh_dir) + os.path.sep + "key.pem"

        if not self._public_url:
            self._host_on_ip()

        handler_class = functools.partial(
            Authenticator,
            username=env.username,
            password=env.password,
            directory=env.host_dir
        )
        self._http_server = HTTPServer(server_address=(env.host, env.port), RequestHandlerClass=handler_class)

    def _host_on_ip(self):
        """Changes hostname to local IP address and generates a self-signed certificate.

        See Also:
            - Hosts on ``localhost`` (127.0.0.1) if Ngrok connection is successful, otherwise hosts on local IP address.
            - Ngrok uses its own certificate, so the self-signed cert is generated only when hosting on local IP.
        """
        ip_socket = socket(AF_INET, SOCK_DGRAM)
        ip_socket.connect(("8.8.8.8", 80))
        env.host = ip_socket.getsockname()[0]
        if not all([os.path.isfile(self._cert_file), os.path.isfile(self._key_file)]):
            cert.generate_cert(common_name='*.ngrok.com', cert_file=self._cert_file, key_file=self._key_file)

    def initiate_connection(self) -> str:
        """Initiates fileserver connection after trying to trigger ngrok tunnel.

        See Also:
            - Checks for ``cert.pem`` and ``key.pem`` files in ~home/ssh path.
            - If not generates a self-signed certificate using ``OpenSSL``
            - If ngrok tunnel is running on the port already, initiates file server on localhost else uses local IP.
        """
        if not self._public_url and all([os.path.isfile(self._cert_file), os.path.isfile(self._key_file)]):
            self._http_server.socket = ssl.wrap_socket(sock=self._http_server.socket, server_side=True,
                                                       certfile=self._cert_file, keyfile=self._key_file)
            endpoint = f"https://{':'.join(map(str, self._http_server.server_address))}"
        else:
            endpoint = f"http://{':'.join(map(str, self._http_server.server_address))}"

        logger.info(f"Initiating file server at: {endpoint}")
        if self._public_url:
            logger.info(f"Hosted at public endpoint: {self._public_url}")

        if self._public_url:
            return self._public_url
        else:
            return self._public_url

    def shutdown(self) -> None:
        """Terminates the http server, ngrok process and the socket server."""
        env.STOPPER = True
        if self._ngrok_process.is_alive():
            self._ngrok_process.join(timeout=1e-2)
            self._ngrok_object.stop_tunnel()
        self._http_server.server_close()
        self._http_server.shutdown()

    def serve(self) -> None:
        """Starts the file server session and ngrok tunnel (if available)."""
        if self._public_url:
            self._ngrok_process.start()
        try:
            self._http_server.serve_forever()
        except KeyboardInterrupt:
            [(os.rename(new_name, old_name), logger.critical(f'Reverted {new_name} to {old_name}'))
             for each in env.renamed for old_name, new_name in each.items() if env.renamed]
            self.shutdown()
