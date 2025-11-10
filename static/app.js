/**
 * SaveTogether - Main JavaScript File
 * Handles frontend interactions and enhancements
 */

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize modern features
    initializeModernFeatures();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form enhancements
    initializeFormEnhancements();
    
    // Initialize animations
    initializeAnimations();
    
    // Initialize real-time features
    initializeRealTimeFeatures();
    
    // Initialize scroll animations
    initializeScrollAnimations();
}

// Modern features initialization
function initializeModernFeatures() {
    // Add smooth scrolling
    document.documentElement.style.scrollBehavior = 'smooth';
    
    // Initialize intersection observer for animations
    if ('IntersectionObserver' in window) {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in-up');
                }
            });
        }, observerOptions);
        
        // Observe elements for animation
        const animateElements = document.querySelectorAll('.feature-card, .stats-card, .contribution-item');
        animateElements.forEach(el => {
            observer.observe(el);
        });
    }
    
    // Initialize landing page enhancements
    initializeLandingPageEnhancements();
    
    // Add loading states to buttons
    initializeButtonLoadingStates();
    
    // Add modern form interactions
    initializeModernFormInteractions();
}

// Landing page specific enhancements
function initializeLandingPageEnhancements() {
    // Animate progress ring on scroll
    animateProgressRing();
    
    // Add interactive feature tags
    initializeFeatureTags();
    
    // Add floating card interactions
    initializeFloatingCardInteractions();
    
    // Add parallax effects
    initializeParallaxEffects();
}

// Animate progress ring
function animateProgressRing() {
    const progressRing = document.querySelector('.progress-ring-fill');
    if (progressRing) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Animate progress ring
                    setTimeout(() => {
                        progressRing.style.strokeDashoffset = '204.2';
                    }, 500);
                }
            });
        });
        
        observer.observe(progressRing);
    }
}

// Interactive feature tags
function initializeFeatureTags() {
    const featureTags = document.querySelectorAll('.feature-tag');
    featureTags.forEach(tag => {
        tag.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px) scale(1.05)';
            this.style.background = 'rgba(255,255,255,0.25)';
            this.style.color = 'white';
        });
        
        tag.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(-2px) scale(1)';
            this.style.background = 'rgba(255,255,255,0.15)';
            this.style.color = 'white';
        });
    });
}

// Floating card interactions
function initializeFloatingCardInteractions() {
    const floatingCards = document.querySelectorAll('.floating-card');
    floatingCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            // Add glow effect
            const glow = this.querySelector('.card-glow');
            if (glow) {
                glow.style.opacity = '1';
            }
            
            // Animate icon
            const icon = this.querySelector('.card-icon');
            if (icon) {
                icon.style.transform = 'scale(1.1) rotate(5deg)';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            const glow = this.querySelector('.card-glow');
            if (glow) {
                glow.style.opacity = '0';
            }
            
            const icon = this.querySelector('.card-icon');
            if (icon) {
                icon.style.transform = 'scale(1) rotate(0deg)';
            }
        });
    });
}

// Parallax effects
function initializeParallaxEffects() {
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.bg-shape, .particle');
        
        parallaxElements.forEach((element, index) => {
            const speed = 0.5 + (index * 0.1);
            element.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });
}

// Tooltip initialization
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Form enhancements
function initializeFormEnhancements() {
    // Auto-format currency inputs
    const currencyInputs = document.querySelectorAll('input[type="number"]');
    currencyInputs.forEach(input => {
        if (input.placeholder && input.placeholder.includes('MAD')) {
            input.addEventListener('input', formatCurrency);
        }
    });
    
    // Form validation feedback
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', handleFormSubmission);
    });
    
    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', autoResizeTextarea);
    });
}

// Currency formatting
function formatCurrency(event) {
    const input = event.target;
    let value = input.value.replace(/[^\d.]/g, '');
    
    if (value) {
        // Format with commas for thousands
        const parts = value.split('.');
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        input.value = parts.join('.');
    }
}

// Auto-resize textareas
function autoResizeTextarea(event) {
    const textarea = event.target;
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

// Form submission handling
function handleFormSubmission(event) {
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    if (submitBtn) {
        // Show loading state
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="loading"></span> Processing...';
        submitBtn.disabled = true;
        
        // Re-enable after a delay (for demo purposes)
        setTimeout(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }, 2000);
    }
}

// Animation initialization
function initializeAnimations() {
    // Animate progress bars on load
    animateProgressBars();
    
    // Add hover effects to cards
    addCardHoverEffects();
    
    // Initialize floating elements
    initializeFloatingElements();
}

// Button loading states
function initializeButtonLoadingStates() {
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (this.type === 'submit') {
                this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
                this.disabled = true;
                
                // Re-enable after a delay (for demo purposes)
                setTimeout(() => {
                    this.innerHTML = this.getAttribute('data-original-text') || this.innerHTML;
                    this.disabled = false;
                }, 2000);
            }
        });
    });
}

// Modern form interactions
function initializeModernFormInteractions() {
    const formControls = document.querySelectorAll('.form-control, .form-select');
    formControls.forEach(control => {
        // Add floating label effect
        control.addEventListener('focus', function() {
            this.parentNode.classList.add('focused');
        });
        
        control.addEventListener('blur', function() {
            if (!this.value) {
                this.parentNode.classList.remove('focused');
            }
        });
        
        // Add character counter for textareas
        if (control.tagName === 'TEXTAREA') {
            const maxLength = control.getAttribute('maxlength');
            if (maxLength) {
                const counter = document.createElement('div');
                counter.className = 'form-text text-end';
                counter.innerHTML = `<span class="char-count">0</span>/<span class="char-max">${maxLength}</span>`;
                control.parentNode.appendChild(counter);
                
                control.addEventListener('input', function() {
                    const count = this.value.length;
                    counter.querySelector('.char-count').textContent = count;
                    
                    if (count > maxLength * 0.9) {
                        counter.classList.add('text-warning');
                    } else {
                        counter.classList.remove('text-warning');
                    }
                });
            }
        }
    });
}

// Scroll animations
function initializeScrollAnimations() {
    // Parallax effect for hero section
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.hero-section::before');
        
        parallaxElements.forEach(element => {
            const speed = 0.5;
            element.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });
}

// Floating elements animation
function initializeFloatingElements() {
    const floatingCards = document.querySelectorAll('.floating-card');
    floatingCards.forEach((card, index) => {
        // Add random delay and duration
        const delay = Math.random() * 2;
        const duration = 3 + Math.random() * 2;
        
        card.style.animationDelay = `${delay}s`;
        card.style.animationDuration = `${duration}s`;
    });
}

// Card hover effects
function addCardHoverEffects() {
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Real-time features
function initializeRealTimeFeatures() {
    // Simulate real-time updates
    if (document.querySelector('.progress-bar')) {
        animateProgressBars();
    }
    
    // Initialize notification system
    initializeNotifications();
    
    // Initialize charts if present
    if (typeof Chart !== 'undefined') {
        initializeCharts();
    }
}

// Progress bar animations
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.width = width;
        }, 500);
    });
}

// Notification system
function initializeNotifications() {
    // Auto-hide flash messages
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        // Never hide progress guide or permanent alerts
        const progressGuide = alert.closest('#progress-levels-guide');
        const progressLegend = alert.id === 'progress-legend';
        const isPermanent = alert.classList.contains('alert-permanent');
        
        if (!isPermanent && !progressGuide && !progressLegend) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });
    
    // Notification click handlers
    const notificationButtons = document.querySelectorAll('[data-notification-action]');
    notificationButtons.forEach(button => {
        button.addEventListener('click', handleNotificationAction);
    });
}

// Handle notification actions
function handleNotificationAction(event) {
    const action = event.target.getAttribute('data-notification-action');
    const notificationId = event.target.getAttribute('data-notification-id');
    
    switch(action) {
        case 'mark-read':
            markNotificationRead(notificationId);
            break;
        case 'dismiss':
            dismissNotification(notificationId);
            break;
    }
}

// Mark notification as read
function markNotificationRead(notificationId) {
    fetch(`/notifications/mark_read/${notificationId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Remove notification from UI
            const notificationElement = document.querySelector(`[data-notification-id="${notificationId}"]`);
            if (notificationElement) {
                notificationElement.closest('.alert').remove();
            }
            
            // Update notification count
            updateNotificationCount();
        }
    })
    .catch(error => {
        console.error('Error marking notification as read:', error);
    });
}

// Dismiss notification
function dismissNotification(notificationId) {
    const notificationElement = document.querySelector(`[data-notification-id="${notificationId}"]`);
    if (notificationElement) {
        const bsAlert = new bootstrap.Alert(notificationElement.closest('.alert'));
        bsAlert.close();
    }
}

// Update notification count
function updateNotificationCount() {
    const badge = document.querySelector('.notification-badge');
    if (badge) {
        const currentCount = parseInt(badge.textContent);
        if (currentCount > 1) {
            badge.textContent = currentCount - 1;
        } else {
            badge.remove();
        }
    }
}

// Chart initialization
function initializeCharts() {
    // Initialize progress charts
    const progressCharts = document.querySelectorAll('[data-chart="progress"]');
    progressCharts.forEach(canvas => {
        const ctx = canvas.getContext('2d');
        const data = JSON.parse(canvas.getAttribute('data-chart-data'));
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Saved', 'Remaining'],
                datasets: [{
                    data: [data.saved, data.remaining],
                    backgroundColor: ['#4CAF50', '#e9ecef'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    });
}

// Utility functions
const utils = {
    // Format currency
    formatCurrency: function(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'MAD'
        }).format(amount);
    },
    
    // Format date
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },
    
    // Show toast notification
    showToast: function(message, type = 'info') {
        const toastContainer = document.querySelector('.toast-container') || createToastContainer();
        
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remove toast after it's hidden
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    },
    
    // Copy to clipboard
    copyToClipboard: function(text) {
        navigator.clipboard.writeText(text).then(() => {
            this.showToast('Copied to clipboard!', 'success');
        }).catch(() => {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            this.showToast('Copied to clipboard!', 'success');
        });
    }
};

// Create toast container if it doesn't exist
function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    container.style.zIndex = '1055';
    document.body.appendChild(container);
    return container;
}

// Export utils for global use
window.SaveTogetherUtils = utils;

// Service Worker registration for PWA features (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}
