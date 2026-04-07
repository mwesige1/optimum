// app.js
// Main JavaScript file for Optim Audit
// We will add dynamic functionality here as we build each module
console.log('Optim Audit loaded.');
// ============================================================
// app.js — Optim Audit
// ============================================================

// ============================================================
// Notification polling
// Checks for unread notifications every 30 seconds
// Updates the bell badge in the topbar
// ============================================================
function checkNotifications() {
    fetch('/findings/api/notifications/count/')
        .then(r => r.json())
        .then(data => {
            const dot   = document.getElementById('notif-dot');
            const count = document.getElementById('notif-count');

            if (!dot || !count) return;

            if (data.count > 0) {
                dot.style.display   = 'block';
                count.style.display = 'flex';
                count.textContent   = data.count;
            } else {
                dot.style.display   = 'none';
                count.style.display = 'none';
            }
        })
        .catch(err => console.log('Notification check error:', err));
}

// check immediately on page load
checkNotifications();

// then check every 30 seconds
setInterval(checkNotifications, 30000);



