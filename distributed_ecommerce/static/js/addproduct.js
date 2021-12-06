const addToCartForm = document.querySelector('#add-to-cart-form');

const addToShopForm = document.querySelector('#add-to-shop-form');

addToCartForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const url = e.target.action;
  const response = await fetch(url, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      product_id: window.location.href.split('/').at(-1),
    }),
  });
  const data = await response.json();
  const status = data.status;
  const alertMessage = document.querySelector('.alert-message');
  if (status === 'redirect') window.location.href = '/login';
  if (status === 'success') {
    const button = document.querySelector('#add_to_cart_button');
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

addToShopForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const url = e.target.action;
  const response = await fetch(url, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      product_id: window.location.href.split('/').at(-1),
    }),
  });
  const data = await response.json();
  const status = data.status;
  const alertMessage = document.querySelector('.alert-message');
  if (status === 'redirect') window.location.href = '/login';
  if (status === 'success') {
    const button = document.querySelector('#add_to_shop_button');
    button.disabled = true;
    alertMessage.classList.remove('red');
    alertMessage.classList.add('green');
    alertMessage.innerHTML = `Added to shop successfuly`;
  } else if (status === 'failed') {
    alertMessage.classList.remove('green');
    alertMessage.classList.add('red');
    alertMessage.innerHTML = `Error. Try again later`;
  }
});
