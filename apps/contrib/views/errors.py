# -*- coding: utf-8 -*-

from django.shortcuts import render


def error_400(request, exc=None):
    """Renders default template for bad request errors."""
    return render(request, 'layouts/errors/400.html', {})


def error_403(request, exc=None):
    """Renders default template for forbidden errors."""
    return render(request, 'layouts/errors/403.html', {})


def error_404(request, exc=None):
    """Renders default template for not found errors."""
    return render(request, 'layouts/errors/404.html', {})


def error_500(request, exc=None):
    """Renders default template for server errors."""
    return render(request, 'layouts/errors/500.html', {})
