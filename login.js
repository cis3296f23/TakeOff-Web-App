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
      if (response.status === 401) {
        throw new Error("Unauthorized");
      } else if (!response.ok) {
        throw new Error("Login failed");
      }
      return response.json();
    })
    //.then(json =>console.log(json))
    .then((data) => {
      // Handle response from the server
      if (data.success) {
        // Redirect to a dashboard or logged-in page
        console.log("Login successful");
        const token = data.token
    if(token){
      console.log('Token Found: ', token);
      localStorage.setItem('authTokenTO', token);
      console.log("from storage");
      console.log(localStorage.getItem('authTokenTO'));

    }
    else
    {
      console.log("Token not found");
    }
        // window.location.href = '/dashboard'; // Redirect to dashboard
      } else {
        // Display error message for failed login
        console.error("Login failed");
        // Show error message to the user
        // const errorMessage = document.getElementById("login-error");
        // errorMessage.textContent = 'Invalid credentials';
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      // Handle other errors, such as network issues
      // Display error message to the user
      // const errorMessage = document.getElementById("login-error");
      // errorMessage.textContent = 'Something went wrong, please try again';
    });

}

document
  .getElementById("loginForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission
    validateLogin();
  });
