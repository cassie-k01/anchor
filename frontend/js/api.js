const API_URL = "";

// Save token to browser storage
function saveToken(token) {
    localStorage.setItem("token", token);
}

// Get token from browser storage
function getToken() {
    return localStorage.getItem("token");
}

// Remove token (logout)
function removeToken() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
}

// Save user info
function saveUser(user) {
    localStorage.setItem("user", JSON.stringify(user));
}

// Get user info
function getUser() {
    return JSON.parse(localStorage.getItem("user"));
}

// Check if logged in
function isLoggedIn() {
    return getToken() !== null;
}

// Main function to call the API
async function apiCall(endpoint, method = "GET", body = null) {
    const headers = {
        "Content-Type": "application/json",
    };

    // Add token if we have one
    if (getToken()) {
        headers["Authorization"] = `Bearer ${getToken()}`;
    }

    const options = { method, headers };
    if (body) options.body = JSON.stringify(body);

    const response = await fetch(`${API_URL}${endpoint}`, options);
    const data = await response.json();

    // If token expired redirect to login
    if (response.status === 401) {
        removeToken();
        window.location.href = "index.html";
    }

    return { ok: response.ok, data };
}