let nextPage = 0;

const main = document.querySelector("main");
basicURL = "http://192.168.1.143:3000/api/attractions?page=0";
generateAttractionDiv(basicURL);
const categoryList = document.querySelector(".category-list");
categoryURL = "http://192.168.1.143:3000/api/categories";
generateCategoryBtn(categoryURL);

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

// function loadMore() {
//   // 利用 fetch 進行連線並取得資料
//   promise.then(function (attractionList) {
//     // 每次新增 8 個 titleItem
//     for (let i = itemNum; i < itemNum + 8; i++) {
//       let newDiv = createItem(
//         str.concat(attractionList[i].file.split(str)[1]),
//         attractionList[i].stitle
//       );
//       newDiv.className = "title";
//       titleList.appendChild(newDiv);
//       // console.log(i); // 檢查目前的 item 編號
//     }
//     return (itemNum += 8);
//   });
// }
