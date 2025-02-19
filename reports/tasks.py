import pandas as pd
from celery import shared_task
from django.utils import timezone
import os
from .models import Report
import time

@shared_task
def generate_report(report_id):
    report = Report.objects.get(id=report_id)
    try:
        report.status = 'processing'
        report.progress = 0
        report.save()

        # Initialize data
        data = {
            'Date': pd.date_range(start='2023-01-01', periods=10),
            'Value': range(10)
        }
        df = pd.DataFrame(data)

        # Create reports directory if it doesn't exist
        os.makedirs('reports/generated', exist_ok=True)

        # Process data in steps to show progress
        progress_steps = [
            (10, 'Initializing'),
            (20, 'Loading data'),
            (40, 'Processing data'),
            (60, 'Analyzing results'),
            (80, 'Generating report'),
            (90, 'Finalizing')
        ]

        for progress, step in progress_steps:
            time.sleep(2)  # Small delay to show progress
            report.progress = progress
            report.save()

        # Save final report
        file_path = f'reports/generated/report_{report_id}.csv'
        df.to_csv(file_path, index=False)

        report.status = 'completed'
        report.file_path = file_path
        report.completed_at = timezone.now()
        report.progress = 100

    except Exception as e:
        report.status = 'failed'
        report.error_message = str(e)
        report.progress = 0

    finally:
        report.save()