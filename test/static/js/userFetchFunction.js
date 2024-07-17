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
        .then(response => response.json())
        .then(data => {
            if (data.Status === 0) {
                let type = 'failed';
                let icon = 'fa fa-times-circle';
                let title = 'Đăng nhập để thêm vào giỏ hàng';
                createToast(type, icon, title);
            } else {
                let type = 'success';
                let icon = 'fa-solid fa-circle-check';
                let title = 'Thêm sản phẩm thành công';
                createToast(type, icon, title);
            }
        })
}

function deleteItem(event) {
    let id = event.currentTarget.dataset.id
    let data = {
        'productId': id
    }

    let url = baseUrl + '/cart/delete'

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
                location.reload()
                alert('Xoá sản phẩm thành công')
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

function login() {
    let username = document.getElementById('username').value
    let password = document.getElementById('password').value
    let data = {
        'username': username,
        'password': password,
    }

    let url = baseUrl + '/login'
    fetch(url, {
        method: 'POST',
        credentials: 'include',
        cache: 'no-cache',
        body: JSON.stringify(data),
        headers: new Headers({
            'content-type': 'application/json'
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.Status === 1) {
                window.location.replace(baseUrl)
            } else {
                let type = 'failed';
                let icon = 'fa fa-times-circle';
                let title = 'Sai tên đăng nhập hoặc mật khẩu';
                createToast(type, icon, title);
            }
        })
}

function userChangeInfo() {
    let fname = document.getElementById('fname').value
    let lname = document.getElementById('lname').value
    let email = document.getElementById('email').value
    let phone = document.getElementById('phone').value
    let data = {
        'fname': fname,
        'lname': lname,
        'email': email,
        'phone': phone,
    }

    let url = baseUrl + '/user'
    fetch(url, {
        method: 'POST',
        credentials: 'include',
        cache: 'no-cache',
        body: JSON.stringify(data),
        headers: new Headers({
            'content-type': 'application/json'
        })
    })
        .then((response) => {
            if (response.status !== 200) {
                console.log(response.status)
            } else {
                alert('Sửa thông tin thành công')
            }
        })
}

function userChangePassword() {
    let oldPass = document.getElementById('old-pass').value
    let newPass = document.getElementById('new-pass').value
    let confirmPass = document.getElementById('confirm-pass').value

    if (newPass !== confirmPass) {
        let type = 'failed';
        let icon = 'fa fa-times-circle';
        let title = 'Mật khẩu xác nhận không trùng với mật khẩu mới'
        createToast(type, icon, title)
    } else {
        let data = {
            'old_password': oldPass,
            'new_password': newPass,
        }

        let url = baseUrl + '/user/change-password'
        fetch(url, {
            method: 'POST',
            credentials: 'include',
            cache: 'no-cache',
            body: JSON.stringify(data),
            headers: new Headers({
                'content-type': 'application/json'
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.code === 0) {
                    let type = 'failed';
                    let icon = 'fa fa-times-circle';
                    let title = 'Mật khẩu cũ không đúng'
                    createToast(type, icon, title)
                } else if (data.code === 1) {
                    let type = 'failed';
                    let icon = 'fa fa-times-circle';
                    let title = 'Mật khẩu mới trùng với mật khẩu cũ'
                    createToast(type, icon, title)
                } else if (data.code === 2) {
                    let type = 'success';
                    let icon = 'fa-solid fa-circle-check';
                    let title = 'Đổi mật khẩu thành công'
                    createToast(type, icon, title)
                }
            })
    }
}