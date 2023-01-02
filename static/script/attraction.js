// import { checkDate, checkTime } from "./validate.js";
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

attraction_init();

async function attraction_init() {
  try {
    const res = await fetch(`/api${window.location.pathname}`);
    const data = await res.json();
    attractionId = data.data.id;
    setAttractionInfo(data);
    loadImage(data.data.images);
    createCurrentImageDot(data.data.images);
    showImage(imageIndex);
    next.addEventListener("click", addImageIndex.bind(null, 1));
    prev.addEventListener("click", addImageIndex.bind(null, -1));
  } catch (err) {
    console.log(err);
  }
}

function setAttractionInfo(data) {
  document.querySelector("title").textContent = data.data.name;
  attractionName.textContent = data.data.name;
  category.textContent = data.data.category;
  mrt.textContent = data.data.mrt;
  description.textContent = data.data.description;
  address.textContent = data.data.address;
  transport.textContent = data.data.transport;
}

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
  images.forEach((image) => {
    image.style.display = "none";
  });
  dots.forEach((dot) => {
    dot.className = dot.className.replace(" active", "");
  });
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

async function handleStartBooking() {
  try {
    const res = await fetch("/api/user/auth", {
      method: "GET",
    });
    const data = await res.json();
    if (data.data != null) {
      bookTrip();
    } else {
      showSignWindow();
    }
  } catch (err) {
    console.log(err);
  }
}

function bookTrip() {
  if (checkTripInfo()) {
    let bookingInfo = {
      attractionId: attractionId,
      date: date.value,
      time: document.querySelector('input[name="time"]:checked').value,
      price: parseInt(price.textContent.slice(4, 8)),
    };
    console.log(bookingInfo);
    (async () => {
      try {
        const res = await fetch("/api/booking", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(bookingInfo),
        });
        const data = await res.json();
        if (data.ok) {
          redirectBooking();
        } else {
          alert("請確認預訂資料是否正確");
        }
      } catch (err) {
        console.log(err);
      }
    })();
  } else {
    return;
  }
}

date.min = new Date().toISOString().slice(0, 10);

function checkTripInfo() {
  let date = document.getElementById("date").value;
  let time = document.querySelector('input[name="time"]:checked');
  if (date === "") {
    alert("請選擇行程日期");
    return false;
  }
  if (time === "") {
    alert("請選擇行程時間");
    return false;
  }
  return true;
}
