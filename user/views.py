import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from .forms import CustomUserCreationForm
from .models import User, Student, Admin

logger = logging.getLogger(__name__)


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                name = form.cleaned_data.get('name')
                email = form.cleaned_data.get('email')
                semester = form.cleaned_data.get('semester')

                if 'student_signup' in request.POST:
                    user.is_student = True
                    user.save()
                    # Generate student_id from username
                    student_id = f"STU_{user.username.upper()}"
                    Student.objects.create(user=user, student_id=student_id, name=name, email=email, semester=semester)
                    logger.info(f'New student registered: {student_id}')
                    messages.success(request, 'Student account created successfully! Please login.')

                elif 'admin_signup' in request.POST:
                    user.is_admin = True
                    user.save()
                    # Generate admin_id from username
                    admin_id = f"ADM_{user.username.upper()}"
                    Admin.objects.create(user=user, admin_id=admin_id, name=name, email=email)
                    logger.info(f'New admin registered: {admin_id}')
                    messages.success(request, 'Admin account created successfully! Please login.')

                return redirect('login')

            except IntegrityError as e:
                logger.error(f'Integrity error during signup: {str(e)}')
                messages.error(request, 'An account with this information already exists.')
            except Exception as e:
                logger.error(f'Error during signup: {str(e)}')
                messages.error(request, 'An error occurred during registration. Please try again.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'user/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Please provide both username and password.')
            return render(request, 'user/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            logger.info(f'User {username} logged in successfully')

            if user.is_student:
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('student_dashboard')
            elif user.is_admin:
                messages.success(request, f'Welcome back, Admin {user.username}!')
                return redirect('admin_dashboard')
            else:
                messages.warning(request, 'User role not assigned. Please contact administrator.')
                return redirect('homepage')
        else:
            logger.warning(f'Failed login attempt for username: {username}')
            messages.error(request, 'Invalid username or password.')
            return render(request, 'user/login.html')
    else:
        return render(request, 'user/login.html')

@login_required
def logout_view(request):
    username = request.user.username
    logout(request)
    logger.info(f'User {username} logged out')
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def homepage_view(request):
    try:
        if request.user.is_student:
            student = Student.objects.get(user=request.user)
            context = {
                'show_buttons': student.application_status,
                'student': student
            }
            return render(request, 'homepage.html', context)

        elif request.user.is_admin:
            # Redirect to admin dashboard
            return redirect('admin_dashboard')

        else:
            messages.error(request, 'User role not assigned. Please contact administrator.')
            logout(request)
            return redirect('login')

    except Student.DoesNotExist:
        logger.error(f'Student profile not found for user {request.user.username}')
        messages.error(request, 'Student profile not found. Please contact administrator.')
        logout(request)
        return redirect('login')
    except Exception as e:
        logger.error(f'Error in homepage view: {str(e)}')
        messages.error(request, 'An error occurred. Please try again.')
        return redirect('login')

