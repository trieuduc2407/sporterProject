let baseUrl = window.origin

function updatePrice(event) {
    let id = event.target.dataset.priceIndex;
    let price = document.querySelector("[data-price-id='" + id + "']").value
    let data = {
        "price": price
    }
    let url = baseUrl + '/admin/update/price/' + id
    fetch(url, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(data),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })
        .then((respone) => {
            if (respone.status !== 200) {
                console.log(respone.status)
            }
            alert("updated")
        })
}

function updateQuantity(event) {
    let id = event.target.dataset.quantityIndex;
    let quantity = document.querySelector("[data-quantity-id='" + id + "']").value
    let data = {
        "quantity": quantity
    }
    let url = baseUrl + '/admin/update/quantity/' + id
    fetch(url, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(data),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })
        .then((respone) => {
            if (respone.status !== 200) {
                console.log(respone.status)
            }
            alert("updated")
        })
}

function deleteProduct(event) {
    if (confirm("delete?")) {
        let id = event.target.dataset.deleteIndex;
        let url = baseUrl + '/admin/delete/' + id
        fetch(url, {
            method: "POST",
            credentials: "include",
            cache: "no-cache",
            body: JSON.stringify(id),
            headers: new Headers({
                "content-type": "application/json"
            })
        })
            .then((respone) => {
                if (respone.status !== 200) {
                    console.log(respone.status)
                }
                location.reload()
            })
    }
}