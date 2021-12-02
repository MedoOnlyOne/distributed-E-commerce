document.querySelector('#minus').addEventListener("click", dec, false);
document.querySelector('#plus').addEventListener("click", inc, false);


/*
$(document).ready(function(){
    $('.countminus').on('click', function(){
        var product_id = $(this).attr('product_id');

        req = $.ajax({
            url: '/inc_product',
            type: 'POST',
            data: {product_id: product_id}
        });

        req.done(function(data){
            $('#quantity_id').text(data.quantity_id)
        });
      });
});
*/

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
