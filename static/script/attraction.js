import { showSignWindow, redirectBooking } from "./base.js";

const gallery = document.querySelector(".gallery");
const picCurrent = document.querySelector(".pic-current");
const attractionName = document.getElementById("name");
const category = document.getElementById("category");
const mrt = document.getElementById("mrt");
const price = document.getElementById("price");
const description = document.getElementById("description");
const address = document.getElementById("address");
const transport = document.getElementById("transport");
const next = document.querySelector(".next");
const prev = document.querySelector(".prev");
const startBookingBtn = document.querySelector(".startBookingBtn");
const date = document.getElementById("date");

let imageIndex = 0;
let attractionId = -1;

fetch(`/api${window.location.pathname}`)
  .then((response) => response.json())
  .then((data) => {
    if (data.data) {
      attractionId = data.data.id;
      document.querySelector("title").textContent = data.data.name;
      loadImage(data.data.images);
      createCurrentImageDot(data.data.images);
      attractionName.textContent = data.data.name;
      category.textContent = data.data.category;
      mrt.textContent = data.data.mrt;
      description.textContent = data.data.description;
      address.textContent = data.data.address;
      transport.textContent = data.data.transport;
      showImage(imageIndex);
      next.addEventListener("click", addImageIndex.bind(null, 1));
      prev.addEventListener("click", addImageIndex.bind(null, -1));
    } else {
      document.querySelector("title").textContent = data.message;
    }
  })
  .catch((error) => {
    console.log(error);
  });

function loadImage(imgURLList) {
  for (let i = 0; i < imgURLList.length; i++) {
    let image = document.createElement("img");
    image.src = imgURLList[i];
    image.classList.add("fade");
    gallery.appendChild(image);
  }
}

function createCurrentImageDot(imgURLList) {
  for (let i = 0; i < imgURLList.length; i++) {
    let span = document.createElement("span");
    span.classList.add("dot");
    span.addEventListener("click", showCurrentImage.bind(null, i));
    picCurrent.appendChild(span);
  }
}

function showImage(n) {
  let images = document.querySelectorAll(".gallery > img");
  let dots = document.querySelectorAll(".dot");
  if (n == images.length) {
    imageIndex = 0;
  }
  if (n < 0) {
    imageIndex = images.length - 1;
  }
  for (let i = 0; i < images.length; i++) {
    images[i].style.display = "none";
  }
  for (let i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  images[imageIndex].style.display = "block";
  dots[imageIndex].className += " active";
}

function addImageIndex(n) {
  showImage((imageIndex += n));
}

function showCurrentImage(n) {
  showImage((imageIndex = n));
}

document.querySelectorAll('input[name="time"]').forEach((element) => {
  element.addEventListener("change", function (e) {
    let target = e.target;
    switch (target.id) {
      case "morning":
        price.textContent = "新台幣 2000元";
        break;
      case "afternoon":
        price.textContent = "新台幣 2500元";
        break;
    }
  });
});

startBookingBtn.addEventListener("click", handleStartBooking);

function handleStartBooking() {
  fetch("/api/user/auth", {
    method: "GET",
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.data != null) {
        bookTrip();
      } else {
        showSignWindow();
      }
    })
    .catch((err) => {
      console.log(err);
    });
}

function bookTrip() {
  if (checkOrderInfo()) {
    let bookingInfo = {
      attractionId: attractionId,
      date: date.value,
      time: document.querySelector('input[name="time"]:checked').value,
      price: parseInt(price.textContent.slice(4, 8)),
    };
    console.log(JSON.stringify(bookingInfo));
    fetch("/api/booking", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(bookingInfo),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.ok) {
          redirectBooking();
        } else {
          alert("請確認預訂資料是否正確");
        }
      })
      .catch((err) => {
        console.log(err);
      });
  } else {
    return;
  }
}

date.min = new Date().toISOString().slice(0, 10);

function checkOrderInfo() {
  let date = document.getElementById("date").value;
  let time = document.querySelector('input[name="time"]:checked');
  if (date === "") {
    alert("請選擇行程日期");
    return false;
  }
  if (time === null) {
    alert("請選擇行程時間");
    return false;
  }
  return true;
}
