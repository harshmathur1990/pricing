from ofbusiness.cache import cache
from ofbusiness import app_settings as settings
from ofbusiness.subscriptions.models import subscriptions
from ofbusiness.products.models import products


def notifications(product_id, typeList):
    if not typeList:
        return
    import pdb;pdb.set_trace()
    key = settings.PRODUCT_SUBSCRIBER_CACHE_KEY + product_id
    user_list = cache.get(key, list())
    product = products.get(product_id)
    if product:
        for a_user in user_list:
            user_key = a_user + '_' + product_id
            subs = subscriptions.get(user_key)
            common_events = [val for val in subs if val in typeList]
            if common_events:
                if settings.ALL_TIME_LOW in common_events:
                    data = {
                        'productId': product_id,
                        'url': product.get('url'),
                        'price': product.get('price'),
                        'reason': settings.ALL_TIME_LOW
                    }
                    # we can make a api call here
                    print a_user, data
                elif settings.MORE_THAN_10 in common_events:
                    data = {
                        'productId': product_id,
                        'url': product.get('url'),
                        'price': product.get('price'),
                        'reason': settings.MORE_THAN_10
                    }
                    # we can make a api call here
                    print a_user, data
                else:
                    data = {
                        'productId': product_id,
                        'url': product.get('url'),
                        'price': product.get('price'),
                        'reason': settings.ALWAYS
                    }
                    # we can make a api call here
                    print a_user, data
