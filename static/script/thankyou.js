const getUrlString = location.href;
const url = new URL(getUrlString);
const Number = url.searchParams.get("number");
const orderStatus = document.getElementById("orderStatus");
const orderNumber = document.getElementById("orderNumber");
const orderMsg = document.getElementById("orderMsg");
const cardFront = document.querySelector(".flip-card-front");
const cardBack = document.querySelector(".flip-card-back");

fetch(`/api/order/${Number}`)
  .then((res) => res.json())
  .then((data) => {
    if (data.data) {
      orderNumber.textContent = data.data.number;
      if (data.data.status === 0) {
        orderStatus.textContent = "行程預定成功";
        cardFront.style.backgroundImage = `url("/img/order_success_1.png")`;
        cardBack.style.backgroundImage = `url("/img/order_success_2.png")`;
        orderMsg.textContent = `期待${data.data.trip.date}與您相遇`;
      } else {
        orderStatus.textContent = "行程預定失敗";
        cardFront.style.backgroundImage = `url("/img/order_fail_1.png")`;
        cardBack.style.backgroundImage = `url("/img/order_fail_2.png")`;
        orderMsg.textContent = `如有問題，請聯絡客服中心`;
      }
    }
  })
  .catch((err) => console.log(err));
