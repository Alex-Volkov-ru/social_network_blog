from django.shortcuts import render


def about(request):
    template_name = 'pages/about.html'
    """Страница "О нас"."""
    return render(request, template_name)


def rules(request):
    """Страница "Правила"."""
    template_name = 'pages/rules.html'
    return render(request, template_name)


def csrf_failure_view(request, reason=""):
    """Вывод 403 ошибки."""
    return render(request, 'pages/403csrf.html', status=403)


def page_not_found_view(request, exception):
    """Вывод 404 ошибки пользователю."""
    return render(request, 'pages/404.html', status=404)


def server_error_view(request):
    """Вывод 500 ошибки пользователю."""
    return render(request, 'pages/500.html', status=500)
