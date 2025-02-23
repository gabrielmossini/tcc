// Function to get the cookie value
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Format the birthday input when it loses focus
document.getElementById("birthday").addEventListener("blur", function () {
    let date = this.value.split('/');
    if (date.length === 3) {
        this.value = `${date[2]}-${date[1]}-${date[0]}`; // Converts to YYYY-MM-DD for MySQL
    }
});

// Show success message if URL contains a 'message' parameter
document.addEventListener("DOMContentLoaded", function () {
    function showMessageFromURL() {
        const urlParams = new URLSearchParams(window.location.search);
        const message = urlParams.get("message");

        if (message) {
            const messageContainer = document.getElementById("message-container");

            if (messageContainer) {
                messageContainer.innerHTML = `<div class="alert alert-success">${message}</div>`;

                // Remove message after 3 seconds
                setTimeout(() => {
                    messageContainer.innerHTML = "";
                    window.history.replaceState({}, document.title, window.location.pathname); // Clean URL
                }, 3000);
            }
        }
    }

    showMessageFromURL();
});
