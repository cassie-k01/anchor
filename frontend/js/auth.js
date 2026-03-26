// Redirect if already logged in
if (isLoggedIn()) window.location.href = "/frontend/feed.html";

function showTab(tab) {
    const isLogin = tab === "login";

    document.getElementById("login-form").classList.toggle("hidden", !isLogin);
    document.getElementById("register-form").classList.toggle("hidden", isLogin);

    document.querySelectorAll(".tab").forEach((t, i) => {
        t.classList.toggle("active", isLogin ? i === 0 : i === 1);
    });

    document.getElementById("form-title").textContent    = isLogin ? "Welcome back"    : "Join ANCHOR";
    document.getElementById("form-subtitle").textContent = isLogin ? "Sign in to your ANCHOR account" : "Create your free account";
    document.getElementById("message").innerHTML = "";
}

function showMessage(text, type) {
    document.getElementById("message").innerHTML = `<div class="${type}">${text}</div>`;
}

async function login() {
    const email    = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    if (!email || !password) return showMessage("Please fill in all fields", "error");

    const { ok, data } = await apiCall("/api/auth/login", "POST", { email, password });

    if (ok) {
        saveToken(data.token);
        saveUser(data.user);
        window.location.href = "/frontend/feed.html";
    } else {
        showMessage(data.error, "error");
    }
}

async function register() {
    const email         = document.getElementById("reg-email").value;
    const display_name  = document.getElementById("reg-name").value;
    const password      = document.getElementById("reg-password").value;
    const academic_year = document.getElementById("reg-year").value;

    if (!email || !display_name || !password) return showMessage("Please fill in all fields", "error");

    const { ok, data } = await apiCall("/api/auth/register", "POST", { email, display_name, password, academic_year });

    if (ok) {
        showMessage("Account created! Please sign in.", "success");
        showTab("login");
    } else {
        showMessage(data.error, "error");
    }
}