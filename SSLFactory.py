from OpenSSL import SSL, crypto
from twisted.internet import ssl

class ServerContextFactory(object):

    _ctx=None

    def getContext(self):
        """Create an SSL context."""

        if not self._ctx:
            ctxFactory=ssl.DefaultOpenSSLContextFactory(
                'sslcert/private/cakey.rsa', 'sslcert/cacert.pem')
            self._ctx=ctxFactory.getContext()
            return self._ctx
        else:
            return self._ctx

class ClientSSLAuthContextFactory(object):

    def getContext(self):
        """Create an SSL context."""
        ctxFactory=ssl.DefaultOpenSSLContextFactory(
            'sslcert/private/cakey.rsa', 'sslcert/cacert.pem')
        ctx=ctxFactory.getContext()
        ctx.set_verify(
            SSL.VERIFY_PEER|SSL.VERIFY_FAIL_IF_NO_PEER_CERT,
            self.verifyCallback
        )
        ctx.load_verify_locations("sslcert/cacert.pem")
        ctx.set_timeout(3600)
        return ctx

    def verifyCallback(self, connection, x509, errnum, errdepth, ok):
        if not ok:
            print 'invalid cert from subject:', x509.get_subject()
            return False
        return True
