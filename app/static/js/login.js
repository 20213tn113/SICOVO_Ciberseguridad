(function () {
    const body = document.querySelector('body');
    body.classList.add('text-center');
})();

function convertirAMayusculasU() {
    var input = document.getElementById("usuario");
    input.value = input.value.toUpperCase();
}



(function () {

    const loginButton = document.querySelectorAll('.loginButton');
    const unsafeChars = ["'", '"', ";", "--", "#"];
    usuario = document.getElementById('usuario').value;
    password = document.getElementById('password').value;

    loginButton.forEach((btn) => {
        btn.addEventListener('click', function () {

            usuario = document.getElementById('usuario').value;
            password = document.getElementById('password').value;
            
            const containsUnsafeChars = unsafeChars.some(char => usuario.includes(char) || password.includes(char));

            if (containsUnsafeChars) {
                Swal.fire({
                    position: "top-start",
                    icon: "warning",
                    title: "No se permiten simbolos especiales",
                    showConfirmButton: false,
                    timer: 9500
                });
            
            } else {

                const params = new URLSearchParams({
                    usuario: usuario,
                    password: password
                }).toString();
                window.location.href = `/login2?${params}`;

                
                // return fetch(`${window.origin}/login`, {
                //     method: 'POST',
                //     mode: 'same-origin',
                //     credentials: 'same-origin',
                //     headers: {
                //         'Content-Type': 'application/json',
                //         // 'X-CSRF-TOKEN': csrf_token
                //     },
                //     body: JSON.stringify({
                //         'usuario' : usuario,
                //         'password' : password
                //     })
                // })

            }
        })
    });
})();