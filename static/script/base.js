const signBtn = document.getElementById("signBtn");
const signup = document.getElementById("signup");
const signin = document.getElementById("signin");
const signBackground = document.querySelector(".sign-background");
const closeIcons = document.querySelectorAll(".sign img");
const registered = document.querySelector("#registered > p");
const unregistered = document.querySelector("#unregistered > p");
const signupHintContainer = document.getElementById("signupHintContainer");
const signinHintContainer = document.getElementById("signinHintContainer");
const signupHint = document.querySelector("#signupHintContainer > p");
const signinHint = document.querySelector("#signinHintContainer > p");
const bookingBtn = document.getElementById("bookingBtn");
const signupForm = document.getElementById("signupForm");
const signinForm = document.getElementById("signinForm");

fetch("/api/user/auth", {
  method: "GET",
})
  .then((res) => res.json())
  .then((data) => {
    if (data.data) {
      signBtn.textContent = "登出系統";
      signBtn.addEventListener("click", logout);
      bookingBtn.addEventListener("click", redirectBooking);
      if (window.location.pathname === "/booking") {
        const username = document.getElementById("username");
        const name = document.getElementById("name");
        const email = document.getElementById("email");
        username.textContent = data.data.name;
        name.value = data.data.name;
        email.value = data.data.email;
      }
    } else {
      signBtn.addEventListener("click", showSignWindow);
      bookingBtn.addEventListener("click", showSignWindow);
      if (
        window.location.pathname === "/booking" ||
        window.location.pathname === "/thankyou"
      ) {
        window.location.href = "/";
      }
    }
  })
  .catch((err) => {
    console.log(err);
  });

function logout() {
  fetch("/api/user/auth", {
    method: "DELETE",
  })
    .then((res) => res.json())
    .then(() => {
      window.location.reload();
    })
    .catch((err) => console.log(err));
}

export function redirectBooking() {
  window.location.href = "/booking";
}

export function showSignWindow() {
  signin.className += " sign-container__active";
  signBackground.className += " sign-background__active";
}

registered.addEventListener("click", showSigninWindow);
unregistered.addEventListener("click", showSignupWindow);
closeIcons.forEach((closeIcon) => {
  closeIcon.addEventListener("click", closeSignWindow);
});

function showSigninWindow() {
  signup.className = signup.className.replace(" sign-container__active", "");
  signin.className += " sign-container__active";
  clearHint();
  document.getElementById("signupForm").reset();
}

function showSignupWindow() {
  signin.className = signin.className.replace(" sign-container__active", "");
  signup.className += " sign-container__active";
  clearHint();
  document.getElementById("signinForm").reset();
}

function closeSignWindow() {
  signBackground.className = signBackground.className.replace(
    " sign-background__active",
    ""
  );
  clearHint();
}

function clearHint() {
  signupHintContainer.style.display = "none";
  signupHint.textContent = "";
  signinHintContainer.style.display = "none";
  signinHint.textContent = "";
}

signupForm.addEventListener("submit", handleSignupSubmit);
signinForm.addEventListener("submit", handleSigninSubmit);

function handleSigninSubmit(e) {
  e.preventDefault();
  const userInfo = new FormData(e.target);
  const infoValue = Object.fromEntries(userInfo.entries());
  fetch("/api/user/auth", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(infoValue),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.ok) {
        signinHintContainer.style.display = "flex";
        signinHint.textContent = "成功登入";
        signinHint.style.color = "green";
        window.location.reload();
      } else {
        signinHintContainer.style.display = "flex";
        signinHint.textContent = "email或密碼錯誤";
        signinHint.style.color = "red";
      }
    })
    .catch((err) => {
      console.log(err);
    });
}

function handleSignupSubmit(e) {
  e.preventDefault();
  const userInfo = new FormData(e.target);
  const infoValue = Object.fromEntries(userInfo.entries());
  fetch("/api/user", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(infoValue),
  })
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      if (data.ok) {
        signupHintContainer.style.display = "flex";
        signupHint.textContent = "成功註冊";
        signupHint.style.color = "green";
      } else {
        signupHintContainer.style.display = "flex";
        signupHint.textContent = "email已被註冊";
        signupHint.style.color = "red";
      }
    })
    .catch((err) => {
      console.log(err);
    });
}
