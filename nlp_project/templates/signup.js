// Function to validate the signup form
function validateSignupForm() {
    var username = document.querySelector('input[type="text"]').value;
    var email = document.querySelector('input[type="email"]').value;
    var password = document.querySelector('input[type="password"]').value;
    var confirmPassword = document.querySelectorAll('input[type="password"]')[1].value;

    // Simple validation for username, email, and password fields
    if (username.trim() === '' || email.trim() === '' || password.trim() === '') {
        alert('Please fill out all fields');
        return false;
    }

    // Check if passwords match
    if (password !== confirmPassword) {
        alert('Passwords do not match');
        return false;
    }

    // All validations passed, form can be submitted
    return true;
}

// Add event listener to the form's submit event
document.querySelector('form').addEventListener('submit', function(event) {
    // Prevent default form submission
    event.preventDefault();

    // Validate the form before submission
    if (validateSignupForm()) {
        // Form is valid, submit it
        this.submit();
    }
});
