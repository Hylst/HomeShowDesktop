// Modern Template JavaScript for HomeShow Desktop
// Interactive features and functionality

(function() {
    'use strict';

    // DOM Elements
    let currentSlide = 0;
    let currentGalleryImage = 0;
    let heroSlides = [];
    let galleryImages = [];

    // Initialize when DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        initializeNavigation();
        initializeHeroSlider();
        initializeGallery();
        initializeMortgageCalculator();
        initializeContactForm();
        initializeSmoothScrolling();
        initializeScrollEffects();
    });

    /**
     * Initialize navigation functionality
     */
    function initializeNavigation() {
        const navbar = document.querySelector('.navbar');
        const navToggle = document.querySelector('.nav-toggle');
        const navMenu = document.querySelector('.nav-menu');

        // Navbar scroll effect
        window.addEventListener('scroll', function() {
            if (window.scrollY > 100) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });

        // Mobile menu toggle
        if (navToggle && navMenu) {
            navToggle.addEventListener('click', function() {
                navMenu.classList.toggle('active');
                navToggle.classList.toggle('active');
            });
        }

        // Close mobile menu when clicking on links
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (navMenu) {
                    navMenu.classList.remove('active');
                }
                if (navToggle) {
                    navToggle.classList.remove('active');
                }
            });
        });
    }

    /**
     * Initialize hero image slider
     */
    function initializeHeroSlider() {
        heroSlides = document.querySelectorAll('.hero-slide');
        const prevBtn = document.querySelector('.hero-prev');
        const nextBtn = document.querySelector('.hero-next');

        if (heroSlides.length === 0) return;

        // Show first slide
        if (heroSlides[0]) {
            heroSlides[0].classList.add('active');
        }

        // Auto-advance slides
        if (heroSlides.length > 1) {
            setInterval(nextHeroSlide, 5000);
        }

        // Navigation buttons
        if (prevBtn) {
            prevBtn.addEventListener('click', prevHeroSlide);
        }
        if (nextBtn) {
            nextBtn.addEventListener('click', nextHeroSlide);
        }

        // Keyboard navigation
        document.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowLeft') {
                prevHeroSlide();
            } else if (e.key === 'ArrowRight') {
                nextHeroSlide();
            }
        });
    }

    /**
     * Show next hero slide
     */
    function nextHeroSlide() {
        if (heroSlides.length === 0) return;
        
        heroSlides[currentSlide].classList.remove('active');
        currentSlide = (currentSlide + 1) % heroSlides.length;
        heroSlides[currentSlide].classList.add('active');
    }

    /**
     * Show previous hero slide
     */
    function prevHeroSlide() {
        if (heroSlides.length === 0) return;
        
        heroSlides[currentSlide].classList.remove('active');
        currentSlide = (currentSlide - 1 + heroSlides.length) % heroSlides.length;
        heroSlides[currentSlide].classList.add('active');
    }

    /**
     * Initialize image gallery
     */
    function initializeGallery() {
        const galleryItems = document.querySelectorAll('.gallery-item');
        const modal = document.querySelector('.gallery-modal');
        const modalImage = document.getElementById('modal-image');
        const modalClose = document.querySelector('.modal-close');
        const modalPrev = document.querySelector('.modal-prev');
        const modalNext = document.querySelector('.modal-next');

        if (!modal || !modalImage) return;

        // Collect gallery images
        galleryImages = Array.from(galleryItems).map(item => {
            const img = item.querySelector('img');
            return {
                src: img ? img.src : '',
                alt: img ? img.alt : ''
            };
        });

        // Open modal on gallery item click
        galleryItems.forEach((item, index) => {
            item.addEventListener('click', function() {
                openGalleryModal(index);
            });
        });

        // Close modal
        if (modalClose) {
            modalClose.addEventListener('click', closeGalleryModal);
        }

        // Modal navigation
        if (modalPrev) {
            modalPrev.addEventListener('click', prevGalleryImage);
        }
        if (modalNext) {
            modalNext.addEventListener('click', nextGalleryImage);
        }

        // Close modal on background click
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeGalleryModal();
            }
        });

        // Keyboard navigation
        document.addEventListener('keydown', function(e) {
            if (modal.style.display === 'flex') {
                if (e.key === 'Escape') {
                    closeGalleryModal();
                } else if (e.key === 'ArrowLeft') {
                    prevGalleryImage();
                } else if (e.key === 'ArrowRight') {
                    nextGalleryImage();
                }
            }
        });
    }

    /**
     * Open gallery modal
     */
    function openGalleryModal(index) {
        const modal = document.querySelector('.gallery-modal');
        const modalImage = document.getElementById('modal-image');
        
        if (!modal || !modalImage || !galleryImages[index]) return;

        currentGalleryImage = index;
        modalImage.src = galleryImages[index].src;
        modalImage.alt = galleryImages[index].alt;
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }

    /**
     * Close gallery modal
     */
    function closeGalleryModal() {
        const modal = document.querySelector('.gallery-modal');
        if (!modal) return;

        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    /**
     * Show next gallery image
     */
    function nextGalleryImage() {
        if (galleryImages.length === 0) return;
        
        currentGalleryImage = (currentGalleryImage + 1) % galleryImages.length;
        updateModalImage();
    }

    /**
     * Show previous gallery image
     */
    function prevGalleryImage() {
        if (galleryImages.length === 0) return;
        
        currentGalleryImage = (currentGalleryImage - 1 + galleryImages.length) % galleryImages.length;
        updateModalImage();
    }

    /**
     * Update modal image
     */
    function updateModalImage() {
        const modalImage = document.getElementById('modal-image');
        if (!modalImage || !galleryImages[currentGalleryImage]) return;

        modalImage.src = galleryImages[currentGalleryImage].src;
        modalImage.alt = galleryImages[currentGalleryImage].alt;
    }

    /**
     * Initialize mortgage calculator
     */
    function initializeMortgageCalculator() {
        const form = document.getElementById('mortgage-form');
        const result = document.getElementById('mortgage-result');
        
        if (!form || !result) return;

        // Calculate on form input change
        const inputs = form.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('input', calculateMortgage);
            input.addEventListener('change', calculateMortgage);
        });

        // Initial calculation
        calculateMortgage();
    }

    /**
     * Calculate mortgage payment
     */
    function calculateMortgage() {
        const priceInput = document.getElementById('property-price');
        const downPaymentInput = document.getElementById('down-payment');
        const interestRateInput = document.getElementById('interest-rate');
        const loanTermInput = document.getElementById('loan-term');
        const result = document.getElementById('mortgage-result');

        if (!priceInput || !downPaymentInput || !interestRateInput || !loanTermInput || !result) {
            return;
        }

        const price = parseFloat(priceInput.value) || 0;
        const downPayment = parseFloat(downPaymentInput.value) || 0;
        const annualRate = parseFloat(interestRateInput.value) || 0;
        const years = parseInt(loanTermInput.value) || 0;

        if (price <= 0 || years <= 0) {
            result.textContent = 'Please enter valid values';
            return;
        }

        const loanAmount = price - downPayment;
        const monthlyRate = annualRate / 100 / 12;
        const numPayments = years * 12;

        if (monthlyRate === 0) {
            const monthlyPayment = loanAmount / numPayments;
            result.textContent = `Monthly Payment: $${monthlyPayment.toFixed(2)}`;
            return;
        }

        const monthlyPayment = loanAmount * 
            (monthlyRate * Math.pow(1 + monthlyRate, numPayments)) / 
            (Math.pow(1 + monthlyRate, numPayments) - 1);

        const totalPayment = monthlyPayment * numPayments;
        const totalInterest = totalPayment - loanAmount;

        result.innerHTML = `
            <div><strong>Monthly Payment: $${monthlyPayment.toFixed(2)}</strong></div>
            <div>Total Interest: $${totalInterest.toFixed(2)}</div>
            <div>Total Payment: $${totalPayment.toFixed(2)}</div>
        `;
    }

    /**
     * Initialize contact form
     */
    function initializeContactForm() {
        const form = document.getElementById('contact-form');
        if (!form) return;

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            // Validate form
            if (!validateContactForm(data)) {
                return;
            }
            
            // Show success message
            showContactSuccess();
            
            // Reset form
            form.reset();
        });
    }

    /**
     * Validate contact form
     */
    function validateContactForm(data) {
        const errors = [];
        
        if (!data.name || data.name.trim().length < 2) {
            errors.push('Name must be at least 2 characters long');
        }
        
        if (!data.email || !isValidEmail(data.email)) {
            errors.push('Please enter a valid email address');
        }
        
        if (!data.phone || data.phone.trim().length < 10) {
            errors.push('Please enter a valid phone number');
        }
        
        if (!data.message || data.message.trim().length < 10) {
            errors.push('Message must be at least 10 characters long');
        }
        
        if (errors.length > 0) {
            showContactErrors(errors);
            return false;
        }
        
        return true;
    }

    /**
     * Validate email format
     */
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    /**
     * Show contact form errors
     */
    function showContactErrors(errors) {
        const errorDiv = document.getElementById('contact-errors') || createErrorDiv();
        errorDiv.innerHTML = `
            <div style="color: #dc3545; background: #f8d7da; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                <strong>Please fix the following errors:</strong>
                <ul style="margin: 0.5rem 0 0 1rem;">
                    ${errors.map(error => `<li>${error}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    /**
     * Show contact form success
     */
    function showContactSuccess() {
        const errorDiv = document.getElementById('contact-errors') || createErrorDiv();
        errorDiv.innerHTML = `
            <div style="color: #155724; background: #d4edda; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                <strong>Thank you!</strong> Your message has been sent successfully. We'll get back to you soon.
            </div>
        `;
        
        // Remove success message after 5 seconds
        setTimeout(() => {
            errorDiv.innerHTML = '';
        }, 5000);
    }

    /**
     * Create error div for contact form
     */
    function createErrorDiv() {
        const form = document.getElementById('contact-form');
        if (!form) return null;
        
        const errorDiv = document.createElement('div');
        errorDiv.id = 'contact-errors';
        form.insertBefore(errorDiv, form.firstChild);
        return errorDiv;
    }

    /**
     * Initialize smooth scrolling
     */
    function initializeSmoothScrolling() {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href === '#') return;
                
                const target = document.querySelector(href);
                if (!target) return;
                
                e.preventDefault();
                
                const offsetTop = target.offsetTop - 80; // Account for fixed navbar
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            });
        });
    }

    /**
     * Initialize scroll effects
     */
    function initializeScrollEffects() {
        // Intersection Observer for fade-in animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);
        
        // Observe elements for animation
        const animatedElements = document.querySelectorAll('.property-details, .gallery, .location, .contact');
        animatedElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        });
    }

    /**
     * Utility function to format currency
     */
    function formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(amount);
    }

    /**
     * Utility function to format number
     */
    function formatNumber(number) {
        return new Intl.NumberFormat('en-US').format(number);
    }

    /**
     * Utility function to debounce function calls
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * Initialize lazy loading for images
     */
    function initializeLazyLoading() {
        const images = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }

    // Initialize lazy loading if supported
    if ('IntersectionObserver' in window) {
        initializeLazyLoading();
    }

    // Export functions for global access if needed
    window.HomeShowApp = {
        nextHeroSlide,
        prevHeroSlide,
        openGalleryModal,
        closeGalleryModal,
        calculateMortgage,
        formatCurrency,
        formatNumber
    };

})();