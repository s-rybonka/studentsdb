from .util import get_groups


def students_processor(request):
    absolute_url = "{}://{}:{}".format(request.scheme, request.META['SERVER_NAME'], request.META['SERVER_PORT'])

    return {'ABSOLUTE_URL': absolute_url}


def groups_processors(request):
    return {'GROUPS': get_groups(request)}
