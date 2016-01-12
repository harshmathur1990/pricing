from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('subscribe', '/subscribe',
                     request_method='POST',
                     accept='application/json')
    config.add_route('unsubscribe', '/unsubscribe',
                     request_method='POST',
                     accept='application/json')
    config.add_route('priceDataPoint', '/priceDataPoint',
                     request_method='POST',
                     accept='application/json')
    config.add_route('showSubscriptions', '/showSubscriptions',
                     request_method='GET',
                     accept='application/json')
    config.add_route('showProducts', '/showProducts',
                     request_method='GET',
                     accept='application/json')
    config.add_route('showCache', '/showCache',
                     request_method='GET',
                     accept='application/json')
    config.scan()
    return config.make_wsgi_app()
