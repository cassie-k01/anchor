if (!isLoggedIn()) window.location.href = "index.html";

function showMessage(text, type) {
    document.getElementById("message").innerHTML = `<div class="${type}">${text}</div>`;
}

async function createPost() {
    const title        = document.getElementById("title").value;
    const body         = document.getElementById("body").value;
    const category     = document.getElementById("category").value;
    const is_anonymous = document.getElementById("is_anonymous").checked;

    if (!title || !body) return showMessage("Title and body are required", "error");

    const { ok, data } = await apiCall("/api/posts", "POST", { title, body, category, is_anonymous });

    if (ok) {
        showMessage("Post created successfully!", "success");
        setTimeout(() => window.location.href = "feed.html", 1500);
    } else {
        showMessage(data.error, "error");
    }
}

function logout() {
    removeToken();
    window.location.href = "index.html";
}