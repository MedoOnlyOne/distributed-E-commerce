const addToCartForm = document.querySelector('#add-to-cart-form');

addToCartForm.addEventListener('submit', async e => {
    e.preventDefault();
    const url = e.originalTarget.action;
    console.log(window.location.href.split('/').at(-1));
    const response = await fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'product_id': window.location.href.split('/').at(-1),
        }),
    });
    const data = await response.json();
    const status = data.status;
    const alertMessage = document.querySelector('.alert-message');
    if(status === 'redirect')
        window.location.href = '/login';
    if(status === 'success'){
        const button = document.querySelector('.cart');
        button.disabled = true;
        alertMessage.classList.remove('red');
        alertMessage.classList.add('green');
        alertMessage.innerHTML = `Added to cart successfuly`;
    }
    else if(status === 'failed'){
        alertMessage.classList.remove('green');
        alertMessage.classList.add('red');
        alertMessage.innerHTML = `Error. Try again later`;
    }
})
