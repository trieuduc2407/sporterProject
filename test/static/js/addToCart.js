let minus = document.getElementById('minus')
let plus = document.getElementById('plus')
let add = document.getElementById('add')
let number = 1

minus.addEventListener('click', () => {
    if (number > 1) {
        number--
        document.getElementById('quantity').innerText = number
    }
})

plus.addEventListener('click', () => {
    number++
    document.getElementById('quantity').innerText = number
})