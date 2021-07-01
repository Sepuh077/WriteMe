var is_login_clicked = True
const form = {{ form }}

const page = document.getElementsByClassName('form')

const login_button = document.getElementsByClassName('login')
const sign_up_button = document.getElementsByClassName('sign_up')

login_button.addEventListener('click', event => {
    is_login_clicked = True
})

sign_up_button.addEventListener('click', event => {
    is_login_clicked = False
})

page.innerHTML = '';
if (is_login_clicked) {
    const username_input = document.createElement('input')
    username_input.name = 'username'
    page.appendChild(username_input)
}
else {
    page.appendChild(form)
}