# Install the Linux Epoll Reactor
from twisted.internet import epollreactor
epollreactor.install()

from twisted.cred.portal import Portal
from twisted.cred import checkers
from twisted.application import internet, service
from twisted.web import server

from goliat.webserver import page
from goliat.utils.config import ConfigManager
from goliat.database import Database
from goliat.session import GoliatSession, SessionManager
from goliat.auth import (DBCredentialsChecker, SessionCookieCredentialsChecker)
from goliat.auth.realm import GoliatRealm

from SSLFactory import ServerContextFactory, ClientSSLAuthContextFactory


application=service.Application('GsCNT')

# Create the System config object
config=ConfigManager()
config.load_config('Goliat', 'gscnt.cfg', True)
cfg=config.get_config('Goliat')
# Create the root page
page=page.Page(cfg['Project'])
# Initialize the database
try:
    database=Database()
except TypeError:
    print 'WARNING: Your database schema is not initialized.'
    print 'You will not be able to use Goliat Databse Authentication.'

# Check for Orbited 
if cfg['Project']['orbited']:
    # Start the embedded MorbidQ Stomp Server
    # NOTE: If you need clustering, multicore, transactions, receipts etc etc
    # will be better if you use ActiveMQ from The Apache Software Foundation
    # and run it in standalone mode, for do that just remove those lines.
    # More information is available under http://www.orbited.org
    # ANOTHER NOTE: You will create a STOMP Productor in your own Python code
    # and connect it as TCPClient to localhost:61613 (or another), then use the
    # Goliat JavaScript object `Goliat.StompClient` in your UI code in order
    # to connect data sockets. You can attach the Goliat.StompClient to any
    # Goliat or ExtJS object, including ExtJS Stores.
    # More information is available under http://goliat.open-phoenix.com/wiki

    # Perform the Orbited imports and configurations
    from orbited import logging, config
    config.map['[access]'][('localhost', 61613)]=['*']
    logging.setup(config.map)

    import orbited.system
    import orbited.start

    # Start logging orbited services
    orbited.start.logger=logging.get_logger('orbited.start')

    # Start orbited
    orbited.start._setup_protocols(page)

    from morbid.morbid import StompFactory
    stomp=StompFactory()
    stompserv=internet.TCPServer(61613, stomp)
    stompserv.setName('StompService')
    stompserv.setServiceParent(application)

# Create the Twisted Portal using the GoliatRealm
portal=Portal(GoliatRealm(page))

# If the initialized database is a valid database register chedential checkers
# at Portal
if database.is_valid():
    portal.registerChecker(DBCredentialsChecker())
    portal.registerChecker(SessionCookieCredentialsChecker())

# If the anonymous application navigation is configured, just add the checker
if cfg['Project']['allow_anonymous']:
    portal.registerChecker(checkers.AllowAnonymousAccess())

# Initialize the Goliat Auth Wrapper SessionManager
root=SessionManager(portal)

goliat_app_site=server.Site(root)
# Use GoliatSession as the session factory
goliat_app_site.sessionFactory=GoliatSession

sslFactory=ServerContextFactory()
#sslFactory=ClientSSLAuthContextFactory()
cfg['sslFactory']=sslFactory

httpserver=internet.SSLServer(cfg['Project']['app_port'], goliat_app_site, sslFactory)
httpserver.setName('GsCNT Application')
httpserver.setServiceParent(application)

# You can add as many services as you need using the MultiService interface
# More info available over http://goliat.open-phoenix.com/wiki
# To activate MultiServices jus uncomment the following lines and add your
# services to the services directory at project root, you will add
# admin=<admin name>, password=<password> and admin_port=<port> to project
# configuration file gscnt.cfg 

from goliat.multiservice import MultiService
services=MultiService(application)
services.create_service_admin_page()
services.register_new_services()

# Store the service on 'Goliat' global config, in that way, it will be
# accessible at whole application. (Remember: ConfigManager is a Borg object)
cfg['service']=application
