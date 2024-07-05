let baseUrl = window.origin

function addToCart(event) {
    let id = event.target.dataset.index;
    let quantity = Number(document.getElementById('quantity').innerText);
    let data = {
        'productId': id,
        'quantity': quantity
    }

    let url = baseUrl + '/cart/add'

    fetch(url, {
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify(data),
        cache: 'no-cache',
        headers: new Headers({
            'content-type': 'application/json'
        })
    })
        .then((response) => {
            if (response.status !== 200) {
                console.log(response.status)
            }
        })
}

function quickAddToCart(event) {
    let id = event.currentTarget.dataset.index;
    let quantity = 1
    let data = {
        'productId': id,
        'quantity': quantity
    }

    let url = baseUrl + '/cart/add'

    fetch(url, {
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify(data),
        cache: 'no-cache',
        headers: new Headers({
            'content-type': 'application/json'
        })
    })
        .then((response) => {
            if (response.status !== 200) {
                console.log(response.status)
            }
        })
}

function updateCart() {
    let itemIdList = document.querySelectorAll('.item-id')
    let data = []
    for (let i = 0; i < itemIdList.length; i++) {
        let quantity = document.getElementById(itemIdList[i].value)
        data.push({'productId': itemIdList[i].value, 'quantity': quantity.innerText})
    }

    let url = baseUrl + '/cart/update'

    fetch(url, {
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify(data),
        cache: 'no-cache',
        headers: new Headers({
            'content-type': 'application/json'
        })
    })
        .then((response) => {
            if (response.status !== 200) {
                console.log(response.status)
            } else {
                let value = 0
                for (let i = 0; i < price.length; i++) {
                    value += Number(price[i].dataset.price) * Number(quantity[i].innerText)
                }
                total.innerText = formatString(value)
                alert('Cập nhật giỏ hàng thành công')
            }
        })
}