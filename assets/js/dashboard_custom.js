document.addEventListener("DOMContentLoaded", function () {
    const menuBtn = document.getElementById("menuBtn");
    const sidebar = document.getElementById("sidebar");
    const dropdownBtn = document.getElementById("dropdownBtn");
    const dropdownMenu = document.getElementById("dropdownMenu");
    const dropdownArrow = document.getElementById("dropdownArrow");

    // Toggle sidebar on button click
    menuBtn.addEventListener("click", (event) => {
        event.stopPropagation(); // Prevent immediate closing
        sidebar.classList.toggle("-translate-x-full");
    });

    // Close sidebar when clicking outside (only if open)
    document.addEventListener("click", (event) => {
        if (
            !sidebar.contains(event.target) && 
            !menuBtn.contains(event.target) && 
            !sidebar.classList.contains("-translate-x-full")
        ) {
            sidebar.classList.add("-translate-x-full");
        }
    });

    // Prevent sidebar from closing when clicking inside
    sidebar.addEventListener("click", (event) => {
        event.stopPropagation();
    });

    // Toggle Dropdown Menu
    if (dropdownBtn) {
        dropdownBtn.addEventListener("click", (event) => {
            event.stopPropagation(); // Prevent closing sidebar when clicking dropdown
            dropdownMenu.classList.toggle("hidden");
            dropdownArrow.classList.toggle("rotate-180");
            dropdownBtn.setAttribute("aria-expanded", dropdownMenu.classList.contains("hidden") ? "false" : "true");
        });
    }

    // Close dropdown when clicking outside
    document.addEventListener("click", (event) => {
        if (
            dropdownMenu &&
            !dropdownMenu.contains(event.target) &&
            !dropdownBtn.contains(event.target)
        ) {
            dropdownMenu.classList.add("hidden");
            dropdownArrow.classList.remove("rotate-180");
            dropdownBtn.setAttribute("aria-expanded", "false");
        }
    });
});
