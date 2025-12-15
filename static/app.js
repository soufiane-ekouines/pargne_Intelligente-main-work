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

// Three.js animation for savings visualization
function initSavingsAnimation() {
    // Check if we're on the homepage and the container exists
    const container = document.getElementById('savings-animation');
    if (!container) return;

    // Set up Three.js scene
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setClearColor(0x0a192f, 1);
    container.appendChild(renderer.domElement);

    // Add lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(1, 1, 1);
    scene.add(directionalLight);

    // Create coins (representing savings)
    const coins = [];
    const coinGeometry = new THREE.CylinderGeometry(0.5, 0.5, 0.1, 32);
    const coinMaterial = new THREE.MeshPhongMaterial({ 
        color: 0xf1c40f,
        shininess: 100,
        emissive: 0xd35400,
        emissiveIntensity: 0.2
    });

    // Create a stack of coins that grows over time
    for (let i = 0; i < 15; i++) {
        const coin = new THREE.Mesh(coinGeometry, coinMaterial);
        coin.rotation.x = Math.PI / 2;
        coin.position.y = i * 0.15;
        coin.position.x = Math.sin(i * 0.5) * 0.5;
        coin.position.z = Math.cos(i * 0.5) * 0.5;
        coin.scale.set(0.01, 0.01, 0.01); // Start small
        scene.add(coin);
        coins.push({
            mesh: coin,
            targetScale: 1,
            speed: 0.02 + Math.random() * 0.03,
            delay: i * 30 // Stagger the animation
        });
    }

    // Create a piggy bank
    const piggyBankGroup = new THREE.Group();
    
    // Body
    const bodyGeometry = new THREE.SphereGeometry(1, 32, 32);
    const bodyMaterial = new THREE.MeshPhongMaterial({ color: 0xff9ff3 });
    const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
    piggyBankGroup.add(body);
    
    // Head
    const headGeometry = new THREE.SphereGeometry(0.7, 32, 32);
    const headMaterial = new THREE.MeshPhongMaterial({ color: 0xff9ff3 });
    const head = new THREE.Mesh(headGeometry, headMaterial);
    head.position.set(0, 0, 1);
    piggyBankGroup.add(head);
    
    // Legs
    const legGeometry = new THREE.CylinderGeometry(0.15, 0.15, 0.5, 16);
    const legMaterial = new THREE.MeshPhongMaterial({ color: 0xff9ff3 });
    
    for (let i = 0; i < 4; i++) {
        const leg = new THREE.Mesh(legGeometry, legMaterial);
        const x = i % 2 === 0 ? -0.4 : 0.4;
        const z = i < 2 ? -0.4 : 0.4;
        leg.position.set(x, -0.7, z);
        leg.rotation.x = Math.PI / 2;
        piggyBankGroup.add(leg);
    }
    
    // Slot
    const slotGeometry = new THREE.BoxGeometry(0.4, 0.05, 0.05);
    const slotMaterial = new THREE.MeshPhongMaterial({ color: 0x000000 });
    const slot = new THREE.Mesh(slotGeometry, slotMaterial);
    slot.position.set(0, 0.2, 0.9);
    piggyBankGroup.add(slot);
    
    piggyBankGroup.position.set(3, -1, 0);
    piggyBankGroup.scale.set(0.8, 0.8, 0.8);
    scene.add(piggyBankGroup);

    // Position camera
    camera.position.z = 5;
    camera.position.y = 1;

    // Animation variables
    let frameCount = 0;
    const clock = new THREE.Clock();

    // Handle window resize
    function onWindowResize() {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    }
    window.addEventListener('resize', onWindowResize);

    // Animation loop
    function animate() {
        requestAnimationFrame(animate);
        
        const delta = clock.getDelta();
        frameCount++;
        
        // Animate coins growing
        coins.forEach((coinObj, index) => {
            if (frameCount > coinObj.delay) {
                const currentScale = coinObj.mesh.scale.x;
                if (currentScale < coinObj.targetScale) {
                    const newScale = Math.min(currentScale + coinObj.speed * delta, coinObj.targetScale);
                    coinObj.mesh.scale.set(newScale, newScale, newScale);
                }
            }
        });
        
        // Rotate piggy bank gently
        piggyBankGroup.rotation.y += 0.005;
        
        // Move coins toward piggy bank occasionally
        if (frameCount % 200 === 0) {
            coins.forEach((coinObj, index) => {
                // Animate a few coins moving toward the piggy bank
                if (index > coins.length - 4 && index < coins.length - 1) {
                    coinObj.mesh.position.x += (piggyBankGroup.position.x - coinObj.mesh.position.x) * 0.01;
                    coinObj.mesh.position.z += (piggyBankGroup.position.z - coinObj.mesh.position.z) * 0.01;
                }
            });
        }
        
        renderer.render(scene, camera);
    }
    
    // Start animation
    animate();
    
    // Clean up on page unload
    window.addEventListener('beforeunload', () => {
        window.removeEventListener('resize', onWindowResize);
    });
}

// Initialize Three.js animation when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the savings animation
    initSavingsAnimation();
});

// Function to simulate playing a savings video
function playSavingsVideo() {
    // In a real implementation, this would play an actual video
    // For now, we'll show an alert explaining the concept
    
    // Create a modal-like overlay
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    overlay.style.display = 'flex';
    overlay.style.alignItems = 'center';
    overlay.style.justifyContent = 'center';
    overlay.style.zIndex = '10000';
    
    const content = document.createElement('div');
    content.style.backgroundColor = 'white';
    content.style.padding = '30px';
    content.style.borderRadius = '10px';
    content.style.maxWidth = '500px';
    content.style.textAlign = 'center';
    content.innerHTML = `
        <h3><i class="fas fa-piggy-bank me-2"></i>Smart Savings with SaveTogether</h3>
        <p class="mt-3">In this video, you would learn:</p>
        <ul class="text-start">
            <li>How group savings multiply your motivation</li>
            <li>Ways to track progress with friends and family</li>
            <li>Tips for reaching financial goals faster</li>
            <li>How SaveTogether makes saving effortless</li>
        </ul>
        <p><strong>Imagine achieving your dreams together!</strong></p>
        <button class="btn btn-primary mt-3" onclick="closeVideoOverlay()">Close</button>
    `;
    
    overlay.appendChild(content);
    document.body.appendChild(overlay);
    
    // Add close function to window object so it can be called from the button
    window.closeVideoOverlay = function() {
        document.body.removeChild(overlay);
        delete window.closeVideoOverlay;
    };
    
    // Close if clicked outside
    overlay.addEventListener('click', function(e) {
        if (e.target === overlay) {
            closeVideoOverlay();
        }
    });
}

// Function to show information about the savings video
function showSavingsVideoInfo() {
    // Create a modal-like overlay with savings video information
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.9)';
    overlay.style.display = 'flex';
    overlay.style.alignItems = 'center';
    overlay.style.justifyContent = 'center';
    overlay.style.zIndex = '10000';
    overlay.style.backdropFilter = 'blur(5px)';
    
    const content = document.createElement('div');
    content.style.backgroundColor = '#fff';
    content.style.padding = '40px';
    content.style.borderRadius = '20px';
    content.style.maxWidth = '600px';
    content.style.width = '90%';
    content.style.textAlign = 'center';
    content.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.3)';
    content.style.position = 'relative';
    
    content.innerHTML = `
        <button class="btn-close position-absolute" style="top: 15px; right: 15px;" onclick="closeSavingsVideoInfo()"></button>
        <div class="mb-4">
            <i class="fas fa-piggy-bank fa-3x text-primary mb-3"></i>
            <h3 class="mb-3">L'Importance de l'Épargne</h3>
        </div>
        <div class="text-start">
            <p>Dans cette vidéo, vous découvrirez :</p>
            <ul class="list-group list-group-flush">
                <li class="list-group-item border-0 py-2">
                    <i class="fas fa-check-circle text-success me-2"></i>
                    <strong>Pourquoi épargner est essentiel</strong> - La sécurité financière et les opportunités futures
                </li>
                <li class="list-group-item border-0 py-2">
                    <i class="fas fa-check-circle text-success me-2"></i>
                    <strong>Les bienfaits de l'épargne collective</strong> - Multiplier la motivation avec vos proches
                </li>
                <li class="list-group-item border-0 py-2">
                    <i class="fas fa-check-circle text-success me-2"></i>
                    <strong>Comment atteindre vos objectifs plus rapidement</strong> - Les stratégies éprouvées
                </li>
                <li class="list-group-item border-0 py-2">
                    <i class="fas fa-check-circle text-success me-2"></i>
                    <strong>Les erreurs à éviter</strong> - Pièges courants dans la gestion financière
                </li>
            </ul>
        </div>
        <div class="mt-4">
            <p class="lead"><i class="fas fa-lightbulb text-warning me-2"></i><strong>Imaginez</strong> atteindre vos rêves ensemble !</p>
            <div class="d-grid gap-2 d-md-flex justify-content-md-center mt-4">
                <a href="/register" class="btn btn-primary btn-lg px-4">
                    <i class="fas fa-rocket me-2"></i>Commencer à Épargner
                </a>
                <button class="btn btn-outline-secondary btn-lg px-4" onclick="closeSavingsVideoInfo()">
                    <i class="fas fa-times me-2"></i>Fermer
                </button>
            </div>
        </div>
    `;
    
    overlay.appendChild(content);
    document.body.appendChild(overlay);
    
    // Add close function to window object so it can be called from the button
    window.closeSavingsVideoInfo = function() {
        document.body.removeChild(overlay);
        delete window.closeSavingsVideoInfo;
    };
    
    // Close if clicked outside
    overlay.addEventListener('click', function(e) {
        if (e.target === overlay) {
            closeSavingsVideoInfo();
        }
    });
    
    // Prevent body scroll when modal is open
    document.body.style.overflow = 'hidden';
}

// Function to show application walkthrough information
function showAppWalkthrough() {
    // Create a modal with app walkthrough details
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.9)';
    overlay.style.display = 'flex';
    overlay.style.alignItems = 'center';
    overlay.style.justifyContent = 'center';
    overlay.style.zIndex = '10000';
    overlay.style.backdropFilter = 'blur(5px)';
    
    const content = document.createElement('div');
    content.style.backgroundColor = '#fff';
    content.style.padding = '30px';
    content.style.borderRadius = '15px';
    content.style.maxWidth = '700px';
    content.style.width = '90%';
    content.style.maxHeight = '90vh';
    content.style.overflowY = 'auto';
    content.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.3)';
    content.style.position = 'relative';
    
    content.innerHTML = `
        <button class="btn-close position-absolute" style="top: 15px; right: 15px;" onclick="closeAppWalkthrough()"></button>
        <div class="text-center mb-4">
            <i class="fas fa-route fa-3x text-primary mb-3"></i>
            <h3 class="mb-3">Navigation dans l'Application SaveTogether</h3>
            <p class="lead">Découvrez toutes les fonctionnalités étape par étape</p>
        </div>
        
        <div class="walkthrough-steps">
            <div class="step-card border rounded-3 p-3 mb-3">
                <div class="d-flex">
                    <div class="step-number bg-primary text-white rounded-circle d-flex align-items-center justify-content-center me-3" style="min-width: 36px; height: 36px;">1</div>
                    <div>
                        <h5 class="mb-1">Inscription & Connexion</h5>
                        <p class="mb-0 text-muted">Créez votre compte ou connectez-vous pour accéder à votre tableau de bord.</p>
                    </div>
                </div>
            </div>
            
            <div class="step-card border rounded-3 p-3 mb-3">
                <div class="d-flex">
                    <div class="step-number bg-primary text-white rounded-circle d-flex align-items-center justify-content-center me-3" style="min-width: 36px; height: 36px;">2</div>
                    <div>
                        <h5 class="mb-1">Tableau de Bord</h5>
                        <p class="mb-0 text-muted">Visualisez vos groupes d'épargne, contributions récentes et notifications.</p>
                    </div>
                </div>
            </div>
            
            <div class="step-card border rounded-3 p-3 mb-3">
                <div class="d-flex">
                    <div class="step-number bg-primary text-white rounded-circle d-flex align-items-center justify-content-center me-3" style="min-width: 36px; height: 36px;">3</div>
                    <div>
                        <h5 class="mb-1">Création de Groupe</h5>
                        <p class="mb-0 text-muted">Créez un nouveau groupe d'épargne avec un objectif, une cible et une date limite.</p>
                    </div>
                </div>
            </div>
            
            <div class="step-card border rounded-3 p-3 mb-3">
                <div class="d-flex">
                    <div class="step-number bg-primary text-white rounded-circle d-flex align-items-center justify-content-center me-3" style="min-width: 36px; height: 36px;">4</div>
                    <div>
                        <h5 class="mb-1">Invitation des Membres</h5>
                        <p class="mb-0 text-muted">Partagez le code d'invitation avec vos amis et votre famille pour les rejoindre.</p>
                    </div>
                </div>
            </div>
            
            <div class="step-card border rounded-3 p-3 mb-3">
                <div class="d-flex">
                    <div class="step-number bg-primary text-white rounded-circle d-flex align-items-center justify-content-center me-3" style="min-width: 36px; height: 36px;">5</div>
                    <div>
                        <h5 class="mb-1">Ajout de Contributions</h5>
                        <p class="mb-0 text-muted">Ajoutez vos contributions avec des descriptions et des preuves optionnelles.</p>
                    </div>
                </div>
            </div>
            
            <div class="step-card border rounded-3 p-3 mb-3">
                <div class="d-flex">
                    <div class="step-number bg-primary text-white rounded-circle d-flex align-items-center justify-content-center me-3" style="min-width: 36px; height: 36px;">6</div>
                    <div>
                        <h5 class="mb-1">Suivi des Progrès</h5>
                        <p class="mb-0 text-muted">Visualisez les graphiques et statistiques pour suivre vos progrès d'épargne.</p>
                    </div>
                </div>
            </div>
            
            <div class="step-card border rounded-3 p-3 mb-3">
                <div class="d-flex">
                    <div class="step-number bg-primary text-white rounded-circle d-flex align-items-center justify-content-center me-3" style="min-width: 36px; height: 36px;">7</div>
                    <div>
                        <h5 class="mb-1">Analyses Avancées</h5>
                        <p class="mb-0 text-muted">Accédez aux analyses détaillées et prédictionnelles (fonctionnalité Premium).</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="mt-4 text-center">
            <div class="alert alert-info">
                <i class="fas fa-video me-2"></i>
                <strong>Une vidéo complète de démonstration sera bientôt disponible !</strong>
            </div>
            <div class="d-grid gap-2 d-md-flex justify-content-md-center mt-3">
                <a href="/register" class="btn btn-primary btn-lg px-4">
                    <i class="fas fa-rocket me-2"></i>Commencer Maintenant
                </a>
                <button class="btn btn-outline-secondary btn-lg px-4" onclick="closeAppWalkthrough()">
                    <i class="fas fa-times me-2"></i>Fermer
                </button>
            </div>
        </div>
    `;
    
    overlay.appendChild(content);
    document.body.appendChild(overlay);
    
    // Add close function to window object so it can be called from the button
    window.closeAppWalkthrough = function() {
        document.body.removeChild(overlay);
        delete window.closeAppWalkthrough;
        // Restore body scroll
        document.body.style.overflow = '';
    };
    
    // Close if clicked outside
    overlay.addEventListener('click', function(e) {
        if (e.target === overlay) {
            closeAppWalkthrough();
        }
    });
    
    // Prevent body scroll when modal is open
    document.body.style.overflow = 'hidden';
}

// Initialize Three.js scene for hero section
function initHeroThreeJs() {
    const container = document.getElementById('hero-threejs-container');
    if (!container) return;

    // Set up scene
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setClearColor(0x0a192f, 0);
    container.appendChild(renderer.domElement);

    // Add lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(1, 1, 1);
    scene.add(directionalLight);

    // Create floating coins
    const coins = [];
    const coinGeometry = new THREE.CylinderGeometry(0.5, 0.5, 0.1, 32);
    const coinMaterial = new THREE.MeshPhongMaterial({ 
        color: 0xf1c40f,
        shininess: 100,
        emissive: 0xd35400,
        emissiveIntensity: 0.2
    });

    // Create a stack of coins that grows over time
    for (let i = 0; i < 8; i++) {
        const coin = new THREE.Mesh(coinGeometry, coinMaterial);
        coin.rotation.x = Math.PI / 2;
        coin.position.y = i * 0.2;
        coin.position.x = Math.sin(i * 0.5) * 0.5;
        coin.position.z = Math.cos(i * 0.5) * 0.5;
        scene.add(coin);
        coins.push({
            mesh: coin,
            speed: 0.01 + Math.random() * 0.02,
            amplitude: 0.1 + Math.random() * 0.2,
            frequency: 0.5 + Math.random() * 1.0,
            phase: Math.random() * Math.PI * 2
        });
    }

    // Create piggy bank
    const piggyBankGroup = new THREE.Group();
    
    // Body
    const bodyGeometry = new THREE.SphereGeometry(1, 32, 32);
    const bodyMaterial = new THREE.MeshPhongMaterial({ color: 0xff9ff3 });
    const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
    piggyBankGroup.add(body);
    
    // Head
    const headGeometry = new THREE.SphereGeometry(0.7, 32, 32);
    const headMaterial = new THREE.MeshPhongMaterial({ color: 0xff9ff3 });
    const head = new THREE.Mesh(headGeometry, headMaterial);
    head.position.set(0, 0, 1);
    piggyBankGroup.add(head);
    
    // Legs
    const legGeometry = new THREE.CylinderGeometry(0.15, 0.15, 0.5, 16);
    const legMaterial = new THREE.MeshPhongMaterial({ color: 0xff9ff3 });
    
    for (let i = 0; i < 4; i++) {
        const leg = new THREE.Mesh(legGeometry, legMaterial);
        const x = i % 2 === 0 ? -0.4 : 0.4;
        const z = i < 2 ? -0.4 : 0.4;
        leg.position.set(x, -0.7, z);
        leg.rotation.x = Math.PI / 2;
        piggyBankGroup.add(leg);
    }
    
    // Slot
    const slotGeometry = new THREE.BoxGeometry(0.4, 0.05, 0.05);
    const slotMaterial = new THREE.MeshPhongMaterial({ color: 0x000000 });
    const slot = new THREE.Mesh(slotGeometry, slotMaterial);
    slot.position.set(0, 0.2, 0.9);
    piggyBankGroup.add(slot);
    
    piggyBankGroup.position.set(2, -1, 0);
    piggyBankGroup.scale.set(0.7, 0.7, 0.7);
    scene.add(piggyBankGroup);

    // Position camera
    camera.position.z = 5;
    camera.position.y = 0;

    // Handle window resize
    function onWindowResize() {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    }
    window.addEventListener('resize', onWindowResize);

    // Animation loop
    let time = 0;
    function animate() {
        requestAnimationFrame(animate);
        time += 0.01;
        
        // Animate coins
        coins.forEach((coinObj, index) => {
            coinObj.mesh.position.y = index * 0.2 + Math.sin(time * coinObj.frequency + coinObj.phase) * coinObj.amplitude;
            coinObj.mesh.rotation.z += coinObj.speed;
        });
        
        // Rotate piggy bank gently
        piggyBankGroup.rotation.y = Math.sin(time * 0.5) * 0.2;
        
        renderer.render(scene, camera);
    }
    
    // Start animation
    animate();
}

// Function to show video information modal
function showVideoModal() {
    const modal = document.createElement('div');
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100%';
    modal.style.height = '100%';
    modal.style.backgroundColor = 'rgba(0, 0, 0, 0.85)';
    modal.style.display = 'flex';
    modal.style.alignItems = 'center';
    modal.style.justifyContent = 'center';
    modal.style.zIndex = '10000';
    modal.style.backdropFilter = 'blur(5px)';
    
    const content = document.createElement('div');
    content.style.backgroundColor = '#fff';
    content.style.padding = '30px';
    content.style.borderRadius = '15px';
    content.style.maxWidth = '600px';
    content.style.width = '90%';
    content.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.3)';
    content.style.position = 'relative';
    
    content.innerHTML = `
        <button class="btn-close position-absolute" style="top: 15px; right: 15px;" onclick="closeVideoModal()"></button>
        <div class="text-center mb-4">
            <i class="fas fa-film fa-3x text-primary mb-3"></i>
            <h3 class="mb-3">Découvrez SaveTogether</h3>
            <p class="lead">Une plateforme innovante pour épargner collectivement</p>
        </div>
        
        <div class="video-info">
            <h5 class="mb-3"><i class="fas fa-info-circle me-2 text-primary"></i>À propos de cette vidéo</h5>
            <ul class="list-group list-group-flush mb-4">
                <li class="list-group-item border-0 py-2">
                    <i class="fas fa-check-circle text-success me-2"></i>
                    Découvrez comment créer et rejoindre des groupes d'épargne
                </li>
                <li class="list-group-item border-0 py-2">
                    <i class="fas fa-check-circle text-success me-2"></i>
                    Apprenez à ajouter des contributions et suivre les progrès
                </li>
                <li class="list-group-item border-0 py-2">
                    <i class="fas fa-check-circle text-success me-2"></i>
                    Comprenez les fonctionnalités de suivi et d'analyse
                </li>
                <li class="list-group-item border-0 py-2">
                    <i class="fas fa-check-circle text-success me-2"></i>
                    Découvrez les avantages de l'épargne collective
                </li>
            </ul>
            
            <div class="alert alert-info">
                <i class="fas fa-video me-2"></i>
                <strong>Prochainement :</strong> Une vidéo détaillée expliquant toutes les fonctionnalités de SaveTogether sera bientôt disponible !
            </div>
        </div>
        
        <div class="text-center mt-4">
            <a href="/register" class="btn btn-primary btn-lg px-4 me-2">
                <i class="fas fa-rocket me-2"></i>Commencer maintenant
            </a>
            <button class="btn btn-outline-secondary btn-lg px-4" onclick="closeVideoModal()">
                <i class="fas fa-times me-2"></i>Fermer
            </button>
        </div>
    `;
    
    modal.appendChild(content);
    document.body.appendChild(modal);
    
    window.closeVideoModal = function() {
        document.body.removeChild(modal);
        delete window.closeVideoModal;
    };
    
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeVideoModal();
        }
    });
}

// Function to show more information modal
function showMoreInfo() {
    const modal = document.createElement('div');
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100%';
    modal.style.height = '100%';
    modal.style.backgroundColor = 'rgba(0, 0, 0, 0.85)';
    modal.style.display = 'flex';
    modal.style.alignItems = 'center';
    modal.style.justifyContent = 'center';
    modal.style.zIndex = '10000';
    modal.style.backdropFilter = 'blur(5px)';
    
    const content = document.createElement('div');
    content.style.backgroundColor = '#fff';
    content.style.padding = '30px';
    content.style.borderRadius = '15px';
    content.style.maxWidth = '600px';
    content.style.width = '90%';
    content.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.3)';
    content.style.position = 'relative';
    
    content.innerHTML = `
        <button class="btn-close position-absolute" style="top: 15px; right: 15px;" onclick="closeInfoModal()"></button>
        <div class="text-center mb-4">
            <i class="fas fa-film fa-3x text-primary mb-3"></i>
            <h3 class="mb-3">Découvrez SaveTogether</h3>
            <p class="lead">Une plateforme innovante pour épargner collectivement</p>
        </div>
        
        <div class="video-info">
            <h5 class="mb-3"><i class="fas fa-info-circle me-2 text-primary"></i>À propos de cette démonstration</h5>
            <ul class="list-group list-group-flush mb-4">
                <li class="list-group-item border-0 py-2">
                    <i class="fas fa-check-circle text-success me-2"></i>
                    Découvrez comment créer et rejoindre des groupes d'épargne
                </li>
                <li class="list-group-item border-0 py-2">
                    <i class="fas fa-check-circle text-success me-2"></i>
                    Apprenez à ajouter des contributions et suivre les progrès
                </li>
                <li class="list-group-item border-0 py-2">
                    <i class="fas fa-check-circle text-success me-2"></i>
                    Comprenez les fonctionnalités de suivi et d'analyse
                </li>
                <li class="list-group-item border-0 py-2">
                    <i class="fas fa-check-circle text-success me-2"></i>
                    Découvrez les avantages de l'épargne collective
                </li>
            </ul>
            
            <div class="alert alert-info">
                <i class="fas fa-video me-2"></i>
                <strong>Prochainement :</strong> Une vidéo détaillée expliquant toutes les fonctionnalités de SaveTogether sera bientôt disponible !
            </div>
        </div>
        
        <div class="text-center mt-4">
            <a href="/register" class="btn btn-primary btn-lg px-4 me-2">
                <i class="fas fa-rocket me-2"></i>Commencer maintenant
            </a>
            <button class="btn btn-outline-secondary btn-lg px-4" onclick="closeInfoModal()">
                <i class="fas fa-times me-2"></i>Fermer
            </button>
        </div>
    `;
    
    modal.appendChild(content);
    document.body.appendChild(modal);
    
    window.closeInfoModal = function() {
        document.body.removeChild(modal);
        delete window.closeInfoModal;
    };
    
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeInfoModal();
        }
    });
}

// Initialize Three.js when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // initHeroThreeJs(); - Removed Three.js initialization
});

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
