from django.core.paginator import Paginator


def paginate(request, POSTS_NUMBER, querysets):
    paginator = Paginator(querysets, POSTS_NUMBER)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
