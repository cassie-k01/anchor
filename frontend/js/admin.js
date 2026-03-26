if (!isLoggedIn()) window.location.href = "/frontend/index.html";

// Check user is moderator or admin
const user = getUser();
if (user && user.role !== "moderator" && user.role !== "admin") {
    window.location.href = "/frontend/feed.html";
}

let currentFilter = "pending";

async function loadStats() {
    const statuses = ["pending", "reviewed", "resolved"];
    const ids      = ["pending-count", "reviewed-count", "resolved-count"];

    for (let i = 0; i < statuses.length; i++) {
        const { ok, data } = await apiCall(`/api/admin/reports?status=${statuses[i]}`);
        if (ok) {
            document.getElementById(ids[i]).textContent = data.reports.length;
        }
    }
}

function setFilter(btn, status) {
    document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    currentFilter = status;
    loadReports(status);
}

async function loadReports(status = "pending") {
    const { ok, data } = await apiCall(`/api/admin/reports?status=${status}`);
    const container    = document.getElementById("reports-container");

    if (!ok) {
        container.innerHTML = `<div class="error">Failed to load reports</div>`;
        return;
    }

    if (data.reports.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">✅</div>
                <p>No ${status} reports</p>
            </div>`;
        return;
    }

    container.innerHTML = data.reports.map(report => `
        <div class="report-card" id="report-${report.id}">
            <div class="report-meta">
                <span class="status-badge status-${report.status}">${report.status}</span>
                <span>${report.content_type} #${report.content_id}</span>
                <span>${new Date(report.created_at).toLocaleDateString()}</span>
            </div>
            <div class="report-reason">${report.reason}</div>
            <div class="report-actions">
                ${report.status === "pending" ? `
                    <button class="btn btn-secondary btn-small" onclick="markReviewed(${report.id})">
                        👁 Mark Reviewed
                    </button>
                    <button class="btn btn-danger btn-small" onclick="removeContent('${report.content_type}', ${report.content_id}, ${report.id})">
                        🗑 Remove ${report.content_type}
                    </button>
                    <button class="btn btn-ghost btn-small" onclick="resolveReport(${report.id})">
                        ✓ Resolve
                    </button>
                    <button class="btn btn-danger btn-small" onclick="suspendUser(${report.reporter_id})">
                        🚫 Suspend User
                    </button>
                ` : ""}
                ${report.status === "reviewed" ? `
                    <button class="btn btn-danger btn-small" onclick="removeContent('${report.content_type}', ${report.content_id}, ${report.id})">
                        🗑 Remove ${report.content_type}
                    </button>
                    <button class="btn btn-ghost btn-small" onclick="resolveReport(${report.id})">
                        ✓ Resolve
                    </button>
                    <button class="btn btn-danger btn-small" onclick="suspendUser(${report.reporter_id})">
                        🚫 Suspend User
                    </button>
                ` : ""}
            </div>
        </div>
    `).join("");
}

async function markReviewed(reportId) {
    const { ok } = await apiCall(`/api/admin/reports/${reportId}`, "PATCH", { status: "reviewed" });
    if (ok) {
        showMessage("Report marked as reviewed", "success");
        loadReports(currentFilter);
        loadStats();
    }
}

async function resolveReport(reportId) {
    const { ok } = await apiCall(`/api/admin/reports/${reportId}`, "PATCH", { status: "resolved" });
    if (ok) {
        showMessage("Report resolved", "success");
        loadReports(currentFilter);
        loadStats();
    }
}

async function removeContent(contentType, contentId, reportId) {
    if (!confirm(`Are you sure you want to remove this ${contentType}?`)) return;

    const { ok } = await apiCall(`/api/admin/content/${contentType}/${contentId}`, "DELETE");

    if (ok) {
        // Also resolve the report automatically
        await apiCall(`/api/admin/reports/${reportId}`, "PATCH", { status: "resolved" });
        showMessage(`${contentType} removed successfully`, "success");
        loadReports(currentFilter);
        loadStats();
    } else {
        showMessage(`Failed to remove ${contentType}`, "error");
    }
}

async function suspendUser(userId) {
    // Confirm before suspending since this is a serious action
    if (!confirm("Are you sure you want to suspend this user? They will no longer be able to login.")) return;

    const { ok } = await apiCall(`/api/admin/users/${userId}/suspend`, "PATCH");

    if (ok) {
        showMessage("User suspended successfully", "success");
        loadReports(currentFilter);
        loadStats();
    } else {
        showMessage("Failed to suspend user", "error");
    }
}

function showMessage(text, type) {
    const msg = document.getElementById("message");
    msg.innerHTML = `<div class="${type}">${text}</div>`;
    setTimeout(() => msg.innerHTML = "", 3000);
}

function logout() {
    removeToken();
    window.location.href = "/frontend/index.html";
}

// Load everything on page start
loadStats();
loadReports("pending");