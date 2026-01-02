# Database Scripts

This directory contains Oracle database scripts for production deployment.

## Current Configuration

The project is currently configured to use **SQLite** for development and testing.

## Oracle Database Setup (Optional)

If you want to use Oracle Database instead of SQLite:

### Prerequisites
- Oracle Database 11g/12c/19c installed and running
- SQL*Plus or another Oracle client

### Installation Steps

1. **Connect to Oracle Database**
   ```bash
   sqlplus system/your-password@localhost:1521/xe
   ```

2. **Run Stored Procedures**
   ```sql
   @oracle_procedures.sql
   ```
   This creates 11 stored procedures for:
   - Dashboard statistics
   - Application management
   - Complaint tracking
   - Student data retrieval

3. **Create Performance Indexes**
   ```sql
   @indexes.sql
   ```
   This creates 28+ indexes for optimized query performance.

4. **Exit SQL*Plus**
   ```sql
   EXIT;
   ```

5. **Update Django Settings**

   Edit `HostelMS/settings.py` and uncomment the Oracle database configuration:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.oracle',
           'NAME': config('DB_NAME', default='xe'),
           'USER': config('DB_USER', default='system'),
           'PASSWORD': config('DB_PASSWORD', default='pass'),
           'HOST': config('DB_HOST', default='localhost'),
           'PORT': config('DB_PORT', default='1521'),
       }
   }
   ```

6. **Update .env File**
   ```env
   DB_NAME=xe
   DB_USER=system
   DB_PASSWORD=your-oracle-password
   DB_HOST=localhost
   DB_PORT=1521
   ```

7. **Install Oracle Driver**
   ```bash
   pip install cx-Oracle
   ```

8. **Update Views**

   Uncomment the Oracle procedure imports in `hostel/views.py` and use `db_utils.py` functions instead of Django ORM queries.

## Files in This Directory

### oracle_procedures.sql
Contains 11 PL/SQL stored procedures:
1. `get_all_complaints` - Retrieve all complaints
2. `get_complaints_by_student` - Get student-specific complaints
3. `get_complaints_by_status` - Filter complaints by status
4. `fetch_applications` - Get all room applications
5. `get_applications_by_student` - Student-specific applications
6. `approve_application` - Approve and allocate room
7. `get_dashboard_stats` - Admin dashboard statistics
8. `update_complaint_status` - Update complaint status
9. Additional helper procedures

### indexes.sql
Creates 28+ database indexes on:
- `hostel_complaint` (student_id, status)
- `hostel_application` (applicant_id, status)
- `hostel_room` (floor_id, room_type, occupancy)
- `user_student` (student_id, application_status)
- And more for performance optimization

## Testing Oracle Connection

```bash
# Test connection
sqlplus system/password@localhost:1521/xe

# Verify procedures exist
SELECT object_name FROM user_procedures;

# Verify indexes exist
SELECT index_name, table_name FROM user_indexes;
```

## Switching Between SQLite and Oracle

The project supports both databases. To switch:

**To SQLite** (Current):
- Comment out Oracle config in `settings.py`
- Use Django ORM in views

**To Oracle**:
- Uncomment Oracle config in `settings.py`
- Use stored procedure wrappers from `db_utils.py`
- Ensure Oracle is running and procedures are created

## Performance Benefits

Using Oracle with stored procedures provides:
- ✅ Faster complex queries
- ✅ Reduced database round trips
- ✅ Better transaction handling
- ✅ Enterprise-level reliability
- ✅ Advanced analytics capabilities

## Notes

- SQLite is recommended for development and testing
- Oracle is recommended for production deployments
- The Django ORM approach works with both databases
- Stored procedures are Oracle-specific optimizations
