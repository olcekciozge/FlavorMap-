document.addEventListener("DOMContentLoaded", function () {

    const box = document.getElementById("search-btn");
    const input = document.getElementById("search-input");

    if (!box || !input) {
        console.log("Search elements not found!");
        return;
    }

    box.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();

        box.classList.add("active");
        input.focus();
    });

    document.addEventListener("click", function (e) {
        if (!box.contains(e.target)) {
            box.classList.remove("active");
            input.value = "";
        }
    });

});