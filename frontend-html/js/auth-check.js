// auth.js
document.addEventListener('DOMContentLoaded', function() {
    const authForm = document.getElementById('auth-form');
    authForm.addEventListener('submit', async function(e)  {
        e.preventDefault(); // Prevent the default form submission

        const authCode = document.getElementById('auth-code').value;
        const errorElement = document.getElementById('auth-error');
        try{
            const authButton = authForm.querySelector('button[type="submit"]');
            // Simulate an API call to verify the authentication code
            await verifyAuthCode(authCode);
            window.location.href = 'dashboard.html';
        }
        catch (error) {
            console.error('Auth error:', error);
            errorElement.textContent = 'Authentication failed. Please try again.';
        }
    });
});