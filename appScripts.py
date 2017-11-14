import uuid
import socket


# generate ID
def idGen():
    nid = str(uuid.uuid4())
    nid = nid[:6]
    return nid


# bad request
def badRequest(self):
    self.response.clear()
    self.response.set_status(400)
    self.response.out.write('Bad Request')


# forbidden request
def forbidRequest(self):
    self.response.clear()
    self.response.set_status(403)
    self.response.out.write('Forbidden')


def fBadRequest():
    return 'Bad Request', 400


def fForbid():
    return 'Forbidden', 403

def is_ipv6(addr):
    """Checks if a given address is an IPv6 address."""
    try:
        socket.inet_pton(socket.AF_INET6, addr)
        return True
    except socket.error:
        return False