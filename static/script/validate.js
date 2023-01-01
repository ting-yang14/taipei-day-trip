export function checkName(name) {
  const nameReg = /^[a-zA-Z0-9_\u4e00-\u9fa5]{1,10}$/;
  if (nameReg.test(name)) {
    return true;
  } else {
    return false;
  }
}

export function checkEmail(email) {
  const emailReg =
    /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;
  if (emailReg.test(email)) {
    return true;
  } else {
    return false;
  }
}

export function checkPassword(password) {
  const passwordReg = /^[A-Za-z\d@$!%*#?&]{8,}$/;
  if (passwordReg.test(password)) {
    return true;
  } else {
    return false;
  }
}
export function checkDate(date) {
  const dateReg = /^((20[0-9]{2})-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01]))$/;
  let todayDate = new Date();
  todayDate.toISOString().split("T")[0];
  const inputDate = new Date(date);
  if (dateReg.test(date) && inputDate >= todayDate) {
    console.log("teru");
    return true;
  } else {
    console.log("false");
    return false;
  }
}
export function checkPhone(phone) {
  const phoneReg = /^09\d{8}$/;
  if (phoneReg.test(phone)) {
    return true;
  } else {
    return false;
  }
}
export function checkTime(time) {
  const timeReg = /morning|afternoon/;
  if (timeReg.test(time)) {
    return true;
  } else {
    return false;
  }
}
