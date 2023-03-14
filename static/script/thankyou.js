const getUrlString = location.href;
const url = new URL(getUrlString);
const number = url.searchParams.get("number");
const orderStatus = document.getElementById("orderStatus");
const orderNumber = document.getElementById("orderNumber");
const orderMsg = document.getElementById("orderMsg");
const cardFront = document.querySelector(".flip-card-front");
const cardBack = document.querySelector(".flip-card-back");

thankyou_init(number);

async function thankyou_init(number) {
  try {
    const res = await fetch(`/api/order/${number}`);
    const data = await res.json();
    if (data.data) {
      orderNumber.textContent = data.data.number;
      if (data.data.status === 0) {
        showOrderSuccess(data);
      } else {
        showOrderFail();
      }
    }
  } catch (err) {
    console.log(err);
  }
}
function showOrderSuccess(data) {
  orderStatus.textContent = "行程預定成功";
  cardFront.style.backgroundImage = `url("/img/order_success_1.png")`;
  cardBack.style.backgroundImage = `url("/img/order_success_2.png")`;
  orderMsg.textContent = `期待${data.data.trip.date}與您相遇`;
}
function showOrderFail() {
  orderStatus.textContent = "行程預定失敗";
  cardFront.style.backgroundImage = `url("/img/order_fail_1.png")`;
  cardBack.style.backgroundImage = `url("/img/order_fail_2.png")`;
  orderMsg.textContent = `如有問題，請聯絡客服中心`;
}
