let value = true
let radio1 = document.getElementById('btnradio1')
let radio2 = document.getElementById('btnradio2')
let input1 = document.getElementById('team')
let input2 = document.getElementById('nation')

radio1.addEventListener('click', () => {
    value = !value
    input1.disabled = false
    input2.disabled = true
    input2.value = null
})

radio2.addEventListener('click', () => {
    value = !value
    input2.disabled = false
    input1.disabled = true
    input1.value = null
})