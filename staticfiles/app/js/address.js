var upBtns = document.getElementsByClassName('remove-address')

for (i = 0; i < upBtns.length; i++) {
    upBtns[i].addEventListener("click",function(){
    var addressId = this.dataset.address
    var action = this.dataset.action
    console.log("addressId:", addressId, "Action:", action)

    console.log("USER:", user)
    if (user == "AnonymousUser") {
      window.location.href = "/login/"
    } else {
      deleteUserAddress(addressId, action)
    }
  })
}

function deleteUserAddress(addresstId,action){
  console.log("User is logged in,sending data..")

  var url = '/delete_address/'
  fetch(url,{
    method:'POST',
    headers:{
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ 'addressId': addresstId, 'action': action }),
  })
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      console.log("data:", data)
      location.reload()
    });
}