import { checkName, checkEmail, checkPassword } from "./validate.js";
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

base_init();

async function base_init() {
  try {
    const res = await fetch("/api/user/auth", {
      method: "GET",
    });
    const data = await res.json();
    if (data.data !== null) {
      signBtn.textContent = "登出系統";
      signBtn.addEventListener("click", logout);
      bookingBtn.addEventListener("click", redirectBooking);
      if (window.location.pathname === "/booking") {
        setBookingInfo(data);
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
  } catch (err) {
    console.log(err);
  }
}

function setBookingInfo(data) {
  const username = document.getElementById("username");
  const name = document.getElementById("name");
  const email = document.getElementById("email");
  username.textContent = data.data.name;
  name.value = data.data.name;
  email.value = data.data.email;
}

async function logout() {
  try {
    await fetch("/api/user/auth", {
      method: "DELETE",
    });
    window.location.reload();
  } catch (err) {
    console.log(err);
  }
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

function showSigninHint(msg, color) {
  signinHintContainer.style.display = "flex";
  signinHint.textContent = msg;
  signinHint.style.color = color;
}
function showSignupHint(msg, color) {
  signupHintContainer.style.display = "flex";
  signupHint.textContent = msg;
  signupHint.style.color = color;
}

function handleSigninSubmit(e) {
  e.preventDefault();
  const signinInput = new FormData(e.target);
  const inputValue = Object.fromEntries(signinInput.entries());
  if (!checkEmail(inputValue.email)) {
    showSigninHint("email格式錯誤", "red");
  }
  if (!checkPassword(inputValue.password)) {
    showSigninHint("密碼格式錯誤，請輸入8位以上字母、數字或符號", "red");
  }
  if (checkEmail(inputValue.email) && checkPassword(inputValue.password)) {
    (async () => {
      try {
        const res = await fetch("/api/user/auth", {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(inputValue),
        });
        const data = await res.json();
        if (data.ok) {
          showSigninHint("成功登入", "green");
          window.location.reload();
        } else {
          showSigninHint("email或密碼錯誤", "red");
        }
      } catch (err) {
        console.log(err);
      }
    })();
  }
}

function handleSignupSubmit(e) {
  e.preventDefault();
  const signupInput = new FormData(e.target);
  const inputValue = Object.fromEntries(signupInput.entries());

  if (!checkName(inputValue.name)) {
    showSignupHint("姓名格式錯誤，請輸入至多10位中英文字母不含空格", "red");
  }
  if (!checkEmail(inputValue.email)) {
    showSignupHint("email格式錯誤", "red");
  }
  if (!checkPassword(inputValue.password)) {
    showSignupHint("密碼格式錯誤，請輸入8位以上字母、數字或符號", "red");
  }
  if (
    checkName(inputValue.name) &&
    checkEmail(inputValue.email) &&
    checkPassword(inputValue.password)
  ) {
    (async () => {
      try {
        const res = await fetch("/api/user", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(inputValue),
        });
        const data = await res.json();
        if (data.ok) {
          showSignupHint("成功註冊", "green");
        } else {
          showSignupHint(data.message, "red");
        }
      } catch (err) {
        console.log(err);
      }
    })();
  }
}
