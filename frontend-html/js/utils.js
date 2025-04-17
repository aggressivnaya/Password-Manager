// Utility functions

// Show toast notification
const showToast = (message, duration = 3000) => {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toast-message');
    
    toastMessage.textContent = message;
    toast.classList.remove('hidden');
    
    setTimeout(() => {
        toast.classList.add('hidden');
    }, duration);
};

// Format date
const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
};

// Check authentication and redirect if not authenticated
const checkAuth = () => {
    if (!isAuthenticated()) {
        window.location.href = 'auth.html';
        return false;
    }
    return true;
};

// Load navbar
const loadNavbar = () => {
    const navbarContainer = document.getElementById('navbar-container');
    if (!navbarContainer) return;
    
    navbarContainer.innerHTML = `
        <nav class="navbar">
            <div class="navbar-container">
                <a href="dashboard.html" class="navbar-brand">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                        <path d="M5 13a2 2 0 0 1 2 -2h10a2 2 0 0 1 2 2v6a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2v-6z" />
                        <path d="M11 16a1 1 0 1 0 2 0a1 1 0 0 0 -2 0" />
                        <path d="M8 11v-4a4 4 0 1 1 8 0v4" />
                    </svg>
                    <span>SecurePass</span>
                </a>
                
                <button class="navbar-menu-button" id="menu-toggle">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                        <path d="M4 6l16 0" />
                        <path d="M4 12l16 0" />
                        <path d="M4 18l16 0" />
                    </svg>
                </button>
                
                <div class="navbar-menu" id="navbar-menu">
                    <a href="dashboard.html" class="navbar-menu-item">Passwords</a>
                    <a href="history.html" class="navbar-menu-item">History</a>
                    <a href="groups.html" class="navbar-menu-item">Groups</a>
                    <a href="#" class="navbar-menu-item" id="logout-btn">Logout</a>
                </div>
            </div>
        </nav>
    `;
    
    // Toggle menu on mobile
    const menuToggle = document.getElementById('menu-toggle');
    const navbarMenu = document.getElementById('navbar-menu');
    
    menuToggle.addEventListener('click', () => {
        navbarMenu.classList.toggle('open');
    });
    
    // Logout functionality
    const logoutBtn = document.getElementById('logout-btn');
    logoutBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        try {
            await logout();
            window.location.href = 'auth.html';
        } catch (error) {
            console.error('Logout failed:', error);
            showToast('Logout failed. Please try again.');
        }
    });
};

// Initialize tabs
const initTabs = () => {
    const tabTriggers = document.querySelectorAll('.tab-trigger');
    
    tabTriggers.forEach(trigger => {
        trigger.addEventListener('click', () => {
            // Remove active class from all triggers and content
            document.querySelectorAll('.tab-trigger').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked trigger
            trigger.classList.add('active');
            
            // Show corresponding content
            const tabId = trigger.getAttribute('data-tab');
            const tabContent = document.getElementById(`${tabId}-tab`) || document.getElementById(`${tabId}-tab-content`);
            if (tabContent) {
                tabContent.classList.add('active');
            }
        });
    });
};

// Filter items by search term
const filterItems = (items, searchTerm, filterFn) => {
    if (!searchTerm) return items;
    
    const lowerSearchTerm = searchTerm.toLowerCase();
    return items.filter(item => filterFn(item, lowerSearchTerm));
};