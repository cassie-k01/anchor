if (!isLoggedIn()) window.location.href = "index.html";

const user = getUser();
if (user) {
    document.getElementById("welcome-msg").innerHTML =
        `Welcome back, <strong>${user.display_name}</strong>! This is a safe space to share and support each other. 💙`;
}
// Show admin link only for moderators and admins
if (user && (user.role === "moderator" || user.role === "admin")) {
    const adminLink = document.getElementById("admin-link");
    adminLink.href = "admin.html";
    adminLink.classList.remove("hidden");
}
function setFilter(btn, category) {
    document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    loadPosts(category);
}

async function loadPosts(category = null) {
    const url = category ? `/api/posts?category=${category}` : "/api/posts";
    const { ok, data } = await apiCall(url);
    const container = document.getElementById("posts-container");

    if (!ok) {
        container.innerHTML = `<div class="error">Failed to load posts</div>`;
        return;
    }

    if (data.posts.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">🌊</div>
                <p>No posts in this category yet!</p>
            </div>`;
        return;
    }

    container.innerHTML = data.posts.map(post => `
        <div class="post-card" onclick="window.location.href='post.html?id=${post.id}'">
            <div class="post-card-header">
                <span class="category-badge">${post.category}</span>
                <span class="anon-badge">${post.is_anonymous ? '🎭 ' + post.author : '👤 ' + post.author}</span>
            </div>
            <h3>${post.title}</h3>
            <p>${post.body.length > 150 ? post.body.substring(0, 150) + '...' : post.body}</p>
            <div class="post-meta">
                <span>💬 ${post.comment_count} responses</span>
                <span>👁 ${post.view_count} views</span>
                <span>${new Date(post.created_at).toLocaleDateString()}</span>
            </div>
        </div>
    `).join("");
}

function logout() {
    removeToken();
    window.location.href = "index.html";
}

loadPosts();