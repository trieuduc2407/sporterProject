function formatString(x) {
    return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ".") + " " + "VND";
}

let itemPrice = document.getElementById('item-price');
itemPrice.innerText = formatString(itemPrice.innerText);

