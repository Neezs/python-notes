document.addEventListener("DOMContentLoaded", () => {
    const navLinks = document.querySelectorAll("nav a");
    const currentURL = window.location.pathname;

    navLinks.forEach(link => {
        if (link.getAttribute("href") === currentURL) {
            link.style.fontWeight = "bold";
            link.style.textDecoration = "underline";
        }
    });

    const firstInput = document.querySelector("form input, form select");
    if (firstInput) {
        firstInput.focus();
    }

    const forms = document.querySelectorAll("form");
    forms.forEach(form => {
        form.addEventListener("submit", function (e) {
            let valid = true;
            const inputs = form.querySelectorAll("input[required], select[required]");

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    input.classList.add("input-error");
                    valid = false;
                } else {
                    input.classList.remove("input-error");
                }
            });

            if (!valid) {
                e.preventDefault();
                alert("Please fill out all required fields.");
            }
        });
    });
});

function filterTable() {
    const input = document.getElementById("tableSearch");
    const filter = input.value.toLowerCase();
    const rows = document.querySelectorAll("table tbody tr");

    rows.forEach(row => {
        const rowText = row.innerText.toLowerCase();
        row.style.display = rowText.includes(filter) ? "" : "none";
    });
}
