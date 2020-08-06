import logging

from initialize import api, app
from resources import Ping

logger = logging.getLogger(__name__)

# Routes
from resources.parser_server import SiteParser, Result

api.add_resource(SiteParser, "/parse")
api.add_resource(Result, "/result/<id>")
api.add_resource(Ping, "/hello")


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.DEBUG)
    app.run(host="0.0.0.0", port=8000)