const signBtn = document.getElementById("signBtn");
const signup = document.getElementById("signup");
const signin = document.getElementById("signin");
const signBackground = document.querySelector(".sign-background");
const closeIcons = document.querySelectorAll(".sign img");
const registered = document.querySelector("#registered > p");
const unregistered = document.querySelector("#unregistered > p");
const signupHintContainer = document.getElementById("signinHintContainer");
const signinHintContainer = document.getElementById("signinHintContainer");
const signupHint = document.querySelector("#signupHintContainer > p");
const signinHint = document.querySelector("#signinHintContainer > p");

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

function showSignWindow() {
  signin.className += " sign-container__active";
  signBackground.className += " sign-background__active";
}

fetch("/api/user/auth", {
  method: "GET",
})
  .then((res) => res.json())
  .then((data) => {
    if (data.data != null) {
      signBtn.textContent = "登出系統";
      signBtn.addEventListener("click", logout);
    } else {
      signBtn.addEventListener("click", showSignWindow);
    }
  })
  .catch((err) => {
    console.log(err);
  });

function clearHintMessage() {
  signupHintContainer.style.display = "none";
  signupHint.textContent = "";
  signinHintContainer.style.display = "none";
  signinHint.textContent = "";
}

function showSigninWindow() {
  signup.className = signup.className.replace(" sign-container__active", "");
  signin.className += " sign-container__active";
  clearHintMessage();
  document.getElementById("signupForm").reset();
}

function showSignupWindow() {
  signin.className = signin.className.replace(" sign-container__active", "");
  signup.className += " sign-container__active";
  clearHintMessage();
  document.getElementById("signinForm").reset();
}

function closeSignWindow() {
  signBackground.className = signBackground.className.replace(
    " sign-background__active",
    ""
  );
  clearHintMessage();
}

registered.addEventListener("click", showSigninWindow);
unregistered.addEventListener("click", showSignupWindow);
closeIcons.forEach((closeIcon) => {
  closeIcon.addEventListener("click", closeSignWindow);
});

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
    .then((res) => {
      return res.json();
    })
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

const signupForm = document.getElementById("signupForm");
signupForm.addEventListener("submit", handleSignupSubmit);
const signinForm = document.getElementById("signinForm");
signinForm.addEventListener("submit", handleSigninSubmit);
