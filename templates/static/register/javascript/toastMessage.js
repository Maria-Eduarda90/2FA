const button = document.querySelector('.btn-login');
const username = document.querySelector('.username');
const email = document.querySelector('.email');
const password = document.querySelector('.password');
const confirmPassword = document.querySelector('.confirm_password');
const title = document.querySelector('.title');

button.addEventListener("click", event => {
    event.preventDefault();

    try {
        if(username.value && email.value && password.value && confirmPassword.value) {
            return ToastSuccess("Usuario criado com sucesso!");
        }
    } catch {
        return ToatsError("Error de servidor tente mais tarde");
    }

    // if(username.value === "" || !username.value.trim()){
    //     return ToatsError("Preencha o campo nome");
    // }
})

function ToatsError(message){
    title.innerHTML = message;
    const error = document.querySelector('.snackbar');
    error.classList.add("error");

    setTimeout(function(){
        error.classList.remove("error")
    }, 3000);
}

function ToastSuccess(message){
    title.innerHTML = message;
    const success = document.querySelector('.snackbar');
    success.classList.add("success");

    setTimeout(function(){
        success.classList.remove("success")
    }, 3000)
}