from django.utils.http import urlencode

from django.template.loader_tags import register

DISPLAY_RANGE = 3


@register.filter()
def pagination_range(page):
    result = []

    if page.number > DISPLAY_RANGE + 1:
        result.append(1)
        if page.number > DISPLAY_RANGE + 2:
            result.append(None)

    start = max(1, page.number - DISPLAY_RANGE)
    end = min(page.paginator.num_pages, page.number + DISPLAY_RANGE)
    result += list(range(start, end + 1))

    if page.paginator.num_pages - page.number > DISPLAY_RANGE:
        if page.paginator.num_pages - page.number - 1 > DISPLAY_RANGE:
            result.append(None)
        result.append(page.paginator.num_pages)

    return result


@register.simple_tag()
def pagination_url(request, page):
    params = {}
    for key in request.GET:
        params[key] = request.GET.get(key, '')
    params['page'] = page
    return urlencode(params)
