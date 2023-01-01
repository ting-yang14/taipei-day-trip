let nextPage = 0;
const main = document.querySelector("main");
const footer = document.querySelector("footer");
const categoryList = document.querySelector(".category-list");
const searchInput = document.getElementById("search-input");
const searchBtn = document.getElementById("search-btn");
const observer = new IntersectionObserver((entries) => {
  if (entries[0].isIntersecting && nextPage != null) {
    loadMoreAttractions();
  }
});

attractionsInit();
createCategoryList();
searchInput.addEventListener("click", showCategoryList);
searchBtn.addEventListener("click", createSearchedAttractions);
document.addEventListener("click", (e) => {
  if (
    categoryList.style.display == "block" &&
    !categoryList.contains(e.target) &&
    !searchInput.contains(e.target)
  ) {
    categoryList.style.display = "none";
  }
});

async function attractionsInit() {
  try {
    const keyword = searchInput.value;
    const res = await fetch(
      `/api/attractions?page=${nextPage.toString()}&keyword=${keyword}`
    );
    const data = await res.json();
    nextPage = data.nextPage;
    createAttractionElements(data.data);
    observer.observe(footer);
  } catch (err) {
    console.log(err);
  }
}

function createAttractionElements(attractionInfoList) {
  attractionInfoList.forEach((attractionInfo) => {
    const attractionDiv = createAttractionElement(attractionInfo);
    main.appendChild(attractionDiv);
  });
}

async function loadMoreAttractions() {
  try {
    const keyword = searchInput.value;
    const res = await fetch(
      `/api/attractions?page=${nextPage.toString()}&keyword=${keyword}`
    );
    const data = await res.json();
    nextPage = data.nextPage;
    createAttractionElements(data.data);
  } catch (err) {
    console.log(err);
  }
}

async function createSearchedAttractions() {
  try {
    const keyword = searchInput.value;
    nextPage = 0;
    observer.unobserve(footer);
    const res = await fetch(
      `/api/attractions?page=${nextPage.toString()}&keyword=${keyword}`
    );
    const data = await res.json();
    if (data.data.length === 0) {
      alert("無此關鍵字相關景點");
      return;
    }
    while (main.firstChild) {
      main.removeChild(main.firstChild);
    }
    createAttractionElements(data.data);
    nextPage = data.nextPage;
    observer.observe(footer);
  } catch (err) {
    console.log(err);
  }
}

async function createCategoryList() {
  try {
    const res = await fetch(`/api/categories`);
    const data = await res.json();
    const categories = await data.data;
    categories.forEach((category) => {
      generateCategoryBtn(category);
    });
  } catch (err) {
    console.log(err);
  }
}

function generateCategoryBtn(category) {
  const categoryBtn = document.createElement("button");
  categoryBtn.classList.add("cat-btn");
  const categoryName = document.createTextNode(category);
  categoryBtn.appendChild(categoryName);
  categoryList.appendChild(categoryBtn);
}

function showCategoryList() {
  const catBtn = Array.from(document.querySelectorAll(".cat-btn"));
  catBtn.forEach((button) => button.addEventListener("click", setCategory));
  categoryList.style.display = "block";
}

function setCategory(event) {
  const category = event.target.textContent;
  searchInput.value = category;
  categoryList.style.display = "none";
}

function createAttractionElement(attractionInfo) {
  const a = document.createElement("a");
  a.href = `/attraction/${attractionInfo.id}`;
  const containerDiv = document.createElement("div");
  containerDiv.classList.add("attraction", "border");
  const attractionImg = document.createElement("img");
  attractionImg.src = attractionInfo.images[0];
  const nameDiv = document.createElement("div");
  nameDiv.classList.add("attraction-name");
  const nameP = document.createElement("p");
  nameP.classList.add("bold");
  const attractionName = document.createTextNode(attractionInfo.name);
  nameP.appendChild(attractionName);
  nameDiv.appendChild(nameP);
  const infoDiv = document.createElement("div");
  infoDiv.classList.add("attraction-info");
  const mrtP = document.createElement("p");
  const categoryP = document.createElement("p");
  mrtP.classList.add("reg");
  const attractionMRT = document.createTextNode(attractionInfo.mrt);
  mrtP.appendChild(attractionMRT);
  categoryP.classList.add("reg");
  const attractionCategory = document.createTextNode(attractionInfo.category);
  categoryP.appendChild(attractionCategory);
  infoDiv.appendChild(mrtP);
  infoDiv.appendChild(categoryP);
  containerDiv.appendChild(attractionImg);
  containerDiv.appendChild(nameDiv);
  containerDiv.appendChild(infoDiv);
  a.appendChild(containerDiv);
  return a;
}
