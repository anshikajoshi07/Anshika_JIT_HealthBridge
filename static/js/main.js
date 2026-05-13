/* Main JavaScript for HealthBridge - Responsive Features */

document.addEventListener('DOMContentLoaded', function() {
    console.log('HealthBridge application loaded');
    
    // Hamburger menu toggle
    const navbarToggle = document.querySelector('.navbar-toggle');
    const navbarMenu = document.querySelector('.navbar-menu');
    
    if (navbarToggle && navbarMenu) {
        navbarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            navbarToggle.classList.toggle('active');
            navbarMenu.classList.toggle('active');
        });
        
        // Close menu when clicking on a link
        const menuLinks = navbarMenu.querySelectorAll('a');
        menuLinks.forEach(link => {
            link.addEventListener('click', function() {
                navbarToggle.classList.remove('active');
                navbarMenu.classList.remove('active');
            });
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            const isClickInsideMenu = navbarMenu.contains(e.target);
            const isClickOnToggle = navbarToggle.contains(e.target);
            
            if (!isClickInsideMenu && !isClickOnToggle && navbarMenu.classList.contains('active')) {
                navbarToggle.classList.remove('active');
                navbarMenu.classList.remove('active');
            }
        });
    }
    
    // Close alert messages
    const closeButtons = document.querySelectorAll('.close-alert');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const alert = this.closest('.alert');
            alert.style.animation = 'slideOut 0.3s ease-in-out';
            setTimeout(() => {
                alert.remove();
            }, 300);
        });
    });
    
    // Auto-close alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'slideOut 0.3s ease-in-out';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
    
    // Dropdown menu toggle for patient navbar
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            const dropdown = this.closest('.dropdown');
            dropdown.classList.toggle('active');
        });
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        const dropdowns = document.querySelectorAll('.dropdown');
        dropdowns.forEach(dropdown => {
            if (!dropdown.contains(e.target)) {
                dropdown.classList.remove('active');
            }
        });
    });
    
    // Handle window resize for responsive navbar
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            if (window.innerWidth >= 769) {
                // Reset mobile menu on desktop
                if (navbarToggle && navbarMenu) {
                    navbarToggle.classList.remove('active');
                    navbarMenu.classList.remove('active');
                }
            }
        }, 250);
    });
});

// Utility function to show notifications
function showNotification(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
}

// Utility function to handle API calls
async function apiCall(url, method = 'GET', data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(url, options);
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showNotification('An error occurred', 'error');
    }
}

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateY(0);
            opacity: 1;
        }
        to {
            transform: translateY(-100%);
            opacity: 0;
        }
    }
    
    /* Smooth scroll behavior */
    html {
        scroll-behavior: smooth;
    }
    
    /* Ensure images are responsive */
    img {
        max-width: 100%;
        height: auto;
    }
    
    /* Responsive video embeds */
    iframe {
        max-width: 100%;
    }
    
    /* Touch-friendly buttons on mobile */
    @media (max-width: 768px) {
        button,
        a.btn,
        input[type="button"],
        input[type="submit"] {
            min-height: 44px;
            min-width: 44px;
        }
    }
`;
document.head.appendChild(style);
