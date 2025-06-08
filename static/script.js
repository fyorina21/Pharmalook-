
document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("loginForm");
    const forgotPasswordLink = document.querySelector(".forgot-password");
    const backToLoginLink = document.querySelector(".show-login");
    const loginContainer = document.querySelector(".login-container");
    const recoveryForm = document.querySelector(".password-recovery-form");
    const recoveryBtn = document.querySelector(".recovery-btn");
    const loginBtn = document.getElementById("loginBtn");
    const loginError = document.getElementById("login-error");
    // Login functionality
    loginForm.addEventListener("submit", function(e) {
        e.preventDefault(); 

        let email = document.getElementById("email").value.trim();
        let password = document.getElementById("password").value.trim();
        let rememberMe = document.getElementById("remember-me").checked;
        if (!email || !password) {
          loginError.textContent = "Please fill in both filds!"
          loginError.style.display = "block";
          return;
        }
        loginError.style.display = "none";
        
        loginBtn.textContent = "Logging in...";
        loginBtn.disabled = true;

        fetch("http://localhost:5000/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password, rememberMe })
        })
        .then(response => {
          if (!response.ok){
            return response.json().then(err => {throw err;});
          }
          return response.json();
        })
        .then(data => {
            loginBtn.textContent = "Login";
            loginBtn.disabled = false;
             if (data.error) {
                loginError.textContent = data.error;
                loginError.style.display = "block";
            } else if (data.success) {
                if (rememberMe) {
                    localStorage.setItem("token", data.token); 
                    sessionStorage.setItem("token", data.token); 
                }
                if (data.role === "admin"){
                    window.location.href = "admin-dashboard.html"; 
            } else {
               window.location.href = "pharmacist-dashboard.html";
            }
          }
        })
        .catch(error => {
            loginBtn.textContent = "Login";
            loginBtn.disabled = false;
            loginError.textContent = error.error || "Login failed.Please try again"
            loginError.style.display = "block";
            console
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
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to send reset link");
            }
            return response.json();
        })
        .then(data => {
            recoveryBtn.textContent = "Send Reset Link";
            recoveryBtn.disabled = false;
            alert("If an account exists with this email, a reset link has been sent");
            recoveryForm.style.display = "none";
            loginContainer.style.display = "block";
        })
        .catch(error => {
            recoveryBtn.textContent = "Send Reset Link";
            recoveryBtn.disabled = false;
            alert("Could not send reset link. Please try again.");
            console.error("Error:", error);
        });
      });
    });

