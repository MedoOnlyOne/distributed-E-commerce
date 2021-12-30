const addToCartForm = document.querySelectorAll('.add-to-cart-form');
var search = document.getElementById('s');
var search_btn = document.getElementById('b');
search.addEventListener('input',function(){
    if (search.value.length>0){
        search_btn.disabled=false;
    }
    else{
        search_btn.disabled=true;
    }
});
for (const cart of addToCartForm) {
  cart.addEventListener('submit', async (e) => {
    e.preventDefault();
    const p_id = cart.querySelector('.p_id').value;
    const url = e.target.action;
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        product_id: p_id,
      }),
    });
    const data = await response.json();
    const status = data.status;
    const alertMessage = cart.querySelector('.alert-message');
    if (status === 'redirect') window.location.href = '/login';
    console.log(status);
    if (status === 'success') {
      const button = cart.querySelector('.add_to_cart_button');
      button.disabled = true;
      alertMessage.classList.remove('red');
      alertMessage.classList.add('green');
      alertMessage.innerHTML = `Added to cart successfuly`;
    } else if (status === 'failed') {
      alertMessage.classList.remove('green');
      alertMessage.classList.add('red');
      alertMessage.innerHTML = `Error. Try again later`;
    }
  });
}
