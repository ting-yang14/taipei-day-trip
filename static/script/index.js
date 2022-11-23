let nextPage = 0;
let keyword = "";
let dataList = [];
const main = document.querySelector("main");

const attractionsApi = "/api/attractions?page=";

const categoryList = document.querySelector(".category-list");
const categoriesApi = "api/categories";

generateCategoryBtn(categoriesApi);
const observer = new IntersectionObserver(function (entries) {
  console.log(entries);
  if (entries[0].isIntersecting && nextPage != null) {
    generateAttractionDiv(
      attractionsApi + nextPage.toString() + "&keyword=" + keyword
    );
  } else {
    return;
  }
});
observer.observe(document.querySelector("footer"));
// generateAttractionDiv(attractionsApi + "0");
function createAttraction(imgURL, name, mrt, category) {
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
  /* 
  <div class="attraction border">
    <img src=imgURL />
    <div class="attraction-name">
      <p class="bold">name</p>
    </div>
    <div class="attraction-info">
      <p class="reg">mrt</p>
      <p class="reg">category</p>
    </div>
  </div> 
  */
  return newDiv;
}

function generateAttractionDiv(URL) {
  fetch(URL)
    .then((response) => response.json())
    .then((data) => {
      nextPage = data.nextPage;
      return data.data;
    })
    .then((attractions) => {
      for (let i = 0; i < 12; i++) {
        let attractionDiv = createAttraction(
          attractions[i].images[0],
          attractions[i].name,
          attractions[i].mrt,
          attractions[i].category
        );
        main.appendChild(attractionDiv);
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

function generateCategoryBtn(URL) {
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
        // <button class="cat-btn">category</button>
      }
    })
    .catch((error) => {
      console.log(error);
    });
}
document
  .getElementById("search-btn")
  .addEventListener("click", filterAttractions);
function filterAttractions() {
  keyword = document.getElementById("search-input").value;
  fetch(attractionsApi + "0&keyword=" + keyword)
    .then((response) => response.json())
    .then((data) => {
      console.log(data.data);
      if (data.data.length === 0) {
        alert("查無此景點！！");
      } else {
        nextPage = 0;
        console.log(nextPage);

        while (main.firstChild) {
          main.removeChild(main.firstChild);
        }
        nextPage = data.nextPage;
      }
    })
    .catch((error) => {
      console.log(error);
    });
}
function getData(URL) {
  fetch(URL)
    .then((response) => response.json())
    .then((data) => {
      nextPage = data.nextPage;
      dataList = data.data;
    })
    .catch((error) => {
      console.log(error);
    });
}
function generateAttractions(attractionList) {
  for (let i = 0; i < 12; i++) {
    let attractionDiv = createAttraction(
      attractionList[i].images[0],
      attractionList[i].name,
      attractionList[i].mrt,
      attractionList[i].category
    );
    main.appendChild(attractionDiv);
  }
}
