import os
from socket import AF_INET, SOCK_STREAM, socket
from typing import Union

import pyngrok.conf
import pyngrok.ngrok
import requests
import yaml
from pyngrok.exception import PyngrokError
from requests.exceptions import ConnectionError, InvalidURL

from . import env, models

logger = models.ngrok_logger()


class Ngrok:
    """Class to initiate ngrok connection, tunneling, and get existing tunnels.

    >>> Ngrok

    """

    SOCKET = socket(AF_INET, SOCK_STREAM)
    TUNNELS = f'http://{env.host}:4040/api/tunnels'
    CONNECTION = None

    def get_ngrok(self) -> Union[str, None]:
        """Identifies if an existing ngrok tunnel by sending a ``GET`` request to ngrok API endpoint.

        Returns:
            str:
            Returns the `ngrok` public URL.
        """
        try:
            logger.info(f'Looking for existing tunnels at {self.TUNNELS}')
            response = requests.get(url=self.TUNNELS)
        except InvalidURL:
            logger.error(f'Invalid URL: {self.TUNNELS}')
            return
        except ConnectionError:
            logger.error(f'Connection failed: {self.TUNNELS}')
            return
        if not response.ok:
            logger.error(f'Failed response [{response.status_code}] from {self.TUNNELS}')
            return
        serving_at = yaml.load(response.content.decode(), Loader=yaml.FullLoader)['tunnels']
        return serving_at[0].get('public_url')

    def connect(self, new_connection: bool = False) -> Union[str, None]:
        """Creates an HTTP socket and uses `pyngrok` module to bind the socket.

        Args:
            new_connection: Takes a boolean flag to bind a local socket to the port and spin up a new connection.

        See Also:
            Run the following code to setup.

            .. code-block:: python
                :emphasize-lines: 4,7,10

                from pyngrok.conf import PyngrokConfig, get_default
                from pyngrok.ngrok import set_auth_token

                # Sets auth token only during run time without modifying global config.
                PyngrokConfig.auth_token = '<NGROK_AUTH_TOKEN>'

                # Uses auth token from the specified file without modifying global config.
                get_default().config_path = "/path/to/config.yml"

                # Changes auth token at $HOME/.ngrok2/ngrok.yml
                set_auth_token('<NGROK_AUTH_TOKEN>')

        Returns:
            tuple:
            A tuple of the connected socket and the public URL.
        """
        if new_connection:
            server_address = (env.host, env.port)
            self.SOCKET.bind(server_address)  # Bind only accepts tuples
        self.SOCKET.listen(1)

        if env.ngrok_auth:
            logger.info('Using env var to set ngrok auth.')
            pyngrok.ngrok.set_auth_token(env.ngrok_auth)
        elif os.path.isfile('ngrok.yml'):
            logger.info('Using config file for ngrok auth')
            pyngrok.conf.get_default().config_path = 'ngrok.yml'
        else:
            logger.warning('Neither config file nor env var for ngrok auth was found.')
            return
        try:
            endpoint = pyngrok.ngrok.connect(env.port, "http", options={"remote_addr": f"{env.host}:{env.port}"})
            endpoint = endpoint.public_url.replace('http', 'https')
            logger.info(f'Ngrok connection has been established at {endpoint}.')
            return endpoint
        except PyngrokError as err:
            logger.error(err)

    def tunnel(self) -> None:
        """Once the socket is bound, the listener is activated and runs in a forever loop accepting connections."""
        while True:
            if env.STOPPER:
                break
            try:
                logger.info("Waiting for a connection")
                self.CONNECTION, client_address = self.SOCKET.accept()
                logger.info(f"Connection established from {client_address}")
            except KeyboardInterrupt:
                self.stop_tunnel()
                break
            except OSError as error:
                logger.error(error)
                break

    def stop_tunnel(self) -> None:
        """Closes the existing socket and connection where the socket is accepted."""
        logger.info("Shutting down server")
        if self.CONNECTION:
            self.CONNECTION.close()
        pyngrok.ngrok.kill(pyngrok_config=None)  # uses default config when None is passed
        self.SOCKET.close()
