document.getElementById("start-backend").addEventListener("click", () => {
    fetch("http://localhost:8765")
        .then(() => {
            document.getElementById("status").textContent = "Status: Connected";
        })
        .catch(() => {
            document.getElementById("status").textContent = "Status: Backend Not Running";
        });
});
