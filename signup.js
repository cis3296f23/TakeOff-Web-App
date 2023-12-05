function validateSignup() {
    var newUsername = document.getElementById("newUsername").value;
    var newPassword = document.getElementById("newPassword").value;
    const hashedPassword = CryptoJS.SHA256(newPassword).toString(); // Fixed variable name typo (password -> newPassword)
    var signupError = document.getElementById("signup-error");
  
    fetch('http://localhost:5002/signup', {
      method: "POST",
      headers: {
        "Content-Type": "application/json;",
      },
      body: JSON.stringify({ "newUsername": newUsername, "hashedPassword": hashedPassword }),
    })
      .then((response) => {
        console.log(response);
        if (response.status === 401) {
          throw new Error("Unauthorized");
        } else if (!response.ok) {
          throw new Error("Signup failed");
        }
        return response.json();
      })
      .then((data) => {
        // Handle response from the server
        if (data.success) {
          // Signup was successful
          console.log("Account Creation successful");
          closeModal('signupModal'); // Close the signup modal
          signupError.textContent = "Account creation successful";
          signupError.style.color = "green";
        } else {
          // Signup failed
          console.error("Account Creation failed");
          signupError.textContent = "Account creation failed";
          signupError.style.color = "red";
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        // Handle other errors, such as network issues
        signupError.textContent = `Something went wrong, please try again. Reason: ${error.message} : Username Exists`;
        signupError.style.color = "red";
      });
  }
  
  document
    .getElementById("signupForm")
    .addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent the default form submission
      validateSignup();
    });
  