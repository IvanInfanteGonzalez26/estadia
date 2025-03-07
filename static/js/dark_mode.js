document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("dark-mode-toggle");
    const icon = document.getElementById("dark-mode-icon");
    const body = document.documentElement; // Asegura que afecta <html>

    // Verificar si el usuario ya tiene un modo guardado
    if (localStorage.getItem("darkMode") === "enabled") {
        body.classList.add("dark-mode");
        icon.src = "/static/img/sun.png";  // Imagen de sol
    } else {
        icon.src = "/static/img/moon.png";  // Imagen de luna
    }

    toggleButton.addEventListener("click", function () {
        body.classList.toggle("dark-mode");

        if (body.classList.contains("dark-mode")) {
            localStorage.setItem("darkMode", "enabled");
            icon.src = "/static/img/sun.png";  // Cambiar a sol
        } else {
            localStorage.setItem("darkMode", "disabled");
            icon.src = "/static/img/moon.png";  // Cambiar a luna
        }
    });
});
