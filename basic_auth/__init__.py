from basic_auth.valheim_server import ValheimServer

server = ValheimServer(__name__)
app = server.flask

import basic_auth.RESTapi
import basic_auth.WebPage