var updateButton = document.getElementsByClassName("update-wishlist");

for (i = 0; i < updateButton.length; i++) {
  updateButton[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log("productId:", productId, "Action:", action);

    console.log("USER:", user);
    if (user == "AnonymousUser") {
      window.location.href = "/login/";
    } else {
      updateUserWishlist(productId, action);
    }
  });
}

function updateUserWishlist(productId, action) {
  console.log("User is logged in,sending data..");

  var url = "/update_wishlist/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("data:", data);
      location.reload();
    });
}
