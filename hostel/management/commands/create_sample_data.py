from django.core.management.base import BaseCommand
from user.models import User, Student, Admin
from hostel.models import Hostel, Wing, Floor, Room, Application, Complaint


class Command(BaseCommand):
    help = 'Create sample data for testing the HostelMS application'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))

        # Create Admin User
        try:
            admin_user = User.objects.create_user(
                username='admin',
                password='admin123',
                email='admin@hostelms.com',
                is_admin=True,
                is_student=False
            )
            Admin.objects.create(
                user=admin_user,
                admin_id='ADM_admin',
                name='Admin User',
                email='admin@hostelms.com'
            )
            self.stdout.write(self.style.SUCCESS('[OK] Admin user created (username: admin, password: admin123)'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Admin already exists or error: {str(e)}'))

        # Create Student Users
        students_data = [
            {'username': 'john', 'name': 'John Doe', 'semester': 3, 'email': 'john@student.com'},
            {'username': 'alice', 'name': 'Alice Smith', 'semester': 5, 'email': 'alice@student.com'},
            {'username': 'bob', 'name': 'Bob Johnson', 'semester': 2, 'email': 'bob@student.com'},
        ]

        for student_data in students_data:
            try:
                user = User.objects.create_user(
                    username=student_data['username'],
                    password='student123',
                    email=student_data['email'],
                    is_student=True,
                    is_admin=False
                )
                Student.objects.create(
                    user=user,
                    student_id=f"STU_{student_data['username']}",
                    name=student_data['name'],
                    semester=student_data['semester'],
                    email=student_data['email'],
                    application_status=False
                )
                self.stdout.write(self.style.SUCCESS(f"[OK] Student created: {student_data['name']} (username: {student_data['username']}, password: student123)"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Student {student_data['username']} already exists or error: {str(e)}"))

        # Create Hostels
        try:
            admin_obj = Admin.objects.get(admin_id='ADM_admin')
            hostel1 = Hostel.objects.create(name='North Hostel', address='North Campus Area', admin=admin_obj, type='Boys')
            hostel2 = Hostel.objects.create(name='South Hostel', address='South Campus Area', admin=admin_obj, type='Girls')
            self.stdout.write(self.style.SUCCESS('[OK] Hostels created: North Hostel, South Hostel'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Hostels already exist or error: {str(e)}'))
            hostel1 = Hostel.objects.filter(name='North Hostel').first()
            hostel2 = Hostel.objects.filter(name='South Hostel').first()

        # Create Wings
        try:
            wing1 = Wing.objects.create(name='A Wing', hostel=hostel1)
            wing2 = Wing.objects.create(name='B Wing', hostel=hostel1)
            wing3 = Wing.objects.create(name='A Wing', hostel=hostel2)
            self.stdout.write(self.style.SUCCESS('[OK] Wings created for hostels'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Wings already exist or error: {str(e)}'))
            wing1 = Wing.objects.filter(name='A Wing', hostel=hostel1).first()
            wing2 = Wing.objects.filter(name='B Wing', hostel=hostel1).first()
            wing3 = Wing.objects.filter(name='A Wing', hostel=hostel2).first()

        # Create Floors
        try:
            floor1 = Floor.objects.create(number=1, wing=wing1)
            floor2 = Floor.objects.create(number=2, wing=wing1)
            floor3 = Floor.objects.create(number=1, wing=wing2)
            floor4 = Floor.objects.create(number=1, wing=wing3)
            self.stdout.write(self.style.SUCCESS('[OK] Floors created for wings'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Floors already exist or error: {str(e)}'))
            floor1 = Floor.objects.filter(number=1, wing=wing1).first()
            floor2 = Floor.objects.filter(number=2, wing=wing1).first()
            floor3 = Floor.objects.filter(number=1, wing=wing2).first()
            floor4 = Floor.objects.filter(number=1, wing=wing3).first()

        # Create Rooms
        rooms_data = [
            {'number': '101', 'room_type': 'Single', 'occupancy': 'Single', 'floor': floor1},
            {'number': '102', 'room_type': 'Double', 'occupancy': 'Double', 'floor': floor1},
            {'number': '103', 'room_type': 'Triple', 'occupancy': 'Triple', 'floor': floor1},
            {'number': '201', 'room_type': 'Single', 'occupancy': 'Single', 'floor': floor2},
            {'number': '202', 'room_type': 'Double', 'occupancy': 'Double', 'floor': floor2},
            {'number': '104', 'room_type': 'Single', 'occupancy': 'Single', 'floor': floor3},
            {'number': '105', 'room_type': 'Double', 'occupancy': 'Double', 'floor': floor3},
            {'number': '106', 'room_type': 'Single', 'occupancy': 'Single', 'floor': floor4},
        ]

        created_rooms = []
        for room_data in rooms_data:
            try:
                room = Room.objects.create(**room_data)
                created_rooms.append(room)
            except Exception as e:
                room = Room.objects.filter(number=room_data['number'], floor=room_data['floor']).first()
                if room:
                    created_rooms.append(room)

        self.stdout.write(self.style.SUCCESS(f'[OK] {len(created_rooms)} rooms created'))

        # Create Sample Applications
        try:
            john_student = Student.objects.get(student_id='STU_john')
            alice_student = Student.objects.get(student_id='STU_alice')

            Application.objects.create(
                room_type='Single',
                occupancy='Single',
                applicant=john_student,
                status=False  # Pending
            )

            Application.objects.create(
                room_type='Double',
                occupancy='Double',
                applicant=alice_student,
                status=True  # Approved
            )
            alice_student.application_status = True
            alice_student.save()

            self.stdout.write(self.style.SUCCESS('[OK] Sample applications created'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Applications already exist or error: {str(e)}'))

        # Create Sample Complaints
        try:
            bob_student = Student.objects.get(student_id='STU_bob')

            Complaint.objects.create(
                description='AC not working in my room',
                status='Pending',
                student=john_student
            )

            Complaint.objects.create(
                description='Water supply issue',
                status='In Progress',
                student=alice_student
            )

            Complaint.objects.create(
                description='Light bulb needs replacement',
                status='Resolved',
                student=bob_student
            )

            self.stdout.write(self.style.SUCCESS('[OK] Sample complaints created'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Complaints already exist or error: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('\n=== Sample Data Creation Complete ==='))
        self.stdout.write(self.style.SUCCESS('\nTest Credentials:'))
        self.stdout.write('  Admin:   username=admin,    password=admin123')
        self.stdout.write('  Student: username=john,     password=student123')
        self.stdout.write('  Student: username=alice,    password=student123')
        self.stdout.write('  Student: username=bob,      password=student123')
        self.stdout.write(self.style.SUCCESS('\nYou can now run: python manage.py runserver'))
