const gallery = document.querySelector(".gallery");
const picCurrent = document.querySelector(".pic-current");
const attractionName = document.getElementById("name");
const category = document.getElementById("category");
const mrt = document.getElementById("mrt");
const fee = document.getElementById("fee");
const description = document.getElementById("description");
const address = document.getElementById("address");
const transport = document.getElementById("transport");
const next = document.querySelector(".next");
const prev = document.querySelector(".prev");
let imageIndex = 0;

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
  for (i = 0; i < images.length; i++) {
    images[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
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

fetch(`/api${window.location.pathname}`)
  .then((response) => response.json())
  .then((data) => {
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
  })
  .catch((error) => {
    console.log(error);
  });

document.querySelectorAll('input[name="trip-time"]').forEach((element) => {
  element.addEventListener("change", function (e) {
    let target = e.target;
    switch (target.id) {
      case "morning":
        fee.textContent = "新台幣 2000元";
        break;
      case "afternoon":
        fee.textContent = "新台幣 2500元";
        break;
    }
  });
});
