const checkboxes = document.querySelectorAll('input[type="checkbox"]');
const totalSpan = document.getElementById('total');
const form = document.getElementById('form');

function calculateTotal() {
    let total = 0;
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            total += parseInt(checkbox.value);
        }
    });
    totalSpan.textContent = total;
}

checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', calculateTotal);
});

form.addEventListener('submit', (e) => {
    e.preventDefault(); // preventing page reload(the default behaviour when a form is submitted)
    
    const cart = [];
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            cart.push({
                item: checkbox.dataset.item,
                price: parseInt(checkbox.value)
            });
        }
    });
    
    console.log('Selected Items:', cart);

    function addToCart(cart){
        return new Promise((resolve, reject) => {
            if (cart.length == 0){
                reject(new Error("Cart is Empty"))
            }else{
                // cart logic
                resolve(Math.floor(Math.random()));
            }
        });
    }

    function proceedToPayment(orderId){
        return new Promise((resolve, reject) => {
            resolve("Payment Successful");
        });
    }

    addToCart(cart)
    .then((orderId) => console.log(orderId))
    .then(() => proceedToPayment(orderId))
    .catch((err) => console.log(err.message))
});

