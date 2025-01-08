let socket;

// Connect to WebSocket server
function connectWebSocket() {
    socket = new WebSocket("ws://localhost:8765");

    socket.onmessage = (event) => {
        const gesture = event.data;
        if (gesture === "page_up") {
            chrome.scripting.executeScript({
                target: { tabId: null, allFrames: true },
                func: () => window.scrollBy(0, -window.innerHeight)
            });
        } else if (gesture === "page_down") {
            chrome.scripting.executeScript({
                target: { tabId: null, allFrames: true },
                func: () => window.scrollBy(0, window.innerHeight)
            });
        }
    };

    socket.onclose = () => {
        console.error("WebSocket connection closed. Reconnecting...");
        setTimeout(connectWebSocket, 1000); // Retry connection
    };
}

// Start WebSocket connection when the extension is loaded
connectWebSocket();
