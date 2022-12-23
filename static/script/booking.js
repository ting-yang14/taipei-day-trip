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
const footer = document.querySelector("footer");
const body = document.querySelector("body");
const main = document.querySelector("main");
const orderBtn = document.querySelector(".orderBtn");
let order = {};

fetch("/api/booking", { method: "get" })
  .then((res) => res.json())
  .then((data) => {
    if (data.data) {
      attractionName.textContent = data.data.attraction.name;
      address.textContent = data.data.attraction.address;
      attractionImg.src = data.data.attraction.image;
      date.textContent = data.data.date;
      time.textContent = translateTime(data.data.time);
      price.textContent = `新台幣 ${data.data.price.toString()}元`;
      totalPrice.textContent = `新台幣 ${data.data.price.toString()}元`;
      order.trip = data.data;
      order.price = order.trip.price;
      delete order.trip.price;
      bookingContexts.forEach((context) => {
        context.style.display = "block";
      });
    } else {
      noBookingContext.style.display = "block";
      body.style.backgroundColor = "var(--secondary-color-gray-50)";
      main.style.backgroundColor = "var(--additional-color-white)";
    }
  })
  .catch((err) => {
    console.log(err);
  });

TPDirect.setupSDK(
  126906,
  "app_Bd7Dq6UOmo6IE1RjeNrEQJR0Epjx6BPWdXL8WeWvXFfOWuQ9PntrdgFoEvAv",
  "sandbox"
);

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
    order.contact = generateContactInfo();
  }
  TPDirect.card.getPrime((result) => {
    if (result.status !== 0) {
      alert("get prime error " + result.msg);
      return;
    }
    orderRequest = {
      prime: result.card.prime,
      order: order,
    };
    fetch("/api/orders", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(orderRequest),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.data) {
          window.location.href = `/thankyou?number=${data.data.number}`;
        }
      })
      .catch((err) => console.log(err));
  });
}

function checkOrderInfo() {
  let name = document.getElementById("name").value;
  let email = document.getElementById("email").value;
  let phone = document.getElementById("phone").value;
  if (name === "") {
    alert("請填入聯絡姓名");
    return false;
  }
  if (email === "") {
    alert("請填入聯絡信箱");
    return false;
  }
  if (phone === "") {
    alert("請填入手機號碼");
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

function deleteBooking() {
  fetch("/api/booking", { method: "DELETE" })
    .then((res) => res.json())
    .then((data) => {
      if (data.ok) {
        window.location.reload();
      } else {
        alert(`${data.message}`);
      }
    });
}
