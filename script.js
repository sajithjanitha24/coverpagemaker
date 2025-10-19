document.addEventListener('DOMContentLoaded', () => {
    // Select all navigation links
    const navLinks = document.querySelectorAll('.nav-links a[href^="#"]');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Prevent the default instant jump
            e.preventDefault();

            // Get the target section's ID from the href
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);

            if (targetSection) {
                // Scroll smoothly to the target section
                window.scrollTo({
                    top: targetSection.offsetTop - 70, // Offset for sticky header
                    behavior: 'smooth'
                });
            }
        });
    });
});