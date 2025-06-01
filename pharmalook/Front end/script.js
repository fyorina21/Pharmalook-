document.addEventListener("DOMContentLoaded", function() {
    const loginBtn = document.querySelector(".login-btn");
    const forgotPasswordLink = document.querySelector(".forgot-password");
    const backToLoginLink = document.querySelector(".show-login");
    const loginContainer = document.querySelector(".login-container");
    const recoveryForm = document.querySelector(".password-recovery-form");
    const recoveryBtn = document.querySelector(".recovery-btn");

    // Login functionality
    loginBtn.addEventListener("click", function() {
        let email = document.getElementById("email").value.trim();
        let password = document.getElementById("password").value.trim();
        let rememberMe = document.getElementById("remember-me").checked;
        if (!email || !password) {
            alert("Please fill in both fields!");
            return;
        }

        // Send login request to backend
        loginBtn.textContent = "Logging in...";
        loginBtn.disabled = true;

        fetch("http://localhost:5000/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password, rememberMe })
        })
        .then(response => response.json())
        .then(data => {
            loginBtn.textContent = "Login";
            loginBtn.disabled = false;
             if (data.redirect) {
                window.location.href = data.redirect; // Redirect to signup if user not found
            } else if (data.success) {
                if (rememberMe) {
                    localStorage.setItem("token", data.token); // Persist token
                } else {
                    sessionStorage.setItem("token", data.token); // Session-only token
                }
                window.location.href = "dashboard.html"; // Redirect on success
            } else {
                alert(data.error);
            }
        })
        .catch(error => {
            loginBtn.textContent = "Login";
            loginBtn.disabled = false;
            console.error("Error:", error);
            alert("Something went wrong. Please try again.");
        });
    });

    // Forgot password toggle
    forgotPasswordLink.addEventListener("click", function(e) {
        e.preventDefault();
        loginContainer.style.display = "none";
        recoveryForm.style.display = "block";
    });

    backToLoginLink.addEventListener("click", function(e) {
        e.preventDefault();
        recoveryForm.style.display = "none";
        loginContainer.style.display = "block";
    });

    // Password recovery functionality
    recoveryBtn.addEventListener("click", function() {
        let recoveryEmail = document.getElementById("recovery-email").value.trim();

        if (!recoveryEmail) {
            alert("Please enter your email!");
            document.getElementById("recovery-email").focus();
            return;
        }

        recoveryBtn.textContent = "Sending...";
        recoveryBtn.disabled = true;

        fetch("http://localhost:5000/api/password-recovery", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: recoveryEmail })
        })
        .then(response => response.json())
        .then(data => {
            recoveryBtn.textContent = "Send Reset Link";
            recoveryBtn.disabled = false;
            alert(data.message);
        })
        .catch(error => {
            recoveryBtn.textContent = "Send Reset Link";
            recoveryBtn.disabled = false;
            console.error("Error:", error);
            alert("Could not send reset link. Try again.");
        });
    });

