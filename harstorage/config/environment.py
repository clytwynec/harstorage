import os

from mako.lookup import TemplateLookup
from pylons.configuration import PylonsConfig
from pylons.error import handle_mako_error
from pylons import cache

import harstorage.lib.app_globals as app_globals
import harstorage.lib.helpers
from harstorage.config.routing import make_map


def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config`` object"""

    config = PylonsConfig()

    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
                 controllers=os.path.join(root, "controllers"),
                 static_files=os.path.join(root, "public"),
                 templates=[os.path.join(root, "templates")])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package="harstorage", paths=paths)

    config["routes.map"] = make_map(config)
    config["pylons.app_globals"] = app_globals.Globals(config)
    config["pylons.h"] = harstorage.lib.helpers

    # Get Mongo settings from environment or use local defaults
    default_mongo_uri = "mongodb://admin:admin@localhost:27017/harstorage"
    config["app_conf"]["mongo_uri"] = os.environ.get(
        "MONGOHQ_URL", default_mongo_uri
    )

    # Setup cache object as early as possible
    cache._push_object(config["pylons.app_globals"].cache)

    # Create the Mako TemplateLookup, with the default auto-escaping
    config["pylons.app_globals"].mako_lookup = TemplateLookup(
        directories=paths["templates"],
        error_handler=handle_mako_error,
        module_directory=os.path.join(app_conf["cache_dir"], "templates"),
        input_encoding="utf-8",
        default_filters=["escape"],
        imports=["from webhelpers.html import escape"])

    return config
