class PasswordStrength {
    constructor(options) {
        this.element = options.element;
        this.strengthLabels = options.strengthLabels || ['Bad', 'Weak', 'Good', 'Strong'];
        this.customReq = options.customReq || null;
        this.strengthLevel = options.strengthLevel || null;
        this.init();
    }

    init() {
        if (this.element) {
            this.element.addEventListener('input', (event) => {
                const value = event.target.value;
                this.updateStrengthMeter(value);
                this.checkRequirements(value);
            });
        }
    }

    updateStrengthMeter(value) {
        const result = zxcvbn(value);
        const meterFill = document.querySelector('.password-strength__meter--fill');
        const strengthValue = document.querySelector('.password-strength__value');
        meterFill.style.width = `${(result.score + 1) * 20}%`;
        meterFill.className = `password-strength__meter--fill password-strength__meter--fill-${result.score + 1}`;
        strengthValue.textContent = this.strengthLabels[result.score];
    }

    checkRequirements(value) {
        const requirements = document.querySelectorAll('.js-password-strength__req');
        requirements.forEach(req => {
            const reqType = req.getAttribute('data-password-req');
            let isValid = false;
            switch (reqType) {
                case 'number':
                    isValid = /\d/.test(value);
                    break;
                case 'letter':
                    isValid = /[a-zA-Z]/.test(value);
                    break;
                case 'special':
                    isValid = /[!@#$%^&*(),.?":{}|<>]/.test(value);
                    break;
                case 'uppercase':
                    isValid = /[A-Z]/.test(value);
                    break;
                case 'length:6':
                    isValid = value.length >= 6;
                    break;
                default:
                    if (this.customReq) {
                        isValid = this.customReq(value);
                    }
                    break;
            }
            req.classList.toggle('is-valid', isValid);
        });
    }
}