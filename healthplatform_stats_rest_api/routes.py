# coding: utf-8

from __future__ import print_function

from datetime import datetime

from bottle import response

from healthplatform_stats_rest_api import rest_api, __version__
from healthplatform_stats_rest_api.analytics import get_stats
from healthplatform_stats_rest_api.utils import auth_needed


@rest_api.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'  # Take out '*' in production!


@rest_api.route('/api/py/stats', apply=[auth_needed])
def stats_route():
    return get_stats()


@rest_api.route('/api')
@rest_api.route('/api/status')
@rest_api.route('/api/py')
def status():
    return {
        'rest_api_version': __version__,
        'server_time': datetime.now().strftime("%I:%M%p on %B %d, %Y")
    }
