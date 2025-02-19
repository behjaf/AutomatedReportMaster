from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import Report
from .tasks import generate_report

@login_required
def dashboard(request):
    reports = Report.objects.filter(user=request.user)
    return render(request, 'reports/dashboard.html', {'reports': reports})

@login_required
def report_progress(request):
    reports = Report.objects.filter(user=request.user)
    data = [{
        'id': report.id,
        'status': report.status,
        'progress': report.progress,
        'file_path': report.file_path
    } for report in reports]
    return JsonResponse(data, safe=False)

@login_required
def request_report(request):
    if request.method == 'POST':
        report_type = request.POST.get('report_type')
        parameters = request.POST.get('parameters')

        report = Report.objects.create(
            user=request.user,
            report_type=report_type,
            parameters=parameters
        )

        # Queue the report generation task
        generate_report.delay(report.id)

        messages.success(request, 'Report request submitted successfully')
        return redirect('dashboard')

    return render(request, 'reports/request_report.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})