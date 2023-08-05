import pynng

from foreverbull_core.models.socket import Request, Response, SocketConfig, SocketType
from foreverbull_core.socket.client import SocketClient


def test_socket_client():
    client = SocketClient(SocketConfig(host="127.0.0.1"))
    req_socket = pynng.Req0(dial=client.url())

    req = Request(task="demo")
    req_socket.send(req.dump())
    client_recieved = client.recv()

    rsp = Response(task="demo")
    client.send(rsp)
    req_socket_recieved = req_socket.recv()

    assert type(client_recieved) == Request
    assert type(req_socket_recieved) == bytes
    assert client.close() is None


def test_context_client():
    rep_client = SocketClient(
        SocketConfig(host="127.0.0.1", port=1337, listen=True, dial=False, socket_type=SocketType.REPLIER)
    )
    req_client = SocketClient(
        SocketConfig(host="127.0.0.1", port=1337, listen=False, dial=True, socket_type=SocketType.REQUESTER)
    )

    rep_context = rep_client.new_context()
    req_context = req_client.new_context()

    req_context.send(Request(task="demo"))

    request = rep_context.recv()
    assert request.task == "demo"

    rep_context.send(Response(task="works"))

    response = req_context.recv()
    assert response.task == "works"

    rep_context.close()
    req_context.close()
    req_client.close()
    rep_client.close()
