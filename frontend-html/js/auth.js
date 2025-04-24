document.addEventListener('DOMContentLoaded', function() {
    // Check if already authenticated
    if (isAuthenticated()) {
        window.location.href = 'dashboard.html';
        return;
    }
    
    // Initialize tabs
    initTabs();
    
    // Login form submission
    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const errorElement = document.getElementById('login-error');
        
        try {
            errorElement.textContent = '';
            const loginButton = loginForm.querySelector('button[type="submit"]');
            const originalText = loginButton.textContent;
            loginButton.textContent = 'Logging in...';
            loginButton.disabled = true;
            
            await login(username, email);
            window.location.href = 'auth-check.html';//window.location.href = 'dashboard.html';
        } catch (error) {
            console.error('Login error:', error);
            errorElement.textContent = 'Login failed. Please check your credentials.';
        } finally {
            const loginButton = loginForm.querySelector('button[type="submit"]');
            loginButton.textContent = 'Login';
            loginButton.disabled = false;
        }
    });
    
    // Signup form submission
    const signupForm = document.getElementById('signup-form');
    signupForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username-signup').value;
        const email = document.getElementById('email-signup').value;
        const errorElement = document.getElementById('signup-error');
        
        try {
            errorElement.textContent = '';
            const signupButton = signupForm.querySelector('button[type="submit"]');
            const originalText = signupButton.textContent;
            signupButton.textContent = 'Signing up...';
            signupButton.disabled = true;
            
            await signup(username, email);
            window.location.href = 'auth-check.html';//window.location.href = 'dashboard.html';
        } catch (error) {
            console.error('Signup error:', error);
            errorElement.textContent = 'Signup failed. Please try again.';
        } finally {
            const signupButton = signupForm.querySelector('button[type="submit"]');
            signupButton.textContent = 'Sign Up';
            signupButton.disabled = false;
        }
    });
});