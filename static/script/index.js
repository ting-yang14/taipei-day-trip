let nextPage = 0;
let keyword = "";

const attractionsApi = `/api/attractions?page=`;
const categoriesApi = `/api/categories`;
const main = document.querySelector("main");
const footer = document.querySelector("footer");
const categoryList = document.querySelector(".category-list");
const searchInput = document.getElementById("search-input");
const searchBtn = document.getElementById("search-btn");
const observer = new IntersectionObserver(function (entries) {
  if (entries[0].isIntersecting && nextPage != null) {
    generateAttractionDiv(
      `${attractionsApi}${nextPage.toString()}&keyword=${keyword}`
    );
  } else {
    return;
  }
});

document.addEventListener("click", (e) => {
  if (
    categoryList.style.display == "block" &&
    !categoryList.contains(e.target) &&
    !searchInput.contains(e.target)
  ) {
    categoryList.style.display = "none";
  }
});
searchInput.addEventListener("click", showCategoryList);
searchBtn.addEventListener("click", filterAttractions);

generateBasicAttractions();
createCategoryBtn(categoriesApi);

function showCategoryList() {
  let catBtn = Array.from(document.querySelectorAll(".cat-btn"));
  catBtn.forEach((button) => button.addEventListener("click", setCategory));
  categoryList.style.display = "block";
}

function setCategory(event) {
  let category = event.target.textContent;
  searchInput.value = category;
  categoryList.style.display = "none";
}
function generateBasicAttractions() {
  fetch(`${attractionsApi}${nextPage.toString()}&keyword=${keyword}`)
    .then((response) => response.json())
    .then((data) => {
      nextPage = data.nextPage;
      loadAttractions(data.data);
      observer.observe(footer);
    });
}

function filterAttractions() {
  keyword = searchInput.value;
  nextPage = 0;
  observer.unobserve(footer);
  fetch(`${attractionsApi}${nextPage.toString()}&keyword=${keyword}`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data.data);
      if (data.data.length === 0) {
        alert("查無此景點！！");
      } else {
        while (main.firstChild) {
          main.removeChild(main.firstChild);
        }
        loadAttractions(data.data);
        nextPage = data.nextPage;
        observer.observe(footer);
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

function generateAttractionDiv(URL) {
  fetch(URL)
    .then((response) => response.json())
    .then((data) => {
      nextPage = data.nextPage;
      loadAttractions(data.data);
    })
    .catch((error) => {
      console.log(error);
    });
}

function loadAttractions(attractionList) {
  for (let i = 0; i < 12; i++) {
    let attractionDiv = createAttractionElement(
      attractionList[i].images[0],
      attractionList[i].name,
      attractionList[i].mrt,
      attractionList[i].category
    );
    main.appendChild(attractionDiv);
  }
}

function createAttractionElement(imgURL, name, mrt, category) {
  const newDiv = document.createElement("div");
  newDiv.classList.add("attraction", "border");
  const attractionImg = document.createElement("img");
  attractionImg.src = imgURL;
  const nameDiv = document.createElement("div");
  nameDiv.classList.add("attraction-name");
  const nameP = document.createElement("p");
  nameP.classList.add("bold");
  const attractionName = document.createTextNode(name);
  nameP.appendChild(attractionName);
  nameDiv.appendChild(nameP);
  const infoDiv = document.createElement("div");
  infoDiv.classList.add("attraction-info");
  const mrtP = document.createElement("p");
  const categoryP = document.createElement("p");
  mrtP.classList.add("reg");
  const attractionMRT = document.createTextNode(mrt);
  mrtP.appendChild(attractionMRT);
  categoryP.classList.add("reg");
  const attractionCategory = document.createTextNode(category);
  categoryP.appendChild(attractionCategory);
  infoDiv.appendChild(mrtP);
  infoDiv.appendChild(categoryP);
  newDiv.appendChild(attractionImg);
  newDiv.appendChild(nameDiv);
  newDiv.appendChild(infoDiv);
  return newDiv;
}

function createCategoryBtn(URL) {
  fetch(URL)
    .then((response) => response.json())
    .then((data) => data.data)
    .then((categories) => {
      for (let i = 0; i < categories.length; i++) {
        let categoryBtn = document.createElement("button");
        categoryBtn.classList.add("cat-btn");
        let categoryName = document.createTextNode(categories[i]);
        categoryBtn.appendChild(categoryName);
        categoryList.appendChild(categoryBtn);
      }
    })
    .catch((error) => {
      console.log(error);
    });
}
