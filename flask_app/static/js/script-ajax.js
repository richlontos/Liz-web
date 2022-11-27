const button = document.querySelector('#buy_now_btn')

button.addEventListener('click', event => {

    fetch('/stripe/pay')
    .then((result) => { return result.json(); })

    .then((data) => {
        var stripe = stripe(data.checkout_public_key);
        stripe.redirectToCheckout({

            sessionId: data.checkout_session_id
        }).then(function(result){
            
        });
    })
});
