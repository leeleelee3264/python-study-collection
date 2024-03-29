""" This module contains all notification payload objects."""


class BaseMsg(dict):
    """The BaseClass of all objects in notification payload."""
    apns_keys = []

    def __init__(self, custom_fields={}, **apn_args):
        super(BaseMsg, self).__init__(custom_fields, **apn_args)
        if custom_fields:
            self.update(custom_fields)

    def update_keys(self, apn_args, msg_obj_keys):
        """Transform the input keys with '_' to apns format with '-'."""
        for k, v in apn_args.items():
            formated_k = k.replace('_', '-')
            if formated_k in msg_obj_keys:
                del apn_args[k]
                apn_args[formated_k] = v


class Alert(BaseMsg):
    """The alert piece in aps section."""
    apns_keys = [
        'title', 'body', 'title-loc-key', 'title-loc-key', 'action-loc-key',
        'loc-key', 'loc-args', 'launch-image']

    def __init__(self, body=None, **apn_args):
        self.update_keys(apn_args, Alert.apns_keys)
        self.__setitem__('body', body)
        super(Alert, self).__init__(**apn_args)


class APS(BaseMsg):
    """The aps section in the payload."""
    apns_keys = [
        'mutable-content', 'alert', 'badge', 'sound', 'content-available',
        'category', 'thread-id']

    def __init__(self, **apn_args):
        self.update_keys(apn_args, APS.apns_keys)
        super(APS, self).__init__(**apn_args)


class Payload(BaseMsg):
    """The whole payload to send to APNs as the request body."""
    def __init__(self, aps, **apn_args):
        self.__setitem__('aps', aps)
        super(Payload, self).__init__(**apn_args)


class Headers(BaseMsg):
    """The request headers to send to APNs."""
    apns_keys = [
        'authorization', 'apns-id', 'apns-expiration', 'apns-priority',
        'apns-topic', 'apns-collapse-id']

    def __init__(self, **apn_args):
        self.update_keys(apn_args, Headers.apns_keys)
        super(Headers, self).__init__(**apn_args)
