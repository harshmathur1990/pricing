import copy
from pyramid.view import view_config
from pyramid.response import Response
from ofbusiness.products.models import products
from ofbusiness.subscriptions.models import subscriptions
from ofbusiness import app_settings as settings
from ofbusiness.cache import cache
from ofbusiness.subscriptions.utils import notifications


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'ofBusiness'}


@view_config(route_name='subscribe')
def subscribe(request):
    body = request.json
    properties = ['user_id', 'subscribe']
    for a_property in properties:
        if not body.get(a_property):
            data = u'{} Missing in request'.format(a_property)
            return Response(json=data, status=400)
    user_id = body.get('user_id')
    subscribe = body.get('subscribe')
    for obj in subscribe:
        key = user_id + '_' + obj.get('product_id')
        value = obj.get('when')
        if value not in settings.ALLOWED_NOTIFICATION_TYPES:
            continue
        data = subscriptions.get(key)
        if not data:
            data = [value]
        else:
            if value not in data:
                data.append(value)
        product_subs_key = settings.PRODUCT_SUBSCRIBER_CACHE_KEY + \
            obj.get('product_id')
        product_subscribers = cache.get(product_subs_key, set())
        product_subscribers.add(user_id)
        cache[product_subs_key] = product_subscribers
        subscriptions[key] = data
    response = {
        'success': True
    }
    return Response(json=response)


@view_config(route_name='unsubscribe')
def unsubscribe(request):
    body = request.json
    properties = ['user_id', 'unsubscribe']
    for a_property in properties:
        if not body.get(a_property):
            data = u'{} Missing in request'.format(a_property)
            return Response(json=data, status=400)
    user_id = body.get('user_id')
    unsubscribe = body.get('unsubscribe')
    for obj in unsubscribe:
        key = user_id + '_' + obj.get('product_id')
        subscriptions[key] = list()
        product_subs_key = settings.PRODUCT_SUBSCRIBER_CACHE_KEY + \
            obj.get('product_id')
        cache.get(product_subs_key, set()).remove(user_id)
    response = {
        'success': True
    }
    return Response(json=response)


@view_config(route_name='priceDataPoint')
def priceDataPoint(request):
    body = request.json
    properties = ['product_id', 'price', 'url']
    for a_property in properties:
        if not body.get(a_property):
            data = u'{} Missing in request'.format(a_property)
            return Response(json=data, status=400)
        if a_property is 'price':
            try:
                int(body.get('price'))
            except:
                error = {
                    'Price must be a integer'
                }
                return Response(json=error, status=400)
    product_id = body.get('product_id')
    price = int(body.get('price'))
    url = body.get('url')
    product = products.get(product_id)
    if not product:
        obj = dict()
        obj['product_id'] = product_id
        obj['price'] = price
        obj['url'] = url
        obj['alltimelow'] = price
        products[product_id] = obj
        notifications(product_id, ['ALWAYS'])
    else:
        events = list()
        price_diff = product['price'] - price
        ten_percent_of_product_price = float(product['price']) * float(0.1)
        if price < product['alltimelow']:
            events.append(settings.ALL_TIME_LOW)
        if price_diff > ten_percent_of_product_price:
            events.append(settings.MORE_THAN_10)
        if price < product['price']:
            events.append(settings.ALWAYS)

        if events:
            product['price'] = price
            if settings.ALL_TIME_LOW in events:
                product['alltimelow'] = price
            products[product_id] = product
            notifications(product_id, events)
    response = {
        'success': True
    }
    return Response(json=response)


@view_config(route_name='showSubscriptions')
def showSubscriptions(request):
    return Response(json=subscriptions)


@view_config(route_name='showProducts')
def showProducts(request):
    return Response(json=products)


@view_config(route_name='showCache')
def showCache(request):
    cache_copy = copy.deepcopy(cache)
    for key, val in cache_copy.items():
        cache_copy[key] = list(val)
    return Response(json=cache_copy)
