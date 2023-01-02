import { checkName, checkEmail, checkPhone } from "./validate.js";
import { APP_ID, APP_KEY } from "./setting.js";
const attractionName = document.getElementById("attractionName");
const date = document.getElementById("date");
const time = document.getElementById("time");
const price = document.getElementById("price");
const totalPrice = document.getElementById("totalPrice");
const address = document.getElementById("address");
const deleteBtn = document.getElementById("delete");
const attractionImg = document.getElementById("attractionImg");
const bookingContexts = document.querySelectorAll(".booking_context");
const noBookingContext = document.querySelector(".noBooking_context");
const body = document.querySelector("body");
const main = document.querySelector("main");
const orderBtn = document.querySelector(".orderBtn");
let orderData = {};

booking_init();
async function booking_init() {
  try {
    const res = await fetch("/api/booking", { method: "get" });
    const data = await res.json();
    if (data.data) {
      showBookingContent(data);
      getOrderData(data);
    } else {
      showNoBookingContent();
    }
  } catch (err) {
    console.log(err);
  }
}

function getOrderData(data) {
  orderData.trip = data.data;
  orderData.price = orderData.trip.price;
  delete orderData.trip.price;
}

function showBookingContent(data) {
  attractionName.textContent = data.data.attraction.name;
  address.textContent = data.data.attraction.address;
  attractionImg.src = data.data.attraction.image;
  date.textContent = data.data.date;
  time.textContent = translateTime(data.data.time);
  price.textContent = `新台幣 ${data.data.price.toString()}元`;
  totalPrice.textContent = `新台幣 ${data.data.price.toString()}元`;
  bookingContexts.forEach((context) => {
    context.style.display = "block";
  });
}

function showNoBookingContent() {
  noBookingContext.style.display = "block";
  body.style.backgroundColor = "var(--secondary-color-gray-50)";
  main.style.backgroundColor = "var(--additional-color-white)";
}

let fields = {
  number: {
    element: "#card-number",
    placeholder: "**** **** **** ****",
  },
  expirationDate: {
    element: document.getElementById("card-expiration-date"),
    placeholder: "MM / YY",
  },
  ccv: {
    element: "#card-ccv",
    placeholder: "ccv",
  },
};

TPDirect.setupSDK(APP_ID, APP_KEY, "sandbox");

TPDirect.card.setup({
  fields: fields,
  styles: {
    input: {
      color: "var(--additional-color-black)",
      "font-family": '"Noto Sans TC", sans-serif',
    },
    "input.ccv": {
      "font-size": "16px",
    },
    "input.expiration-date": {
      "font-size": "16px",
    },
    "input.card-number": {
      "font-size": "16px",
    },
    ":focus": {
      color: "black",
    },
    ".valid": {
      color: "green",
    },
    ".invalid": {
      color: "red",
    },
    "@media screen and (max-width: 400px)": {
      input: {
        color: "orange",
      },
    },
  },
  // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
  isMaskCreditCardNumber: true,
  maskCreditCardNumberRange: {
    beginIndex: 6,
    endIndex: 11,
  },
});

function postOrder() {
  const tappayStatus = TPDirect.card.getTappayFieldsStatus();
  if (tappayStatus.canGetPrime === false) {
    alert("付款資訊輸入不正確");
    return;
  }
  if (checkOrderInfo() === false) {
    return;
  } else {
    orderData.contact = generateContactInfo();
  }
  TPDirect.card.getPrime((result) => {
    if (result.status !== 0) {
      alert("get prime error " + result.msg);
      return;
    }
    let orderRequest = {
      prime: result.card.prime,
      order: orderData,
    };
    (async () => {
      try {
        const res = await fetch("/api/orders", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(orderRequest),
        });
        const data = await res.json();
        if (data.error) {
          alert(data.message);
        }
        window.location.href = `/thankyou?number=${data.data.number}`;
      } catch (err) {
        console.log(err);
      }
    })();
  });
}

function checkOrderInfo() {
  let name = document.getElementById("name").value;
  let email = document.getElementById("email").value;
  let phone = document.getElementById("phone").value;
  if (!checkName(name)) {
    alert("姓名格式錯誤，請輸入至多10位中英文字母不含空格");
    return false;
  }
  if (!checkEmail(email)) {
    alert("信箱格式錯誤，請填入正確的信箱格式");
    return false;
  }
  if (!checkPhone(phone)) {
    alert("手機格式錯誤，請輸入09xxxxxxxx");
    return false;
  }
  return true;
}

function generateContactInfo() {
  let contact = {};
  contact.name = document.getElementById("name").value;
  contact.email = document.getElementById("email").value;
  contact.phone = document.getElementById("phone").value;
  return contact;
}

orderBtn.addEventListener("click", postOrder);

function translateTime(time) {
  if (time === "morning") {
    return "早上9點到下午4點";
  } else {
    return "下午2點到下午9點";
  }
}

deleteBtn.addEventListener("click", deleteBooking);

async function deleteBooking() {
  try {
    const res = await fetch("/api/booking", { method: "DELETE" });
    const data = await res.json();
    if (data.ok) {
      window.location.reload();
    } else {
      alert(`${data.message}`);
    }
  } catch (err) {
    console.log(err);
  }
}
