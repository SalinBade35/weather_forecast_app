from django.db import models

class StudentLeave(models.Model):
    roll_number = models.CharField(max_length=6, unique=True)
    full_name = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    semester = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=50)
    reason = models.TextField()
    document = models.FileField(upload_to='documents/', null=True)
    # document = models.FileField(upload_to='image', null=True)
    guardian_contact = models.CharField(max_length=15)
    student_contact = models.CharField(max_length=15)
    is_delete=models.BooleanField(default=False) 
    deleted_time= models.DateTimeField(null=True)
    student_email = models.EmailField(max_length=100)
    


# Hard Delete: Permanently removes a record from the database. Once deleted, it cannot be recovered.
# Soft Delete: Marks a record as deleted without removing it from the database, often by setting a flag (e.g., is_deleted = True). The record can be recovered later if needed.


