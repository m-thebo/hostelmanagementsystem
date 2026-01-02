"""
Database utility functions for HostelMS.
Provides Python wrappers for Oracle stored procedures.
"""
import cx_Oracle
import logging
from django.db import connection
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


def call_get_all_complaints() -> List[Dict]:
    """
    Retrieve all complaints with student details.

    Returns:
        List[Dict]: List of complaint dictionaries with keys:
            - id: Complaint ID
            - description: Complaint description
            - status: Current status
            - student_id: Student ID
            - student_name: Name of student
            - student_email: Email of student
    """
    try:
        cursor = connection.cursor()

        plsql = """
            DECLARE
                complaints_cursor SYS_REFCURSOR;
            BEGIN
                get_all_complaints(complaints_cursor);
                :complaints := complaints_cursor;
            END;
        """

        complaints_var = cursor.var(cx_Oracle.CURSOR)
        cursor.execute(plsql, {'complaints': complaints_var})

        rows = complaints_var.getvalue().fetchall()
        cursor.close()

        # Convert tuples to dictionaries
        complaints = []
        for row in rows:
            complaints.append({
                'id': row[0],
                'description': row[1],
                'status': row[2],
                'student_id': row[3],
                'student_name': row[4],
                'student_email': row[5],
            })

        logger.info(f'Fetched {len(complaints)} complaints from database')
        return complaints

    except Exception as e:
        logger.error(f'Error calling get_all_complaints: {str(e)}')
        raise


def call_get_complaints_by_student(student_user_id: int) -> List[Dict]:
    """
    Retrieve complaints for a specific student.

    Args:
        student_user_id: The user ID of the student

    Returns:
        List[Dict]: List of complaint dictionaries with keys:
            - id: Complaint ID
            - description: Complaint description
            - status: Current status
    """
    try:
        cursor = connection.cursor()

        plsql = """
            DECLARE
                complaints_cursor SYS_REFCURSOR;
            BEGIN
                get_complaints_by_student(:student_id, complaints_cursor);
                :complaints := complaints_cursor;
            END;
        """

        complaints_var = cursor.var(cx_Oracle.CURSOR)
        cursor.execute(plsql, {
            'student_id': student_user_id,
            'complaints': complaints_var
        })

        rows = complaints_var.getvalue().fetchall()
        cursor.close()

        complaints = []
        for row in rows:
            complaints.append({
                'id': row[0],
                'description': row[1],
                'status': row[2],
            })

        logger.info(f'Fetched {len(complaints)} complaints for student {student_user_id}')
        return complaints

    except Exception as e:
        logger.error(f'Error calling get_complaints_by_student: {str(e)}')
        raise


def call_get_complaints_by_status(status: str) -> List[Dict]:
    """
    Retrieve complaints filtered by status.

    Args:
        status: Status to filter by (Pending, In Progress, Resolved)

    Returns:
        List[Dict]: List of complaint dictionaries
    """
    try:
        cursor = connection.cursor()

        plsql = """
            DECLARE
                complaints_cursor SYS_REFCURSOR;
            BEGIN
                get_complaints_by_status(:status, complaints_cursor);
                :complaints := complaints_cursor;
            END;
        """

        complaints_var = cursor.var(cx_Oracle.CURSOR)
        cursor.execute(plsql, {
            'status': status,
            'complaints': complaints_var
        })

        rows = complaints_var.getvalue().fetchall()
        cursor.close()

        complaints = []
        for row in rows:
            complaints.append({
                'id': row[0],
                'description': row[1],
                'status': row[2],
                'student_id': row[3],
                'student_name': row[4],
                'student_email': row[5],
            })

        logger.info(f'Fetched {len(complaints)} complaints with status {status}')
        return complaints

    except Exception as e:
        logger.error(f'Error calling get_complaints_by_status: {str(e)}')
        raise


def call_fetch_applications() -> List[Dict]:
    """
    Retrieve all room applications with applicant details.

    Returns:
        List[Dict]: List of application dictionaries with keys:
            - id: Application ID
            - room_type: Requested room type
            - occupancy: Requested occupancy
            - status: Application status (0=Pending, 1=Approved)
            - applicant_user_id: User ID of applicant
            - student_id: Student ID
            - applicant_name: Name of applicant
            - applicant_email: Email of applicant
            - semester: Applicant's semester
    """
    try:
        cursor = connection.cursor()

        plsql = """
            DECLARE
                applications_cursor SYS_REFCURSOR;
            BEGIN
                fetch_applications(applications_cursor);
                :applications := applications_cursor;
            END;
        """

        applications_var = cursor.var(cx_Oracle.CURSOR)
        cursor.execute(plsql, {'applications': applications_var})

        rows = applications_var.getvalue().fetchall()
        cursor.close()

        applications = []
        for row in rows:
            applications.append({
                'id': row[0],
                'room_type': row[1],
                'occupancy': row[2],
                'status': row[3],
                'applicant_user_id': row[4],
                'student_id': row[5],
                'applicant_name': row[6],
                'applicant_email': row[7],
                'semester': row[8],
            })

        logger.info(f'Fetched {len(applications)} applications from database')
        return applications

    except Exception as e:
        logger.error(f'Error calling fetch_applications: {str(e)}')
        raise


def call_get_applications_by_student(student_user_id: int) -> List[Dict]:
    """
    Retrieve applications for a specific student.

    Args:
        student_user_id: The user ID of the student

    Returns:
        List[Dict]: List of application dictionaries
    """
    try:
        cursor = connection.cursor()

        plsql = """
            DECLARE
                applications_cursor SYS_REFCURSOR;
            BEGIN
                get_applications_by_student(:student_id, applications_cursor);
                :applications := applications_cursor;
            END;
        """

        applications_var = cursor.var(cx_Oracle.CURSOR)
        cursor.execute(plsql, {
            'student_id': student_user_id,
            'applications': applications_var
        })

        rows = applications_var.getvalue().fetchall()
        cursor.close()

        applications = []
        for row in rows:
            applications.append({
                'id': row[0],
                'room_type': row[1],
                'occupancy': row[2],
                'status': row[3],
            })

        logger.info(f'Fetched {len(applications)} applications for student {student_user_id}')
        return applications

    except Exception as e:
        logger.error(f'Error calling get_applications_by_student: {str(e)}')
        raise


def call_get_pending_applications() -> List[Dict]:
    """
    Retrieve all pending (unapproved) applications.

    Returns:
        List[Dict]: List of pending application dictionaries
    """
    try:
        cursor = connection.cursor()

        plsql = """
            DECLARE
                applications_cursor SYS_REFCURSOR;
            BEGIN
                get_pending_applications(applications_cursor);
                :applications := applications_cursor;
            END;
        """

        applications_var = cursor.var(cx_Oracle.CURSOR)
        cursor.execute(plsql, {'applications': applications_var})

        rows = applications_var.getvalue().fetchall()
        cursor.close()

        applications = []
        for row in rows:
            applications.append({
                'id': row[0],
                'room_type': row[1],
                'occupancy': row[2],
                'status': row[3],
                'student_id': row[4],
                'applicant_name': row[5],
                'applicant_email': row[6],
                'semester': row[7],
            })

        logger.info(f'Fetched {len(applications)} pending applications')
        return applications

    except Exception as e:
        logger.error(f'Error calling get_pending_applications: {str(e)}')
        raise


def call_approve_application(application_id: int, room_id: int) -> bool:
    """
    Approve an application and allocate a room.

    Args:
        application_id: ID of the application to approve
        room_id: ID of the room to allocate

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = connection.cursor()

        plsql = """
            BEGIN
                approve_application(:app_id, :room_id);
            END;
        """

        cursor.execute(plsql, {
            'app_id': application_id,
            'room_id': room_id
        })

        cursor.close()

        logger.info(f'Approved application {application_id} and allocated room {room_id}')
        return True

    except Exception as e:
        logger.error(f'Error calling approve_application: {str(e)}')
        raise


def call_update_complaint_status(complaint_id: int, status: str) -> bool:
    """
    Update the status of a complaint.

    Args:
        complaint_id: ID of the complaint
        status: New status (Pending, In Progress, Resolved)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = connection.cursor()

        plsql = """
            BEGIN
                update_complaint_status(:comp_id, :status);
            END;
        """

        cursor.execute(plsql, {
            'comp_id': complaint_id,
            'status': status
        })

        cursor.close()

        logger.info(f'Updated complaint {complaint_id} status to {status}')
        return True

    except Exception as e:
        logger.error(f'Error calling update_complaint_status: {str(e)}')
        raise


def call_get_dashboard_stats() -> Dict:
    """
    Retrieve dashboard statistics for admin.

    Returns:
        Dict: Dashboard statistics with keys:
            - total_students: Total number of students
            - total_rooms: Total number of rooms
            - pending_applications: Number of pending applications
            - pending_complaints: Number of pending complaints
            - inprogress_complaints: Number of in-progress complaints
            - resolved_complaints: Number of resolved complaints
            - approved_applications: Number of approved applications
            - students_with_rooms: Number of students with allocated rooms
    """
    try:
        cursor = connection.cursor()

        plsql = """
            DECLARE
                stats_cursor SYS_REFCURSOR;
            BEGIN
                get_dashboard_stats(stats_cursor);
                :stats := stats_cursor;
            END;
        """

        stats_var = cursor.var(cx_Oracle.CURSOR)
        cursor.execute(plsql, {'stats': stats_var})

        row = stats_var.getvalue().fetchone()
        cursor.close()

        if row:
            stats = {
                'total_students': row[0] or 0,
                'total_rooms': row[1] or 0,
                'pending_applications': row[2] or 0,
                'pending_complaints': row[3] or 0,
                'inprogress_complaints': row[4] or 0,
                'resolved_complaints': row[5] or 0,
                'approved_applications': row[6] or 0,
                'students_with_rooms': row[7] or 0,
            }

            logger.info('Fetched dashboard statistics')
            return stats
        else:
            logger.warning('No dashboard statistics returned')
            return {}

    except Exception as e:
        logger.error(f'Error calling get_dashboard_stats: {str(e)}')
        raise


def call_get_room_statistics() -> List[Dict]:
    """
    Retrieve room occupancy statistics.

    Returns:
        List[Dict]: List of room statistics by type and occupancy
    """
    try:
        cursor = connection.cursor()

        plsql = """
            DECLARE
                stats_cursor SYS_REFCURSOR;
            BEGIN
                get_room_statistics(stats_cursor);
                :stats := stats_cursor;
            END;
        """

        stats_var = cursor.var(cx_Oracle.CURSOR)
        cursor.execute(plsql, {'stats': stats_var})

        rows = stats_var.getvalue().fetchall()
        cursor.close()

        statistics = []
        for row in rows:
            statistics.append({
                'room_type': row[0],
                'occupancy': row[1],
                'total_rooms': row[2],
                'occupied_beds': row[3],
                'total_capacity': row[4],
            })

        logger.info(f'Fetched room statistics for {len(statistics)} categories')
        return statistics

    except Exception as e:
        logger.error(f'Error calling get_room_statistics: {str(e)}')
        raise


def call_get_available_rooms(room_type: Optional[str] = None,
                             occupancy: Optional[str] = None) -> List[Dict]:
    """
    Retrieve rooms with available capacity.

    Args:
        room_type: Optional filter by room type (AC/Non-AC)
        occupancy: Optional filter by occupancy (Single/Double/Triple)

    Returns:
        List[Dict]: List of available rooms
    """
    try:
        cursor = connection.cursor()

        plsql = """
            DECLARE
                rooms_cursor SYS_REFCURSOR;
            BEGIN
                get_available_rooms(:room_type, :occupancy, rooms_cursor);
                :rooms := rooms_cursor;
            END;
        """

        rooms_var = cursor.var(cx_Oracle.CURSOR)
        cursor.execute(plsql, {
            'room_type': room_type,
            'occupancy': occupancy,
            'rooms': rooms_var
        })

        rows = rooms_var.getvalue().fetchall()
        cursor.close()

        rooms = []
        for row in rows:
            rooms.append({
                'id': row[0],
                'number': row[1],
                'room_type': row[2],
                'occupancy': row[3],
                'current_occupants': row[4],
                'max_capacity': row[5],
                'floor_number': row[6],
                'wing_name': row[7],
                'hostel_name': row[8],
            })

        logger.info(f'Fetched {len(rooms)} available rooms')
        return rooms

    except Exception as e:
        logger.error(f'Error calling get_available_rooms: {str(e)}')
        raise
