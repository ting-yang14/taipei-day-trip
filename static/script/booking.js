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
