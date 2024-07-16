function formatString(x) {
    return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ".") + " " + "VND";
}

let baseUrl = window.origin

let subtotal = document.querySelectorAll('.subtotal');
let total = document.getElementById('total')
let totalValue = 0

for (let i = 0; i < subtotal.length; i++) {
    let subPrice = Number(subtotal[i].dataset.itemPrice) * Number(subtotal[i].dataset.itemQuantity)
    totalValue += subPrice
    subtotal[i].innerText = formatString(subPrice)
}


total.innerText = formatString(totalValue)


function checkout() {
    let fname = document.getElementsByName('fname')[0].value
    let lname = document.getElementsByName('lname')[0].value
    let address = document.getElementsByName('address')[0].value
    let email = document.getElementsByName('email')[0].value
    let phone = document.getElementsByName('phone')[0].value
    let note = document.getElementsByName('note')[0].value
    let btn1 = document.getElementById('flexRadioDefault1')
    let payment = 1
    if (btn1.checked === true) {
        payment = 1
    } else if (btn1.checked === false) {
        payment = 2
    }

    let data = {
        'fname': fname,
        'lname': lname,
        'address': address,
        'email': email,
        'phone': phone,
        'note': note,
        'payment': payment,
        'total': totalValue
    }

    let url = baseUrl + '/checkout'

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
                window.location.replace(baseUrl)
            }
        })

}