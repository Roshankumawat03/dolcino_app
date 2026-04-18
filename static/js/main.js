// Mobile Menu Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger?.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    hamburger.classList.toggle('active');
});

// Close menu on link click
document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    });
});

// Newsletter AJAX
const newsletterForm = document.getElementById('newsletterForm');
newsletterForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const emailInput = document.getElementById('email');
    const button = newsletterForm.querySelector('button');
    
    const email = emailInput.value;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Subscribing...';
    button.disabled = true;
    
    try {
        const response = await fetch('/subscribe', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `email=${encodeURIComponent(email)}`
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert(result.message);
            newsletterForm.reset();
        } else {
            alert('Oops! Something went wrong. Try again.');
        }
    } catch (error) {
        alert('Network error. Please check your connection.');
    } finally {
        button.innerHTML = '<i class="fas fa-paper-plane"></i> Subscribe';
        button.disabled = false;
    }
});

// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(anchor.getAttribute('href'));
        target?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
});

// Header scroll effect
window.addEventListener('scroll', () => {
    const header = document.querySelector('.header');
    if (window.scrollY > 100) {
        header.style.background = 'rgba(255,255,255,0.98)';
    } else {
        header.style.background = 'rgba(255,255,255,0.95)';
    }
});

// Post navigation
function goToPost(slug) {
    window.location.href = `/post/${slug}`;
}

// Intersection Observer for animations
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animationPlayState = 'running';
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.post-card, .section-title').forEach(el => {
    el.style.animationPlayState = 'paused';
    observer.observe(el);
});