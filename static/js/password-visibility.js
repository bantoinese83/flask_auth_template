function togglePasswordVisibility(inputIds) {
    inputIds.forEach(inputId => {
        const input = document.getElementById(inputId);
        const icon = document.getElementById(`${inputId}-icon`);
        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        } else {
            input.type = 'password';
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        }
    });
}