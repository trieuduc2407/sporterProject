function formatString(x) {
    return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ".") + " " + "VND";
}

let price = document.querySelectorAll('.item-price')

for (let i = 0; i < price.length; i++) {
    price[i].innerText = formatString(price[i].innerText)
}