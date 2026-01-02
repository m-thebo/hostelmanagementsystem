-- =====================================================
-- HostelMS Oracle Stored Procedures
-- Database: Oracle 11g/12c/19c
-- Purpose: Stored procedures for hostel management system
-- =====================================================

-- =====================================================
-- Procedure: get_all_complaints
-- Description: Retrieves all complaints with student details
-- Parameters: p_cursor OUT SYS_REFCURSOR
-- =====================================================
CREATE OR REPLACE PROCEDURE get_all_complaints(p_cursor OUT SYS_REFCURSOR)
IS
BEGIN
    OPEN p_cursor FOR
        SELECT
            c.id,
            c.description,
            c.status,
            s.student_id,
            s.name AS student_name,
            s.email AS student_email
        FROM hostel_complaint c
        INNER JOIN user_student s ON c.student_id = s.user_id
        ORDER BY c.id DESC;
END get_all_complaints;
/

-- =====================================================
-- Procedure: get_complaints_by_student
-- Description: Retrieves complaints for a specific student
-- Parameters:
--   p_student_user_id IN NUMBER - The user ID of the student
--   p_cursor OUT SYS_REFCURSOR
-- =====================================================
CREATE OR REPLACE PROCEDURE get_complaints_by_student(
    p_student_user_id IN NUMBER,
    p_cursor OUT SYS_REFCURSOR
)
IS
BEGIN
    OPEN p_cursor FOR
        SELECT
            c.id,
            c.description,
            c.status
        FROM hostel_complaint c
        WHERE c.student_id = p_student_user_id
        ORDER BY c.id DESC;
END get_complaints_by_student;
/

-- =====================================================
-- Procedure: get_complaints_by_status
-- Description: Retrieves complaints filtered by status
-- Parameters:
--   p_status IN VARCHAR2 - Status to filter by
--   p_cursor OUT SYS_REFCURSOR
-- =====================================================
CREATE OR REPLACE PROCEDURE get_complaints_by_status(
    p_status IN VARCHAR2,
    p_cursor OUT SYS_REFCURSOR
)
IS
BEGIN
    OPEN p_cursor FOR
        SELECT
            c.id,
            c.description,
            c.status,
            s.student_id,
            s.name AS student_name,
            s.email AS student_email
        FROM hostel_complaint c
        INNER JOIN user_student s ON c.student_id = s.user_id
        WHERE c.status = p_status
        ORDER BY c.id DESC;
END get_complaints_by_status;
/

-- =====================================================
-- Procedure: fetch_applications
-- Description: Retrieves all room applications with applicant details
-- Parameters: p_cursor OUT SYS_REFCURSOR
-- =====================================================
CREATE OR REPLACE PROCEDURE fetch_applications(p_cursor OUT SYS_REFCURSOR)
IS
BEGIN
    OPEN p_cursor FOR
        SELECT
            a.id,
            a.room_type,
            a.occupancy,
            a.status,
            s.user_id AS applicant_user_id,
            s.student_id,
            s.name AS applicant_name,
            s.email AS applicant_email,
            s.semester
        FROM hostel_application a
        INNER JOIN user_student s ON a.applicant_id = s.user_id
        ORDER BY a.status ASC, a.id DESC;
END fetch_applications;
/

-- =====================================================
-- Procedure: get_applications_by_student
-- Description: Retrieves applications for a specific student
-- Parameters:
--   p_student_user_id IN NUMBER - The user ID of the student
--   p_cursor OUT SYS_REFCURSOR
-- =====================================================
CREATE OR REPLACE PROCEDURE get_applications_by_student(
    p_student_user_id IN NUMBER,
    p_cursor OUT SYS_REFCURSOR
)
IS
BEGIN
    OPEN p_cursor FOR
        SELECT
            a.id,
            a.room_type,
            a.occupancy,
            a.status
        FROM hostel_application a
        WHERE a.applicant_id = p_student_user_id
        ORDER BY a.id DESC;
END get_applications_by_student;
/

-- =====================================================
-- Procedure: get_pending_applications
-- Description: Retrieves all pending (not yet approved) applications
-- Parameters: p_cursor OUT SYS_REFCURSOR
-- =====================================================
CREATE OR REPLACE PROCEDURE get_pending_applications(p_cursor OUT SYS_REFCURSOR)
IS
BEGIN
    OPEN p_cursor FOR
        SELECT
            a.id,
            a.room_type,
            a.occupancy,
            a.status,
            s.student_id,
            s.name AS applicant_name,
            s.email AS applicant_email,
            s.semester
        FROM hostel_application a
        INNER JOIN user_student s ON a.applicant_id = s.user_id
        WHERE a.status = 0
        ORDER BY a.id ASC;
END get_pending_applications;
/

-- =====================================================
-- Procedure: approve_application
-- Description: Approves an application and allocates a room
-- Parameters:
--   p_application_id IN NUMBER - ID of the application to approve
--   p_room_id IN NUMBER - ID of the room to allocate
-- =====================================================
CREATE OR REPLACE PROCEDURE approve_application(
    p_application_id IN NUMBER,
    p_room_id IN NUMBER
)
IS
    v_applicant_id NUMBER;
    v_count NUMBER;
BEGIN
    -- Get the applicant ID
    SELECT applicant_id INTO v_applicant_id
    FROM hostel_application
    WHERE id = p_application_id;

    -- Update application status to approved
    UPDATE hostel_application
    SET status = 1
    WHERE id = p_application_id;

    -- Update student's application_status
    UPDATE user_student
    SET application_status = 1
    WHERE user_id = v_applicant_id;

    -- Add student to room's residents (if using ManyToMany through table)
    -- Check if relationship already exists
    SELECT COUNT(*) INTO v_count
    FROM hostel_room_residents
    WHERE room_id = p_room_id AND student_id = v_applicant_id;

    IF v_count = 0 THEN
        INSERT INTO hostel_room_residents (room_id, student_id)
        VALUES (p_room_id, v_applicant_id);
    END IF;

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END approve_application;
/

-- =====================================================
-- Procedure: update_complaint_status
-- Description: Updates the status of a complaint
-- Parameters:
--   p_complaint_id IN NUMBER - ID of the complaint
--   p_status IN VARCHAR2 - New status value
-- =====================================================
CREATE OR REPLACE PROCEDURE update_complaint_status(
    p_complaint_id IN NUMBER,
    p_status IN VARCHAR2
)
IS
BEGIN
    UPDATE hostel_complaint
    SET status = p_status
    WHERE id = p_complaint_id;

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END update_complaint_status;
/

-- =====================================================
-- Procedure: get_dashboard_stats
-- Description: Retrieves dashboard statistics for admin
-- Parameters: p_cursor OUT SYS_REFCURSOR
-- =====================================================
CREATE OR REPLACE PROCEDURE get_dashboard_stats(p_cursor OUT SYS_REFCURSOR)
IS
BEGIN
    OPEN p_cursor FOR
        SELECT
            (SELECT COUNT(*) FROM user_student) AS total_students,
            (SELECT COUNT(*) FROM hostel_room) AS total_rooms,
            (SELECT COUNT(*)
             FROM hostel_application
             WHERE status = 0) AS pending_applications,
            (SELECT COUNT(*)
             FROM hostel_complaint
             WHERE status = 'Pending') AS pending_complaints,
            (SELECT COUNT(*)
             FROM hostel_complaint
             WHERE status = 'In Progress') AS inprogress_complaints,
            (SELECT COUNT(*)
             FROM hostel_complaint
             WHERE status = 'Resolved') AS resolved_complaints,
            (SELECT COUNT(*)
             FROM hostel_application
             WHERE status = 1) AS approved_applications,
            (SELECT COUNT(*)
             FROM user_student
             WHERE application_status = 1) AS students_with_rooms
        FROM DUAL;
END get_dashboard_stats;
/

-- =====================================================
-- Procedure: get_room_statistics
-- Description: Retrieves room occupancy statistics
-- Parameters: p_cursor OUT SYS_REFCURSOR
-- =====================================================
CREATE OR REPLACE PROCEDURE get_room_statistics(p_cursor OUT SYS_REFCURSOR)
IS
BEGIN
    OPEN p_cursor FOR
        SELECT
            r.room_type,
            r.occupancy,
            COUNT(r.id) AS total_rooms,
            COUNT(rr.student_id) AS occupied_beds,
            CASE r.occupancy
                WHEN 'Single' THEN COUNT(r.id) * 1
                WHEN 'Double' THEN COUNT(r.id) * 2
                WHEN 'Triple' THEN COUNT(r.id) * 3
                ELSE 0
            END AS total_capacity
        FROM hostel_room r
        LEFT JOIN hostel_room_residents rr ON r.id = rr.room_id
        GROUP BY r.room_type, r.occupancy
        ORDER BY r.room_type, r.occupancy;
END get_room_statistics;
/

-- =====================================================
-- Procedure: get_available_rooms
-- Description: Retrieves rooms with available capacity
-- Parameters:
--   p_room_type IN VARCHAR2 (optional) - Filter by room type
--   p_occupancy IN VARCHAR2 (optional) - Filter by occupancy
--   p_cursor OUT SYS_REFCURSOR
-- =====================================================
CREATE OR REPLACE PROCEDURE get_available_rooms(
    p_room_type IN VARCHAR2 DEFAULT NULL,
    p_occupancy IN VARCHAR2 DEFAULT NULL,
    p_cursor OUT SYS_REFCURSOR
)
IS
BEGIN
    OPEN p_cursor FOR
        SELECT
            r.id,
            r.number,
            r.room_type,
            r.occupancy,
            COUNT(rr.student_id) AS current_occupants,
            CASE r.occupancy
                WHEN 'Single' THEN 1
                WHEN 'Double' THEN 2
                WHEN 'Triple' THEN 3
                ELSE 0
            END AS max_capacity,
            f.number AS floor_number,
            w.name AS wing_name,
            h.name AS hostel_name
        FROM hostel_room r
        INNER JOIN hostel_floor f ON r.floor_id = f.id
        INNER JOIN hostel_wing w ON f.wing_id = w.id
        INNER JOIN hostel_hostel h ON w.hostel_id = h.id
        LEFT JOIN hostel_room_residents rr ON r.id = rr.room_id
        WHERE (p_room_type IS NULL OR r.room_type = p_room_type)
          AND (p_occupancy IS NULL OR r.occupancy = p_occupancy)
        GROUP BY r.id, r.number, r.room_type, r.occupancy,
                 f.number, w.name, h.name
        HAVING COUNT(rr.student_id) < CASE r.occupancy
            WHEN 'Single' THEN 1
            WHEN 'Double' THEN 2
            WHEN 'Triple' THEN 3
            ELSE 0
        END
        ORDER BY h.name, w.name, f.number, r.number;
END get_available_rooms;
/

-- =====================================================
-- Display success message
-- =====================================================
BEGIN
    DBMS_OUTPUT.PUT_LINE('========================================');
    DBMS_OUTPUT.PUT_LINE('All stored procedures created successfully!');
    DBMS_OUTPUT.PUT_LINE('========================================');
    DBMS_OUTPUT.PUT_LINE('Procedures created:');
    DBMS_OUTPUT.PUT_LINE('  1. get_all_complaints');
    DBMS_OUTPUT.PUT_LINE('  2. get_complaints_by_student');
    DBMS_OUTPUT.PUT_LINE('  3. get_complaints_by_status');
    DBMS_OUTPUT.PUT_LINE('  4. fetch_applications');
    DBMS_OUTPUT.PUT_LINE('  5. get_applications_by_student');
    DBMS_OUTPUT.PUT_LINE('  6. get_pending_applications');
    DBMS_OUTPUT.PUT_LINE('  7. approve_application');
    DBMS_OUTPUT.PUT_LINE('  8. update_complaint_status');
    DBMS_OUTPUT.PUT_LINE('  9. get_dashboard_stats');
    DBMS_OUTPUT.PUT_LINE(' 10. get_room_statistics');
    DBMS_OUTPUT.PUT_LINE(' 11. get_available_rooms');
    DBMS_OUTPUT.PUT_LINE('========================================');
END;
/
