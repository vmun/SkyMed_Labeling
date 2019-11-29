from markup.serializers import UserShortSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserShortSerializer(user, context={'request': request}).data
    }
