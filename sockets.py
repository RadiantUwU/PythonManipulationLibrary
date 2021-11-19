import asyncio
import pickle
import socket
import threading
from types import FunctionType
from typing import Tuple, NewType, Union, Any, List

from logger import Logger
from nullObj import NullClass

IpAddress = NewType('IpAddress', Tuple[str, int])


def serv_con_to_sock(connection: Tuple[socket.socket, IpAddress]):
    sock = Socket(connection[1], connection[0])
    return sock


# noinspection PyAttributeOutsideInit
class Socket:
    """A network socket. You can send anything through it."""

    def __init__(self, address: IpAddress, the_socket: socket.SocketType = None,
                 logger: Union[Logger, NullClass] = NullClass):
        """Create a new socket on address"""
        self.address = address
        self.logger = logger
        if the_socket is None:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect(address)
        else:
            self._socket = the_socket
        self.is_socket_closed = False

    # noinspection PyAttributeOutsideInit
    def send(self, data, internal_instruction=0) -> Union[None, ConnectionResetError]:
        """Sends data. It gets converted into a bytes object by pickle module and sent."""
        if not self.is_socket_closed:
            try:
                self._socket.send(
                    pickle.dumps(
                        {
                            "internal": internal_instruction,
                            "message": data
                        }
                    )
                )
            except ConnectionResetError as e:
                self.is_socket_closed = True
                return e

    def recv(self, buffer_size: int = 1024) -> Any:
        """Reads data."""
        if not self.is_socket_closed:
            try:
                data = pickle.loads(self._socket.recv(buffer_size))
                return data
            except ConnectionResetError:
                self.is_socket_closed = True
            except pickle.PickleError as e:
                self.logger.error("Connection error. Socket id {sock_id} will be closed.".format(sock_id=id(self)))
                self.send(
                    self.internal_instruction("disconnect", "pickle.UnpicklingError:" + str(str(" ").join(e.args))),
                    True)
                self.close()
                self.is_socket_closed = True

    @staticmethod
    def internal_instruction(inst, *args):
        args: list = list(args)
        for _ in range(5 - len(args)):
            args.append(None)
        instructions = {
            "disconnect": {
                "type": "disconnect",
                "message": str((args[0] if args[0] is not None else "Disconnected"))},
            "connectFail": {
                "type": "connectFail",
                "message": str((args[0] if args[0] is not None else "Disconnected"))},
            "connectOk": {
                "type": "connectOk",
                "message": args[0]},
            "ping": {
                "type": "ping"},
            "ch_buf_size": {
                "type": "ch_buf_size",
                "message": int((args[0] if args[0] is not None else 1024))},
        }
        return instructions[inst]

    def close(self):
        try:
            self._socket.close()
            self.is_socket_closed = True
        except ConnectionResetError:
            self.is_socket_closed = True


# noinspection PyAttributeOutsideInit
class ListeningServerSocket:
    """A listening network socket."""

    def __init__(self, address: Tuple[str, int]):
        super().__init__(address)

    def onInit(self, address: Tuple[str, int]):
        """Make a listening network socket on the address."""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(address)
        self._socket.listen(4)
        self.newConnections: List[Socket] = []
        self.connections: List[Socket] = []
        self.listening = False
        self._private_listening_thread = None

    def listen(self, function_on_connect: FunctionType = None):
        if not self.listening:
            self.listening = True
            asyncio.run(self._private_listen(function_on_connect))

    async def _private_listen(self, function_on_connect):
        while self.listening:
            c = serv_con_to_sock(self._socket.accept())
            self.connections.append(c)
            self.newConnections.append(c)
            if function_on_connect is not None:
                threading.Thread(target=function_on_connect, args=(c,), daemon=True).start()
            self.checkForClosedCons()

    def checkForClosedCons(self):
        for index, i in enumerate(self.connections):
            if i.is_socket_closed:
                del self.connections[index]
