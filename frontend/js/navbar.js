// ── Dark mode ────────────────────────────────────────────
function initTheme() {
    const saved = localStorage.getItem("theme") || "light";
    document.documentElement.setAttribute("data-theme", saved);
}

function toggleTheme() {
    const current = document.documentElement.getAttribute("data-theme");
    const next    = current === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
}

// ── Hamburger menu ───────────────────────────────────────
function initHamburger() {
    const hamburger  = document.getElementById("hamburger");
    const mobileMenu = document.getElementById("mobile-menu");

    if (!hamburger || !mobileMenu) return;

    hamburger.addEventListener("click", () => {
        hamburger.classList.toggle("open");
        mobileMenu.classList.toggle("open");
    });

    // Close menu when a link is clicked
    mobileMenu.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", () => {
            hamburger.classList.remove("open");
            mobileMenu.classList.remove("open");
        });
    });
}

// Run on page load
initTheme();
document.addEventListener("DOMContentLoaded", initHamburger);