function increase(event) {
    let id = event.target.dataset.quantityIndex
    let quantity = document.querySelector("[data-quantity-id='" + id + "']").value
    quantity += 1
    quantity.innerText = quantity
}

function decrease(event) {
    let id = event.target.dataset.quantityIndex
    let quantity = document.querySelector("[data-quantity-id='" + id + "']").value
    if (quantity > 1) {
        quantity -= 1
        quantity.innerText = quantity
    }
}