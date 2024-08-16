document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('container');
    const registerBtn = document.getElementById('register');
    const loginBtn = document.getElementById('login');
    const avatarInput = document.getElementById('avatar');

    if (!container) {
        console.error("Container element is not found in the DOM.");
        return;
    }
    if (!registerBtn) {
        console.error("Register button is not found in the DOM.");
        return;
    }
    if (!loginBtn) {
        console.error("Login button is not found in the DOM.");
        return;
    }
    if (!avatarInput) {
        console.error("Avatar input element is not found in the DOM.");
        return;
    }

    // Debounce function to prevent rapid firing of click events
    function debounce(func, wait = 100) {
        let timeout;
        return function(...args) {
            const context = this;
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(context, args), wait);
        };
    }

    try {
        registerBtn.addEventListener('click', debounce(() => {
            container.classList.add("active");
            console.info("Register button clicked, container activated.");
        }));

        loginBtn.addEventListener('click', debounce(() => {
            container.classList.remove("active");
            console.info("Login button clicked, container deactivated.");
        }));

        avatarInput.addEventListener('change', function() {
            var fileName = this.files[0].name;
            var nextSibling = this.nextElementSibling;
            if (nextSibling) {
                nextSibling.innerText = fileName;
            } else {
                console.error("Next sibling element not found.");
            }
        });
    } catch (error) {
        console.error("Error attaching event listeners:", error);
    }
});

function validateSignUpForm() {
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();

    if (!username) {
        alert('Username is required.');
        return false;
    }

    if (!email) {
        alert('Email is required.');
        return false;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        alert('Please enter a valid email address.');
        return false;
    }

    if (!password) {
        alert('Password is required.');
        return false;
    }

    if (password.length < 8) {
        alert('Password must be at least 8 characters long.');
        return false;
    }

    return true;
}

function validateSignInForm() {
    const email = document.getElementById('email-signin').value.trim();
    const password = document.getElementById('password-signin').value.trim();

    if (!email) {
        alert('Email is required.');
        return false;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        alert('Please enter a valid email address.');
        return false;
    }

    if (!password) {
        alert('Password is required.');
        return false;
    }

    return true;
}

function previewImage(event) {
    const reader = new FileReader();
    reader.onload = function() {
        const output = document.getElementById('user-avatar');
        output.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
}

document.addEventListener('DOMContentLoaded', () => {
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
    if ($navbarBurgers.length > 0) {
        $navbarBurgers.forEach(el => {
            el.addEventListener('click', () => {
                const target = el.dataset.target;
                const $target = document.getElementById(target);
                el.classList.toggle('is-active');
                $target.classList.toggle('is-active');
            });
        });
    }
});

function handleError(resource) {
    console.error(`Error loading ${resource}`);
}

document.addEventListener('DOMContentLoaded', () => {
    const signUpForm = document.getElementById('sign-up-form');
    const signInForm = document.getElementById('sign-in-form');
    const toggleSignInLink = document.getElementById('toggle-signin-link');
    const toggleSignUpLink = document.getElementById('toggle-signup-link');

    if (toggleSignInLink) {
        toggleSignInLink.addEventListener('click', (event) => {
            event.preventDefault();
            signUpForm.classList.add('is-hidden');
            signInForm.classList.remove('is-hidden');
        });
    }

    if (toggleSignUpLink) {
        toggleSignUpLink.addEventListener('click', (event) => {
            event.preventDefault();
            signInForm.classList.add('is-hidden');
            signUpForm.classList.remove('is-hidden');
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        new PasswordStrength({
            element: passwordInput
        });
    }
});

document.querySelector('.upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    fetch('/upload_avatar', {
        method: 'POST',
        headers: {
            'X-CSRF-TOKEN': csrfToken
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Profile picture updated successfully');
        } else {
            alert('Error updating profile picture');
        }
    })
    .catch(error => console.error('Error:', error));
});