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
        .then((response) => {
            if (response.status !== 200) {
                console.log(response.status)
            }
            alert("Cập nhật giá thành công")
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
        .then((response) => {
            if (response.status !== 200) {
                console.log(response.status)
            } else {
                alert("Cập nhật số lượng thành công")
            }
        })
}

function deleteProduct(event) {
    if (confirm("Xoá sản phẩm?")) {
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
            .then((response) => {
                if (response.status !== 200) {
                    console.log(response.status)
                }
                location.reload()
            })
    }
}

function adminLogin() {
    let url = baseUrl + '/admin/login'
    let username = document.getElementById('email_field').value
    let password = document.getElementById('password_field').value
    let data = {
        'username': username,
        'password': password,
    }
    fetch(url, {
        method: "POST",
        credentials: "include",
        cache: "no-cache",
        body: JSON.stringify(data),
        headers: new Headers({
            'content-type': 'application/json'
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.Status === 1) {
                window.location.replace(baseUrl + '/admin')
            } else {
                let type = 'failed';
                let icon = 'fa fa-times-circle';
                let title = 'Sai tên đăng nhập hoặc mật khẩu';
                createToast(type, icon, title);
            }
        })
}