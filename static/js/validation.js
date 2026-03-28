document.addEventListener('DOMContentLoaded', function () {
    // Password validation
    const passwordField = document.querySelector('input[name="password"]');

    if (passwordField) {
        passwordField.addEventListener('input', function () {
            const value = this.value;

            const checks = {
                'req-length': value.length >= 8,
                'req-upper': /[A-Z]/.test(value),
                'req-lower': /[a-z]/.test(value),
                'req-digit': /[0-9]/.test(value),
                'req-special': /[!@#$%^&*(),.?":{}|<>]/.test(value),
            };

            for (const [id, passed] of Object.entries(checks)) {
                const el = document.getElementById(id);
                if (el) {
                    el.style.color = passed ? '#4caf50' : '';
                }
            }
        });
    }

    // Username validation
    const usernameField = document.querySelector('input[name="username"]');

    if (usernameField) {
        // Real-time format and length check
        usernameField.addEventListener('input', function () {
            const value = this.value;

            const usernameChecks = {
                'req-username-length': value.length >= 3,
                'req-username-format': /^[A-Za-z0-9_]*$/.test(value),
            };

            for (const [id, passed] of Object.entries(usernameChecks)) {
                const el = document.getElementById(id);
                if (el) {
                    el.style.color = passed ? '#4caf50' : '';
                }
            }
        });

        // Check uniqueness on blur (when user leaves the field)
        usernameField.addEventListener('blur', function () {
            const value = this.value;
            const uniqueElement = document.getElementById('req-username-unique');
            
            if (!value || value.length < 3) {
                uniqueElement.style.color = '';
                return;
            }

            fetch(`/user/check-username/?username=${encodeURIComponent(value)}`)
                .then(res => res.json())
                .then(data => {
                    if (data.taken) {
                        uniqueElement.style.color = '#ff6b6b';
                    } else {
                        uniqueElement.style.color = '#4caf50';
                    }
                })
                .catch(err => {
                    console.error('Error checking username:', err);
                    uniqueElement.style.color = '';
                });
        });
    }
});