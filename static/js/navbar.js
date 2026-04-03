// Mobile menu toggle
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');
const menuIconOpen = document.getElementById('menu-icon-open');
const menuIconClose = document.getElementById('menu-icon-close');

if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
        menuIconOpen.classList.toggle('hidden');
        menuIconClose.classList.toggle('hidden');
    });
}

// User dropdown toggle
const userDropdownToggle = document.getElementById('user-dropdown-toggle');
const userDropdown = document.getElementById('user-dropdown');

if (userDropdownToggle) {
    userDropdownToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        userDropdown.classList.toggle('hidden');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!userDropdown.contains(e.target) && !userDropdownToggle.contains(e.target)) {
            userDropdown.classList.add('hidden');
        }
    });
}

// Navbar scroll effect
const navbar = document.getElementById('navbar');

let lastScroll = 0;
window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 20) {
        navbar.classList.remove('bg-[#bce1ff]');
        navbar.classList.add('bg-white/95', 'backdrop-blur-md', 'shadow-md');
    } else {
        navbar.classList.add('bg-[#bce1ff]');
        navbar.classList.remove('bg-white/95', 'backdrop-blur-md', 'shadow-md');
    }

    lastScroll = currentScroll;
});
