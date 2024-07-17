let minus = document.getElementById('minus')
let plus = document.getElementById('plus')
let add = document.getElementById('add')
let number = 1

minus.addEventListener('click', () => {
    // Lang nghe su kien click
    if (number > 1) {
        // Neu number(quantity) > 1
        number--
        // Giam gia tri cua number 1 don vi
        // Cap nhat gia tri moi cua number cho quantity
        document.getElementById('quantity').innerText = number
    }
})

plus.addEventListener('click', () => {
    // Lang nghe su kien click
    number++
    // Tang gia tri cua number 1 don vi
    // Cap nhat gia tri moi cua number cho quantity
    document.getElementById('quantity').innerText = number
})