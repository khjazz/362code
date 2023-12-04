import socket
import logging
from concurrent.futures import ThreadPoolExecutor


def get_quotes(host, port, protocol, concurrency, executor=ThreadPoolExecutor()):
    """
    Use a thread pool to start multiple clients to get quotes from the quote server.
    Protocol can be "tcp" or "udp".
    """
    # validate the protocol value
    if protocol not in ["tcp", "udp"]:
        raise ValueError("protocol must be tcp or udp")
    try:
        res = executor.map(
            start_tcp_client if protocol == "tcp" else start_udp_client,
            [host] * concurrency,
            [port] * concurrency,
        )
        return {"protocol": protocol, "concurrency": concurrency, "quotes": list(res)}
    except Exception as e:
        logging.error(f"error trying to get quotes from the quote server: {e}")


def start_tcp_client(host, port):
    """
    Start a TCP client and return the received data.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b"")
        data = s.recv(1024)
        return data.decode()


def start_udp_client(host, port):
    """
    Start a UDP client and return the received data.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(b"", (host, port))
        data, _ = s.recvfrom(1024)
        return data.decode()
