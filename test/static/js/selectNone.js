let value = true
let radio1 = document.getElementById('btnradio1')
let radio2 = document.getElementById('btnradio2')
let input1 = document.getElementById('team')
let input2 = document.getElementById('nation')
let team = document.getElementById('team')
console.log(team.value)

radio1.addEventListener('click', () => {
    value = !value
    input1.readOnly = false
    input1.value = null
    input2.value = 'None'
    input2.readOnly = true
})

radio2.addEventListener('click', () => {
    value = !value
    input2.readOnly = false
    input2.value = null
    input1.value = 'None'
    input1.readOnly = true
})