/* Front-end Micro-Interactions & Theme Sync */

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initNavbarScroll();
    initScrollAnimations();
    initTypingEffect();
    initProjectFilters();
    initContactForm();
});

/* 1. Theme Management (Dark/Light Mode) */
function initTheme() {
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    if (!themeToggleBtn) return;

    const darkIcon = themeToggleBtn.querySelector('.theme-icon-dark');
    const lightIcon = themeToggleBtn.querySelector('.theme-icon-light');
    const htmlEl = document.documentElement;

    // Get theme from local storage or system preferences
    const savedTheme = localStorage.getItem('portfolio-theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const currentTheme = savedTheme || (prefersDark ? 'dark' : 'light');

    // Apply active theme
    setTheme(currentTheme);

    themeToggleBtn.addEventListener('click', () => {
        const targetTheme = htmlEl.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';
        setTheme(targetTheme);
    });

    function setTheme(theme) {
        htmlEl.setAttribute('data-bs-theme', theme);
        localStorage.setItem('portfolio-theme', theme);

        if (theme === 'dark') {
            darkIcon.classList.remove('d-none');
            lightIcon.classList.add('d-none');
        } else {
            darkIcon.classList.add('d-none');
            lightIcon.classList.remove('d-none');
        }
    }
}

/* 2. Navbar Styling on Scroll */
function initNavbarScroll() {
    const navbar = document.querySelector('.custom-navbar');
    if (!navbar) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Handle initial state on load
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    }
}

/* 3. Skill & Section Entrance Scroll Animations */
function initScrollAnimations() {
    // 3a. Sections Fade-In
    const revealElements = document.querySelectorAll('.scroll-reveal');
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const sectionObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    revealElements.forEach(el => sectionObserver.observe(el));

    // 3b. Skills Progress Bars Fill-in Animation
    const progressBars = document.querySelectorAll('.skill-progress-bar');
    const skillsObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const width = bar.getAttribute('data-target-width') || '80%';
                bar.style.width = width;
                observer.unobserve(bar);
            }
        });
    }, { threshold: 0.2 });

    progressBars.forEach(bar => skillsObserver.observe(bar));
}

/* 4. Typed Animation for Hero Role */
function initTypingEffect() {
    const typedTextEl = document.querySelector('.typed-text');
    if (!typedTextEl) return;

    // Get current text as a starting point, or default to standard titles
    const initialText = typedTextEl.textContent.trim();
    const rolesList = [
        initialText,
        'Full-Stack Web Developer',
        'UI/UX Designer',
        'Django & Python Specialist',
        'Problem Solver'
    ].filter(role => role.length > 0);

    let roleIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typingSpeed = 100;

    function type() {
        const currentRole = rolesList[roleIndex];
        
        if (isDeleting) {
            typedTextEl.textContent = currentRole.substring(0, charIndex - 1);
            charIndex--;
            typingSpeed = 50; // Deletes faster
        } else {
            typedTextEl.textContent = currentRole.substring(0, charIndex + 1);
            charIndex++;
            typingSpeed = 100;
        }

        if (!isDeleting && charIndex === currentRole.length) {
            typingSpeed = 2000; // Pause at end of word
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            roleIndex = (roleIndex + 1) % rolesList.length;
            typingSpeed = 500; // Brief pause before typing next word
        }

        setTimeout(type, typingSpeed);
    }

    // Start typing loop
    type();
}

/* 5. Client-Side Instant Project Searching & Filtering */
function initProjectFilters() {
    const searchField = document.getElementById('project-search');
    const filterButtons = document.querySelectorAll('#filter-pills .btn-filter');
    const projectCards = document.querySelectorAll('#projects-grid .project-item-card');

    if (!projectCards.length) return;

    let activeCategory = 'All';
    let searchQuery = '';

    // Filter pill click listener
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            activeCategory = btn.getAttribute('data-category');
            applyFilters();
        });
    });

    // Search field keyup listener
    if (searchField) {
        searchField.addEventListener('input', (e) => {
            searchQuery = e.target.value.toLowerCase().trim();
            applyFilters();
        });
    }

    function applyFilters() {
        projectCards.forEach(card => {
            const cardCategory = card.getAttribute('data-category');
            const cardTitle = card.getAttribute('data-title') || '';
            const cardDesc = card.getAttribute('data-desc') || '';
            const cardTech = card.getAttribute('data-tech') || '';

            const matchesCategory = (activeCategory === 'All' || cardCategory === activeCategory);
            const matchesSearch = (
                cardTitle.includes(searchQuery) ||
                cardDesc.includes(searchQuery) ||
                cardTech.includes(searchQuery)
            );

            if (matchesCategory && matchesSearch) {
                card.style.display = 'block';
                // Trigger reflow/fade animation
                setTimeout(() => {
                    card.style.opacity = '1';
                    card.style.transform = 'scale(1)';
                }, 10);
            } else {
                card.style.opacity = '0';
                card.style.transform = 'scale(0.9)';
                // Delay hiding element until fade ends
                setTimeout(() => {
                    if (card.style.opacity === '0') {
                        card.style.display = 'none';
                    }
                }, 300);
            }
        });
    }
}

/* 6. AJAX Contact Form Submission */
function initContactForm() {
    const contactForm = document.getElementById('contact-form');
    if (!contactForm) return;

    const submitBtn = document.getElementById('contact-submit-btn');
    const btnText = document.getElementById('btn-text');
    const btnSpinner = document.getElementById('btn-spinner');
    const alertWrapper = document.getElementById('contact-alert-wrapper');

    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();

        // Perform client-side validation
        if (!contactForm.checkValidity()) {
            contactForm.classList.add('was-validated');
            return;
        }

        // Show spinner / disable submit
        submitBtn.disabled = true;
        btnText.textContent = 'Sending...';
        btnSpinner.classList.remove('d-none');
        alertWrapper.innerHTML = '';

        const formData = new FormData(contactForm);

        fetch(contactForm.getAttribute('action'), {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json().then(data => ({ status: response.status, body: data })))
        .then(res => {
            // Restore button state
            submitBtn.disabled = false;
            btnText.textContent = 'Send Message';
            btnSpinner.classList.add('d-none');

            if (res.status === 200 && res.body.success) {
                // Display success notification
                showAlert('success', res.body.message);
                contactForm.reset();
                contactForm.classList.remove('was-validated');
            } else {
                // Display error notification
                showAlert('danger', res.body.message || 'An error occurred. Please check inputs.');
            }
        })
        .catch(error => {
            // Restore button state
            submitBtn.disabled = false;
            btnText.textContent = 'Send Message';
            btnSpinner.classList.add('d-none');
            showAlert('danger', 'Network connection issue. Please try again later.');
            console.error('Submit Error:', error);
        });
    });

    function showAlert(type, message) {
        alertWrapper.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show glass-alert" role="alert">
                <i class="bi ${type === 'success' ? 'bi-check-circle-fill' : 'bi-exclamation-triangle-fill'} me-2"></i>
                ${message}
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;

        // Automatically close the success message after 5 seconds
        if (type === 'success') {
            setTimeout(() => {
                const activeAlert = alertWrapper.querySelector('.alert');
                if (activeAlert) {
                    const bsAlert = new bootstrap.Alert(activeAlert);
                    bsAlert.close();
                }
            }, 6000);
        }
    }
}
