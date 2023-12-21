from django.shortcuts import redirect, render
from functools import wraps


def seller_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_seller:
            return function(request, *args, **kwargs)
        else:
            return render(request, 'forbidden.html')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def verificatoin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_seller:
            if request.user.is_verified:
                return function(request, *args, **kwargs)
            else:
                return render(request, 'seller_unverified.html')
        else:
            return render(request, 'forbidden.html')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
