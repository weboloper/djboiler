function validateUsername(username) {
  const alphanumeric = /^[a-zA-Z0-9]*$/;
  if (username.trim() === "") {
    return "Kullanıcı adı boş";
  } else if (username.length < 3) {
    return "Kullanıcı adı çok kısa";
  } else if (!username.match(alphanumeric)) {
    return "Kullanıcı adı sadece harf ve rakamdan oluşabilir";
  } else {
    return "";
  }
}
function validateUsernameOrEmail(usernameOrEmail) {
  if (usernameOrEmail.trim() === "") {
    return "Kullanıcı adı/E-posta boş";
  } else if (usernameOrEmail.length < 3) {
    return "Kullanıcı adı çok kısa";
  } else {
    return "";
  }
}

function validateEmail(email) {
  if (email.trim() === "") {
    return "E-posta boş";
  }
  return "";
}

function validatePassword(password) {
  if (password.length < 6) {
    return "Şifre en az 6 karakterden oluşmalı";
  }
  return "";
}

function validatePasswordsMatch(password, re_password) {
  if (password !== re_password) {
    return "Şifreler eşleşmiyor";
  }
  return "";
}
