-- =====================================================
-- HostelMS Oracle Performance Indexes
-- Database: Oracle 11g/12c/19c
-- Purpose: Performance optimization indexes
-- =====================================================

-- =====================================================
-- Complaint Table Indexes
-- =====================================================

-- Index on student_id for fast complaint lookups by student
CREATE INDEX idx_complaint_student
ON hostel_complaint(student_id);

-- Index on status for filtering complaints by status
CREATE INDEX idx_complaint_status
ON hostel_complaint(status);

-- Composite index for status + student lookups
CREATE INDEX idx_complaint_status_student
ON hostel_complaint(status, student_id);

-- =====================================================
-- Application Table Indexes
-- =====================================================

-- Index on applicant_id for fast application lookups by student
CREATE INDEX idx_application_applicant
ON hostel_application(applicant_id);

-- Index on status for filtering applications
CREATE INDEX idx_application_status
ON hostel_application(status);

-- Index on room preferences for matching available rooms
CREATE INDEX idx_application_room_prefs
ON hostel_application(room_type, occupancy);

-- Composite index for status + room preferences
CREATE INDEX idx_application_status_prefs
ON hostel_application(status, room_type, occupancy);

-- =====================================================
-- Student Table Indexes
-- =====================================================

-- Index on student_id for lookups
CREATE INDEX idx_student_id
ON user_student(student_id);

-- Index on email for lookups
CREATE INDEX idx_student_email
ON user_student(email);

-- Index on application_status for filtering
CREATE INDEX idx_student_app_status
ON user_student(application_status);

-- Index on semester for filtering
CREATE INDEX idx_student_semester
ON user_student(semester);

-- =====================================================
-- Admin Table Indexes
-- =====================================================

-- Index on admin_id for lookups
CREATE INDEX idx_admin_id
ON user_admin(admin_id);

-- Index on email for lookups
CREATE INDEX idx_admin_email
ON user_admin(email);

-- =====================================================
-- Room Table Indexes
-- =====================================================

-- Index on floor_id for hierarchical queries
CREATE INDEX idx_room_floor
ON hostel_room(floor_id);

-- Index on room_type for filtering
CREATE INDEX idx_room_type
ON hostel_room(room_type);

-- Index on occupancy for filtering
CREATE INDEX idx_room_occupancy
ON hostel_room(occupancy);

-- Composite index for type + occupancy filtering
CREATE INDEX idx_room_type_occupancy
ON hostel_room(room_type, occupancy);

-- =====================================================
-- Room Residents (ManyToMany) Table Indexes
-- =====================================================

-- Index on room_id for resident lookups
CREATE INDEX idx_room_residents_room
ON hostel_room_residents(room_id);

-- Index on student_id for finding student's room
CREATE INDEX idx_room_residents_student
ON hostel_room_residents(student_id);

-- Composite index for both foreign keys
CREATE INDEX idx_room_residents_both
ON hostel_room_residents(room_id, student_id);

-- =====================================================
-- Floor Table Indexes
-- =====================================================

-- Index on wing_id for hierarchical queries
CREATE INDEX idx_floor_wing
ON hostel_floor(wing_id);

-- Composite index for wing + floor number
CREATE INDEX idx_floor_wing_number
ON hostel_floor(wing_id, number);

-- =====================================================
-- Wing Table Indexes
-- =====================================================

-- Index on hostel_id for hierarchical queries
CREATE INDEX idx_wing_hostel
ON hostel_wing(hostel_id);

-- =====================================================
-- Hostel Table Indexes
-- =====================================================

-- Index on admin_id for finding hostels by admin
CREATE INDEX idx_hostel_admin
ON hostel_hostel(admin_id);

-- Index on type for filtering by Boys/Girls
CREATE INDEX idx_hostel_type
ON hostel_hostel(type);

-- =====================================================
-- User Table Indexes (Django's auth_user table)
-- Note: Django creates some indexes automatically
-- =====================================================

-- Index on username (usually created by Django)
-- CREATE INDEX idx_user_username ON user_user(username);

-- Index on email
CREATE INDEX idx_user_email
ON user_user(email);

-- Index on is_student flag
CREATE INDEX idx_user_is_student
ON user_user(is_student);

-- Index on is_admin flag
CREATE INDEX idx_user_is_admin
ON user_user(is_admin);

-- =====================================================
-- Statistics Update
-- Note: Update statistics after creating indexes
-- =====================================================

-- Gather statistics for better query optimization
BEGIN
    DBMS_STATS.GATHER_SCHEMA_STATS(
        ownname => USER,
        cascade => TRUE,
        options => 'GATHER AUTO'
    );
END;
/

-- =====================================================
-- Display success message
-- =====================================================
BEGIN
    DBMS_OUTPUT.PUT_LINE('========================================');
    DBMS_OUTPUT.PUT_LINE('All indexes created successfully!');
    DBMS_OUTPUT.PUT_LINE('========================================');
    DBMS_OUTPUT.PUT_LINE('Performance indexes created for:');
    DBMS_OUTPUT.PUT_LINE('  - Complaint table (3 indexes)');
    DBMS_OUTPUT.PUT_LINE('  - Application table (4 indexes)');
    DBMS_OUTPUT.PUT_LINE('  - Student table (4 indexes)');
    DBMS_OUTPUT.PUT_LINE('  - Admin table (2 indexes)');
    DBMS_OUTPUT.PUT_LINE('  - Room table (4 indexes)');
    DBMS_OUTPUT.PUT_LINE('  - Room Residents table (3 indexes)');
    DBMS_OUTPUT.PUT_LINE('  - Floor table (2 indexes)');
    DBMS_OUTPUT.PUT_LINE('  - Wing table (1 index)');
    DBMS_OUTPUT.PUT_LINE('  - Hostel table (2 indexes)');
    DBMS_OUTPUT.PUT_LINE('  - User table (3 indexes)');
    DBMS_OUTPUT.PUT_LINE('========================================');
    DBMS_OUTPUT.PUT_LINE('Statistics gathered for schema');
    DBMS_OUTPUT.PUT_LINE('========================================');
END;
/
