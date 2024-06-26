let success = document.getElementById('add');
let notifications = document.querySelector('.notifications');

function createToast(type, icon, title) {
    let newToast = document.createElement('div');
    newToast.innerHTML = `
        <div class="toast ${type}">
                <i class="${icon}"></i>
                <div class="content">
                    <div class="title">${title}</div>
                </div>
                <i class="close fa-solid fa-xmark"
                onclick="(this.parentElement).remove()"
                ></i>
            </div>`;

    notifications.appendChild(newToast);
    newToast.timeOut = setTimeout(() => newToast.remove(), 3000)
}

success.addEventListener('click', () => {
    let type = 'success';
    let icon = 'fa-solid fa-circle-check';
    let title = 'Thêm sản phẩm thành công';
    createToast(type, icon, title);
})