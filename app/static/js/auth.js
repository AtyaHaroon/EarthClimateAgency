// Authentication form handling
document.addEventListener("DOMContentLoaded", function () {
  const signinForm = document.getElementById("signin-form");
  const signupForm = document.getElementById("signup-form");

  if (signinForm) {
    signinForm.addEventListener("submit", function (e) {
      e.preventDefault();
      // Here you would normally handle the sign in logic
      console.log("Sign In submitted");
      // For demo purposes, just show an alert
      alert("Sign In functionality would be implemented here");
    });
  }

  if (signupForm) {
    signupForm.addEventListener("submit", function (e) {
      e.preventDefault();
      // Here you would normally handle the sign up logic
      console.log("Sign Up submitted");

      // Simple validation
      const password = document.getElementById("password").value;
      const confirmPassword = document.getElementById("confirm-password").value;

      if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
      }

      // For demo purposes, just show an alert
      alert("Account created successfully! (This is a demo)");
    });
  }

  // Social auth buttons
  document.querySelectorAll(".social-button").forEach((button) => {
    button.addEventListener("click", function () {
      const provider = this.classList.contains("google")
        ? "Google"
        : "Microsoft";
      alert(`Would normally authenticate with ${provider} (This is a demo)`);
    });
  });
});
