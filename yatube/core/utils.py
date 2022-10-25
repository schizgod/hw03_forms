from django.core.paginator import Paginator


def paginate(request, POSTS_NUMBER, querysets):
    paginator = Paginator(querysets, POSTS_NUMBER)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def truncatechars(text, STRING_TRANCATE_NUM):
    return (
        text[:STRING_TRANCATE_NUM] + '...'
        if len(text) > STRING_TRANCATE_NUM
        else text
    )
