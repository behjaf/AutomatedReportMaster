function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function updateProgress() {
    const progressBars = document.querySelectorAll('.progress-bar');
    const rows = document.querySelectorAll('tr[data-report-id]');

    if (rows.length === 0) return;

    const csrftoken = getCookie('csrftoken');

    // Fetch current progress for all reports
    fetch('/api/reports/progress/', {
        headers: {
            'X-CSRFToken': csrftoken,
        }
    })
    .then(response => response.json())
    .then(data => {
        data.forEach(report => {
            const row = document.querySelector(`tr[data-report-id="${report.id}"]`);
            if (row) {
                const progressBar = row.querySelector('.progress-bar');
                const statusBadge = row.querySelector('.badge');

                // Smoothly update progress bar
                if (progressBar) {
                    progressBar.style.width = `${report.progress}%`;
                    progressBar.textContent = `${report.progress}%`;
                }

                // Update status badge
                if (statusBadge) {
                    statusBadge.textContent = report.status;
                    statusBadge.className = `badge bg-${report.status === 'completed' ? 'success' : 
                                                       report.status === 'processing' ? 'warning' : 
                                                       report.status === 'failed' ? 'danger' : 'secondary'}`;
                }

                // If completed, show download button
                if (report.status === 'completed' && report.file_path) {
                    const actionsCell = row.querySelector('td:last-child');
                    if (!actionsCell.querySelector('.btn')) {
                        actionsCell.innerHTML = `
                            <a href="${report.file_path}" class="btn btn-sm btn-success" download>
                                Download
                            </a>`;
                    }
                }
            }
        });
    });
}

// Check progress every second if we're on the dashboard
if (window.location.pathname === '/') {
    setInterval(updateProgress, 1000);
}