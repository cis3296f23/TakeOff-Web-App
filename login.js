/**
 * Function to validate login by getting the username & password, based on response display any errors/messages front end
 */

function validateLogin() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const hashedPassword = CryptoJS.SHA256(password).toString();

  fetch('http://localhost:5000/login', {
    method: "POST",
    headers: {
      "Content-Type": "application/json;",
    },
    body: JSON.stringify({ "username": username, "hashedPassword": hashedPassword }),
  })
    .then((response) => {
      if (!response.ok) {
        if (response.status === 401) {
          throw new Error("Unauthorized");
        } else {
          throw new Error("Login failed");
        }
      }
      return response.json();
    })
    .then((data) => {
      if (data.success) {
        console.log("Login successful");
        const signUpSuccess = document.getElementById("login-error");
        signUpSuccess.textContent = 'Login Successful';
        signUpSuccess.style.color = "green";

        // Redirect to a dashboard or logged-in page
        // window.location.href = '/dashboard'; // Redirect to dashboard
      } else {
        console.error("Login failed");
        const signupError = document.getElementById("login-error");
        signupError.textContent = "Invalid credentials";
        signupError.style.color = "red";
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      const signupError = document.getElementById("login-error");
      signupError.textContent = `Something went wrong, please try again. Reason: ${error.message} `;
      signupError.style.color = "red";
    });
}

document
  .getElementById("loginForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission
    validateLogin();
  });