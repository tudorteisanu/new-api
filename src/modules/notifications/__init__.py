from src.app import api
from .resource import NotificationResource, NotificationOneResource, NotificationListResource
from .resource import NotificationCountResource
from .models import Notification

resource = '/notifications'

api.add_resource(NotificationResource, resource)
api.add_resource(NotificationOneResource, f'{resource}/<model_id>')
api.add_resource(NotificationListResource, f'{resource}/list')
api.add_resource(NotificationCountResource, f'{resource}/count')
