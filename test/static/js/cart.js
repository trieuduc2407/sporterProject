function formatString(x) {
    return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ".") + " " + "VND";
}

let price = document.querySelectorAll('.item-price')
let priceMd = document.querySelectorAll('.item-price-md')
let quantity = document.querySelectorAll('.quantity')
let subtotal = document.querySelectorAll('.item-subtotal')
let total = document.getElementById('total')
let value = 0

for (let i = 0; i < price.length; i++) {
    price[i].innerText = formatString(price[i].dataset.price);
}

for (let i = 0; i < priceMd.length; i++) {
    priceMd[i].innerText = formatString(priceMd[i].dataset.price);
}

for (let i = 0; i < price.length; i++) {
    subtotal[i].innerText = formatString(Number(price[i].dataset.price) * Number(quantity[i].innerText))
}

for (let i = 0; i < price.length; i++) {
    value += Number(price[i].dataset.price) * Number(quantity[i].innerText)
}

total.innerText = formatString(value)


function increase(event) {
    let id = event.currentTarget.dataset.index
    let quantity = document.getElementById(id)
    quantity.innerText = Number(quantity.innerText) + 1
    document.querySelector("[data-subtotal-index='" + id + "']").innerText = formatString(Number(quantity.innerText) * Number(event.currentTarget.dataset.price))
}

function decrease(event) {
    let id = event.currentTarget.dataset.index
    let quantity = document.getElementById(id)

    if (Number(quantity.innerText > 1)) {
        quantity.innerText = Number(quantity.innerText) - 1
        document.querySelector("[data-subtotal-index='" + id + "']").innerText = formatString(Number(quantity.innerText) * Number(event.currentTarget.dataset.price))
    }
}