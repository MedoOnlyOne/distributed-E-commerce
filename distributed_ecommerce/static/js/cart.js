const numberOfProducts =
  document.querySelector('.itemscontainer').children.length;

const totalPriceElement = document.querySelector('#total-price');

const changeTotalPrice = () => {
  let totalPrice = 0;
  for (let i = 0; i < numberOfProducts; i++) {
    const incButton = document.querySelector(`#plus${i + 1}`);
    const quantityElement = incButton.parentElement.children[3].children[0];
    const quantity = parseInt(quantityElement.innerHTML.split(':').at(-1));
    const priceElement = incButton.parentElement.children[5];
    const price = parseInt(priceElement.innerHTML.split(':').at(-1));
    totalPrice += price * quantity;
  }
  totalPriceElement.innerHTML = `Total = ${totalPrice} L.E`;
};

changeTotalPrice();

const incButtonsHandler = (incButton, index) => () => {
  const quantityElement = incButton.parentElement.children[3].children[0];
  const oldQuantity = parseInt(quantityElement.innerHTML.split(':').at(-1));
  quantityElement.innerHTML = `Quantity: ${
    oldQuantity + 1 > stocks[index] ? oldQuantity : oldQuantity + 1
  }`;
  changeTotalPrice();
};

const decButtonsHandler = (decButton) => () => {
  const quantityElement = decButton.parentElement.children[3].children[0];
  const oldQuantity = parseInt(quantityElement.innerHTML.split(':').at(-1));
  quantityElement.innerHTML = `Quantity: ${
    oldQuantity - 1 < 1 ? 1 : oldQuantity - 1
  }`;
  changeTotalPrice();
};

for (let i = 0; i < numberOfProducts; i++) {
  const incButton = document.querySelector(`#plus${i + 1}`);
  const decButton = document.querySelector(`#minus${i + 1}`);
  incButton.addEventListener('click', incButtonsHandler(incButton, i));
  decButton.addEventListener('click', decButtonsHandler(decButton));
}

const proceedToCheckoutButton = document.querySelector('#checkout_btn');

proceedToCheckoutButton.addEventListener('click', async () => {
  const url = `http://localhost:5000/savecart`;
  const quantities = [];
  for (let i = 0; i < numberOfProducts; i++) {
    const incButton = document.querySelector(`#plus${i + 1}`);
    const quantityElement = incButton.parentElement.children[3].children[0];
    const quantity = parseInt(quantityElement.innerHTML.split(':').at(-1));
    quantities.push(quantity);
  }
  const response = await fetch(url, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      quantities,
    }),
  });
  const data = await response.json();
  const status = data.status;
  const alertMessage = document.querySelector('.alert-message');
  if (status === 'success') {
    window.location.href = '/checkout';
  } else if (status === 'failed') {
    alertMessage.classList.add('red');
    alertMessage.innerHTML = `Error. Try again later`;
  }
});
