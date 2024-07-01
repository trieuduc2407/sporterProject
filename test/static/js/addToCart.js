let minus = document.getElementById('minus')
let plus = document.getElementById('plus')
let add = document.getElementById('add')
let number = 1

let baseUrl = window.origin

minus.addEventListener('click', () => {
    if (number > 1) {
        number--
        document.getElementById('quantity').innerText = number
    }
})

plus.addEventListener('click', () => {
    number++
    document.getElementById('quantity').innerText = number
})

function addToCart(event) {
    let id = event.target.dataset.index;
    let quantity = Number(document.getElementById('quantity').innerText);
    let data = {
        "productId": id,
        "quantity": quantity
    }
    let url = baseUrl + '/cart/add'
    fetch(url, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(data),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })
        .then((response) => {
            if (response.status !== 200) {
                console.log(response.status)
            }
        })
}