from mrsservice.lib.odoo import Odoo
from flask_redis import Redis
from flask_babel import Babel
from flask.ext.cache import Cache


odoo = Odoo()
redis = Redis()
babel = Babel()
cache = Cache(config={'CACHE_TYPE': 'simple'})

