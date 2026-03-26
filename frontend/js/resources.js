if (!isLoggedIn()) window.location.href = "/frontend/index.html";

const user = getUser();

// Show admin link for moderators/admins
if (user && (user.role === "moderator" || user.role === "admin")) {
    const adminLink = document.getElementById("admin-link");
    adminLink.href = "/frontend/admin.html";
    adminLink.classList.remove("hidden");
}

// Show add resource form for mentors/admins/moderators
if (user && (user.role === "mentor" || user.role === "moderator" || user.role === "admin")) {
    document.getElementById("add-resource-form").classList.remove("hidden");
}

function setFilter(btn, category) {
    document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    loadResources(category);
}

async function loadResources(category = null) {
    const url = category ? `/api/resources?category=${category}` : "/api/resources";
    const { ok, data } = await apiCall(url);
    const container = document.getElementById("resources-container");

    if (!ok) {
        container.innerHTML = `<div class="error">Failed to load resources</div>`;
        return;
    }

    if (data.resources.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📭</div>
                <p>No resources yet in this category.</p>
            </div>`;
        return;
    }

    container.innerHTML = data.resources.map(resource => `
        <div class="resource-card">
            <div class="resource-card-header">
                <span class="category-badge">${resource.category}</span>
                ${user && (user.role === "moderator" || user.role === "admin") ? `
                    <button class="btn btn-danger btn-small" 
                        onclick="deleteResource(${resource.id})">Remove</button>
                ` : ""}
            </div>
            <h3>${resource.title}</h3>
            <p>${resource.description}</p>
            ${resource.url ? `
                <a href="${resource.url}" target="_blank" rel="noopener noreferrer">
                    🔗 Visit resource →
                </a>
            ` : ""}
            <div class="resource-meta">
                ${new Date(resource.created_at).toLocaleDateString()}
            </div>
        </div>
    `).join("");
}

async function addResource() {
    const title       = document.getElementById("res-title").value;
    const description = document.getElementById("res-description").value;
    const url         = document.getElementById("res-url").value;
    const category    = document.getElementById("res-category").value;

    if (!title || !description) {
        showResourceMessage("Title and description are required", "error");
        return;
    }

    const { ok, data } = await apiCall("/api/resources", "POST", {
        title, description, url, category
    });

    if (ok) {
        showResourceMessage("Resource added!", "success");
        document.getElementById("res-title").value       = "";
        document.getElementById("res-description").value = "";
        document.getElementById("res-url").value         = "";
        loadResources();
    } else {
        showResourceMessage(data.error, "error");
    }
}

async function deleteResource(resourceId) {
    if (!confirm("Are you sure you want to remove this resource?")) return;

    const { ok } = await apiCall(`/api/resources/${resourceId}`, "DELETE");

    if (ok) {
        loadResources();
    }
}

function showResourceMessage(text, type) {
    const msg = document.getElementById("resource-message");
    msg.innerHTML = `<div class="${type}">${text}</div>`;
    setTimeout(() => msg.innerHTML = "", 3000);
}

function logout() {
    removeToken();
    window.location.href = "/frontend/index.html";
}

loadResources();