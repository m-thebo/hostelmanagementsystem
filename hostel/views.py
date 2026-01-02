import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ComplaintForm, ApplicationForm
from .decorators import student_required, admin_required
from django.http import FileResponse
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

@student_required
def lodge_complaint(request):
    try:
        if request.method == 'POST':
            form = ComplaintForm(request.POST)
            if form.is_valid():
                complaint = form.save(commit=False)
                complaint.student = request.user.student
                complaint.save()
                logger.info(f'Student {request.user.student.student_id} lodged complaint ID {complaint.id}')
                messages.success(request, 'Complaint lodged successfully!')
                return redirect('homepage')
        else:
            form = ComplaintForm()
    except Exception as e:
        logger.error(f'Error lodging complaint: {str(e)}')
        messages.error(request, 'An error occurred while lodging your complaint. Please try again.')
        form = ComplaintForm()

    return render(request, 'hostel/lodge_complaint.html', {'form': form})


@student_required
def download_voucher(request):
    try:
        file = open('static/fee_voucher.pdf', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'attachment; filename="FeeVoucher.pdf"'
        logger.info(f'Student {request.user.student.student_id} downloaded fee voucher')
        return response
    except FileNotFoundError:
        logger.error('Fee voucher file not found')
        messages.error(request, 'Fee voucher not available at this time.')
        return redirect('homepage')
    except Exception as e:
        logger.error(f'Error downloading voucher: {str(e)}')
        messages.error(request, 'An error occurred while downloading the voucher.')
        return redirect('homepage')


@student_required
def submit_application(request):
    from .models import Application

    try:
        # Check if student already has an application
        existing_application = Application.objects.filter(applicant=request.user.student).first()

        if existing_application:
            messages.warning(request, 'You have already submitted an application.')
            logger.warning(f'Student {request.user.student.student_id} attempted duplicate application')
            return redirect('homepage')

        if request.method == 'POST':
            form = ApplicationForm(request.POST)
            if form.is_valid():
                application = form.save(commit=False)
                application.applicant = request.user.student
                application.save()
                logger.info(f'Student {request.user.student.student_id} submitted application ID {application.id}')
                messages.success(request, 'Room application submitted successfully!')
                return redirect('homepage')
        else:
            form = ApplicationForm()
    except Exception as e:
        logger.error(f'Error submitting application: {str(e)}')
        messages.error(request, 'An error occurred while submitting your application. Please try again.')
        form = ApplicationForm()

    return render(request, 'hostel/room_application.html', {'form': form})

@admin_required
def fetch_complaints(request):
    """Fetch all complaints using Django ORM (SQLite compatible)"""
    from .models import Complaint

    try:
        # Get all complaints with related student data
        complaints = Complaint.objects.select_related('student').all().order_by('-id')

        logger.info(f'Admin {request.user.username} fetched all complaints')
        return render(request, 'hostel/complaints.html', {'complaints': complaints})

    except Exception as e:
        logger.error(f'Error fetching complaints: {str(e)}')
        messages.error(request, 'An error occurred while fetching complaints.')
        return redirect('homepage')

@admin_required
def fetch_applications(request):
    """Fetch all applications using Django ORM (SQLite compatible)"""
    from .models import Application

    try:
        # Get all applications with related applicant data
        applications = Application.objects.select_related('applicant').all().order_by('-id')

        logger.info(f'Admin {request.user.username} fetched all applications')
        return render(request, 'hostel/applications.html', {'applications': applications})

    except Exception as e:
        logger.error(f'Error fetching applications: {str(e)}')
        messages.error(request, 'An error occurred while fetching applications.')
        return redirect('homepage')


@admin_required
def admin_dashboard(request):
    """Admin dashboard with statistics and charts (SQLite compatible)"""
    from .models import Student, Room, Hostel, Application, Complaint

    try:
        # Get statistics using Django ORM
        total_students = Student.objects.count()
        total_rooms = Room.objects.count()
        pending_applications = Application.objects.filter(status=False).count()
        approved_applications = Application.objects.filter(status=True).count()
        pending_complaints = Complaint.objects.filter(status='Pending').count()
        inprogress_complaints = Complaint.objects.filter(status='In Progress').count()
        resolved_complaints = Complaint.objects.filter(status='Resolved').count()
        students_with_rooms = Student.objects.filter(application_status=True).count()
        hostel_count = Hostel.objects.count()

        # Calculate occupancy percentage
        if total_rooms > 0:
            occupancy_rate = round((students_with_rooms / total_rooms) * 100, 1)
        else:
            occupancy_rate = 0

        stats = {
            'total_students': total_students,
            'total_rooms': total_rooms,
            'pending_applications': pending_applications,
            'approved_applications': approved_applications,
            'pending_complaints': pending_complaints,
            'inprogress_complaints': inprogress_complaints,
            'resolved_complaints': resolved_complaints,
            'students_with_rooms': students_with_rooms,
        }

        context = {
            'stats': stats,
            'hostel_count': hostel_count,
            'occupancy_rate': occupancy_rate,
        }

        logger.info(f'Admin {request.user.username} accessed dashboard')
        return render(request, 'hostel/admin_dashboard.html', context)

    except Exception as e:
        logger.error(f'Error loading admin dashboard: {str(e)}')
        messages.error(request, 'An error occurred while loading the dashboard.')
        return redirect('homepage')


@student_required
def student_dashboard(request):
    """Student dashboard showing application and complaint status (SQLite compatible)"""
    from .models import Application, Complaint

    try:
        student = request.user.student

        # Get student's application using Django ORM
        application = Application.objects.filter(applicant=student).first()

        # Get student's complaints using Django ORM
        complaints = Complaint.objects.filter(student=student).order_by('-id')

        # Get room details if allocated
        room = None
        if student.application_status:
            room = student.rooms.first()

        context = {
            'student': student,
            'application': application,
            'complaints': complaints,
            'room': room,
        }

        logger.info(f'Student {student.student_id} accessed dashboard')
        return render(request, 'hostel/student_dashboard.html', context)

    except Exception as e:
        logger.error(f'Error loading student dashboard: {str(e)}')
        messages.error(request, 'An error occurred while loading your dashboard.')
        return redirect('homepage')
