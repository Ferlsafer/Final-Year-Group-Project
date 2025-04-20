document.addEventListener('DOMContentLoaded', function() {
    // Mobile sidebar toggle
    const sidebarToggle = document.querySelector('.btn-close');
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.remove('show');
        });
    }

    // Menu items click handler
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            menuItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Chat input handler
    const chatInput = document.querySelector('.chat-input-container input');
    const sendButton = document.querySelector('.chat-input-container .btn');
    const chatMessages = document.querySelector('.chat-messages');

    function sendMessage() {
        const message = chatInput.value.trim();
        if (message) {
            // Add user message
            const userMessageHTML = `
                <div class="message user-message">
                    ${message}
                    <small class="message-time">${getCurrentTime()}</small>
                </div>
            `;
            chatMessages.insertAdjacentHTML('beforeend', userMessageHTML);
            
            // Clear input
            chatInput.value = '';
            
            // Scroll to bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            // Simulate bot response (you can replace this with actual API call)
            setTimeout(() => {
                const botMessageHTML = `
                    <div class="message bot-message">
                        This is a sample response. In a real application, this would be replaced with an actual response from the backend.
                        <small class="message-time">${getCurrentTime()}</small>
                    </div>
                `;
                chatMessages.insertAdjacentHTML('beforeend', botMessageHTML);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 1000);
        }
    }

    // Send message on button click
    sendButton.addEventListener('click', sendMessage);

    // Send message on Enter key
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Handle navigation buttons
    const navButtons = document.querySelectorAll('.navbar-nav .btn-link');
    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Add your navigation logic here
            console.log('Clicked:', this.textContent.trim());
        });
    });
});

// Helper function to get current time
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('en-US', { 
        hour: 'numeric', 
        minute: '2-digit',
        hour12: true 
    });
} 