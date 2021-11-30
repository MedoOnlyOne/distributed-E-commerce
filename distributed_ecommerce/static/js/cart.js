function dec(product_id){
    fetch('/dec_product', {
        method: "POST",
        body: JSON.stringify({product_id: product_id}),        
    }).then((_res) => {
        window.location.href = "/";
    });
}

function inc(product_id){
    fetch('/inc_product', {
        method: "POST",
        body: JSON.stringify({product_id: product_id}),        
    }).then((_res) => {
        window.location.href = "/";
    });
}


