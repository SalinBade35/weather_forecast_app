from django.shortcuts import render, redirect
from .models import StudentLeave
from django.contrib import messages
from datetime import datetime, timedelta
from django.db.models import Q
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string 
from django.db.models import F
from django.utils import timezone  # Import timezone to use the current time


def home(request):
    searched = request.GET.get('searched')
    category = request.GET.get('category')

    if searched:
        # Search functionality based on the category
        if category == 'full_name':
            student_leaves = StudentLeave.objects.filter(full_name__icontains=searched)
        elif category == 'faculty':
            student_leaves = StudentLeave.objects.filter(faculty__icontains=searched)
        elif category == 'semester':
            student_leaves = StudentLeave.objects.filter(semester__iexact=searched)
        elif category == 'leave_type':
            student_leaves = StudentLeave.objects.filter(leave_type__icontains=searched)
        elif category == 'reason':
            student_leaves = StudentLeave.objects.filter(reason__icontains=searched)
        elif category == 'roll_number':
            student_leaves = StudentLeave.objects.filter(roll_number__iexact=searched)
        else:
            # Default search across multiple fields
            student_leaves = StudentLeave.objects.filter(
                Q(full_name__icontains=searched) |
                Q(faculty__icontains=searched) |
                Q(semester__iexact=searched) |
                Q(leave_type__icontains=searched) |
                Q(reason__icontains=searched) |
                Q(roll_number__iexact=searched)
            )
    else:
        # Display all non-deleted records
        student_leaves = StudentLeave.objects.filter(is_delete=False)

    # Render the home template with the filtered or full list
    return render(request, 'crudApp1/home.html', {'student_leaves': student_leaves})


def form(request):
    # if request.method == 'POST' and request.FILES:
    if request.method == 'POST' and request.FILES:
        roll_number = request.POST.get('rollNumber')
        full_name = request.POST.get('fullName')
        faculty = request.POST.get('faculty')
        semester = request.POST.get('semester')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')
        leave_type = request.POST.get('leaveType')
        reason = request.POST.get('reason')
        document = request.FILES.get('document')
        guardian_contact = request.POST.get('guardianContact')
        student_contact = request.POST.get('studentContact')
        student_email = request.POST.get('studentEmail') 

        StudentLeave.objects.create(
            roll_number=roll_number,
            full_name=full_name,
            faculty=faculty,
            semester=semester,
            start_date=start_date,
            end_date=end_date,
            leave_type=leave_type,
            reason=reason,
            document=document,
            guardian_contact=guardian_contact,
            student_contact=student_contact,
            student_email=student_email
        )
        
        subject="Trail email by Salin"
        # message="Thank you for submitting your form, this is just for trail"
        message = render_to_string('crudApp1/msg.html', {
            'full_name': full_name,
            'roll_number': roll_number,
            'faculty': faculty,
            'semester': semester,
            'start_date': start_date,
            'end_date': end_date,
            'leave_type': leave_type,
            'reason': reason,
            'guardian_contact': guardian_contact,
            'student_contact': student_contact,
        })
        from_email='salinbade1994@gmail.com'
        # recipient_list=['sambhukhawas634@gamil.com', 'salinbade1994@gmail.com', 'sampadashrestha435@gmail.com']
        recipient_list=[student_email, 'salinbade1994@gmail.com']
        fail_silently=False,
        
        # send_mail(subject, message, from_email, recipient_list, fail_silently=True) # error aye silently ignore gara, hamilai navana
        msg_email = EmailMessage(subject, message, from_email, recipient_list)
        msg_email.attach_file('django_syllabus.pdf')
        msg_email.send(fail_silently=True)
        # Extract the first name from full_name
        first_name = full_name.split()[0] if full_name else "User"  # Default to "User" if full_name is empty

        # Display the success message with the first name
        messages.success(request, f"Hey, {first_name.capitalize()}! Your Leave Form Is Successfully Submitted!!!, check mail for confirmation")

        return redirect('form')  # Redirect to the form page after submission
        
    return render(request, 'crudApp1/form.html')


def about(request):
    return render(request, 'crudApp1/about.html')


def contact(request):
    return render(request, 'crudApp1/contact.html')


def recycle(request):
    # Retrieve soft-deleted items
    data = StudentLeave.objects.filter(is_delete=True)
    
    # Determine when to hard delete
    var = timezone.now() - timedelta(minutes=1)  # Change this to the appropriate duration
    
    # Hard delete records older than 30 days
    StudentLeave.objects.filter(is_delete=True, deleted_time__lt=var).delete()
    
    return render(request, 'crudApp1/recycle.html', {"data": data})


# def recycle(request):
#     # Fetch records marked as deleted
#     data = StudentLeave.objects.filter(is_delete=True)

#     # Define the time limit for permanent deletion (e.g., 30 days)
#     var = datetime.now() - timedelta(minutes=2)  

#     # Fetch records that are older than the defined limit
#     v = StudentLeave.objects.filter(deleted_time__lt=var)

#     # Log the number of records being deleted
#     deleted_count = v.count()
#     if deleted_count > 0:
#         v.delete()
#         messages.success(request, f"Deleted {deleted_count} records permanently.")
#     else:
#         messages.info(request, "No records to delete.")

#     # Render the recycle bin template with current data
#     return render(request, 'crudApp1/recycle.html', {"data": data})


# def recycle(request):
#     data = StudentLeave.objects.filter(is_delete=True)
#     # var = datetime.now() - timedelta(days=30) # after 30 days the data will be deleted permanently
#     var = datetime.now() - timedelta(minutes=1) # after 30 days the data will be deleted permanently
#     v = StudentLeave.objects.filter(deleted_time__lt=var)
#     v.delete()
#     return render(request, 'crudApp1/recycle.html', {"data":data})

# def restore(request, id):  #id as parameter 
#     data = StudentLeave.objects.get(id = id) #retrieves the uniques data aka primary keys
#     data.is_delete=False
#     data.save()
#     messages.success(request, "Data is Restored")
#     return redirect('home')

def restore(request, id):
    # Fetch the record by ID
    leave = StudentLeave.objects.get(id=id)
    
    # Set `is_delete` to False to restore the data
    leave.is_delete = False
    leave.save()

    # Send a success message
    messages.success(request, "Record restored successfully!")

    # Redirect to the home page
    return redirect('home')

# def clear_items(request):
#     StudentLeave.objects.all().update(is_delete=True)  # Use .all() and .update() properly
#     return redirect('home')

def clear_items(request):
    # Use timezone.now() to get the current timestamp
    current_time = timezone.now()
    
    # Update all records to set is_delete to True and set deleted_time to the current time
    StudentLeave.objects.all().update(is_delete=True, deleted_time=current_time)
    
    # Redirect to the home page or wherever you want after the operation
    return redirect('home')

def delete_data(request, id):  #id as parameter 
    data = StudentLeave.objects.get(id = id) #retrieves the uniques data aka primary keys
    data.is_delete=True
    data.deleted_time = datetime.now()
    data.save()
    
    return redirect('home')

def restore_all(request):
    # Restore all deleted items by setting is_delete=False
    StudentLeave.objects.filter(is_delete=True).update(is_delete=False)

    # Optionally add a success message
    messages.success(request, "All deleted items have been restored.")

    return redirect('recycle')  # Redirect to the recycle bin or home page

def edit(request, id):
    # Fetch the existing StudentLeave record by ID
    data = StudentLeave.objects.get(id=id)
    
    if request.method == 'POST':
        # Get form data
        roll_number = request.POST.get('rollNumber')
        full_name = request.POST.get('fullName')
        faculty = request.POST.get('faculty')
        semester = request.POST.get('semester')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')
        leave_type = request.POST.get('leaveType')
        reason = request.POST.get('reason')
        document = request.FILES.get('document') if request.FILES.get('document') else data.document
        guardian_contact = request.POST.get('guardianContact')
        student_contact = request.POST.get('studentContact')
        student_email = request.POST.get('studentEmail')
        # this will now update the existing StudentLeave record
        data.roll_number = roll_number
        data.full_name = full_name
        data.faculty = faculty
        data.semester = semester
        data.start_date = start_date
        data.end_date = end_date
        data.leave_type = leave_type
        data.reason = reason
        data.document = document
        data.guardian_contact = guardian_contact
        data.student_contact = student_contact
        data.student_email = request.POST.get('studentEmail') 
        # now Save the updated data
        data.save()

        # Display success message and redirect to afulai man parne page
        messages.success(request, f"Successfully updated details for {full_name}.")
        return redirect('home')  # Adjust the redirect URL as needed
        
    
    # Render the edit form template
    return render(request, 'crudApp1/edit.html', {"data": data})

