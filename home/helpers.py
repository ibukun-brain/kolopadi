import logging

from django.contrib.gis.geoip2 import GeoIP2


def get_user_geo_data(ip_address):
    """
    Fetch user geo data with GeoIP using user ip address
    """
    logging.info("Fetching Geo Data")
    g = GeoIP2()
    result = g.city(ip_address)
    return result
