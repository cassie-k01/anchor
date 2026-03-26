if (!isLoggedIn()) window.location.href = "/frontend/index.html";

const params = new URLSearchParams(window.location.search);
const postId = params.get("id");

if (!postId) window.location.href = "/frontend/feed.html";

let replyToId = null;

async function loadPost() {
    const { ok, data } = await apiCall(`/api/posts/${postId}`);

    if (!ok) {
        document.getElementById("post-container").innerHTML =
            `<div class="error">Post not found</div>`;
        return;
    }

    const post = data;
    document.getElementById("post-container").innerHTML = `
        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                <span class="category-badge">${post.category}</span>
                <span class="anon-badge">${post.is_anonymous ? '🎭 ' + post.author : '👤 ' + post.author}</span>
            </div>
            <h2 style="color:#2C3E7A; margin-bottom:15px;">${post.title}</h2>
            <p style="font-size:15px; line-height:1.7; color:#444;">${post.body}</p>
            <div class="post-meta" style="margin-top:15px;">
                <span>💬 ${post.comment_count} responses</span>
                <span>👁 ${post.view_count} views</span>
                <span>${new Date(post.created_at).toLocaleDateString()}</span>
            </div>
            <div style="margin-top:15px;">
                <button class="btn btn-danger btn-small" onclick="reportPost()">⚠️ Report</button>
            </div>
        </div>
    `;

    document.getElementById("comments-section").classList.remove("hidden");
    loadComments();
}

async function loadComments() {
    const { ok, data } = await apiCall(`/api/posts/${postId}/comments`);
    const container = document.getElementById("comments-container");

    if (!ok || data.comments.length === 0) {
        container.innerHTML = `<p style="text-align:center; color:#999; margin-top:20px;">
            No responses yet. Be the first to respond!
        </p>`;
        return;
    }

    container.innerHTML = data.comments.map(comment => `
        <div class="comment card">
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span class="anon-badge">
                    ${comment.is_anonymous ? '🎭 ' + comment.author : '👤 ' + comment.author}
                </span>
                <span style="font-size:12px; color:#999;">
                    ${new Date(comment.created_at).toLocaleDateString()}
                </span>
            </div>
            <p style="font-size:14px; color:#444;">${comment.body}</p>
            <button class="btn btn-small"
                style="margin-top:8px; background:#f0f0f0; color:#555;"
                onclick="setReply(${comment.id})">
                ↩ Reply
            </button>
            ${comment.replies && comment.replies.length > 0 ? `
                <div style="margin-top:10px;">
                    ${comment.replies.map(reply => `
                        <div class="reply">
                            <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                                <span class="anon-badge" style="font-size:11px;">
                                    ${reply.is_anonymous ? '🎭 ' + reply.author : '👤 ' + reply.author}
                                </span>
                            </div>
                            <p style="font-size:13px; color:#555;">${reply.body}</p>
                        </div>
                    `).join("")}
                </div>
            ` : ""}
        </div>
    `).join("");
}

function setReply(commentId) {
    replyToId = commentId;
    document.getElementById("comment-body").placeholder = "Writing a reply...";
    document.getElementById("comment-body").focus();
}

async function addComment() {
    const body         = document.getElementById("comment-body").value;
    const is_anonymous = document.getElementById("comment-anonymous").checked;

    if (!body) return;

    const payload = { body, is_anonymous };
    if (replyToId) payload.parent_comment_id = replyToId;

    const { ok, data } = await apiCall(`/api/posts/${postId}/comments`, "POST", payload);

    if (ok) {
        document.getElementById("comment-body").value = "";
        replyToId = null;
        document.getElementById("comment-body").placeholder = "Share your advice or perspective...";
        loadComments();
    } else {
        document.getElementById("comment-message").innerHTML =
            `<div class="error">${data.error}</div>`;
    }
}

async function reportPost() {
    const reason = prompt("Why are you reporting this post?");
    if (!reason) return;

    const { ok } = await apiCall("/api/reports", "POST", {
        content_type: "post",
        content_id:   postId,
        reason
    });

    alert(ok ? "Report submitted. Thank you!" : "Failed to submit report.");
}

function logout() {
    removeToken();
    window.location.href = "/frontend/index.html";
}

loadPost();