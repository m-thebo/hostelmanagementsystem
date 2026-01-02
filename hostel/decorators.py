"""
Custom authentication and authorization decorators for HostelMS.
"""
from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def student_required(view_func):
    """
    Decorator that ensures the user is authenticated and is a student.
    Redirects to login if not authenticated, or homepage if not a student.
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'is_student') or not request.user.is_student:
            messages.error(request, 'This page is only accessible to students.')
            return redirect('homepage')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """
    Decorator that ensures the user is authenticated and is an admin.
    Redirects to login if not authenticated, or homepage if not an admin.
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'is_admin') or not request.user.is_admin:
            messages.error(request, 'This page is only accessible to administrators.')
            return redirect('homepage')
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(roles=None):
    """
    Generic decorator that requires specific roles.

    Args:
        roles (list): List of role attributes to check (e.g., ['is_student', 'is_admin'])

    Usage:
        @role_required(roles=['is_admin'])
        def my_view(request):
            ...
    """
    if roles is None:
        roles = []

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            user_has_role = False
            for role in roles:
                if hasattr(request.user, role) and getattr(request.user, role):
                    user_has_role = True
                    break

            if not user_has_role:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('homepage')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
