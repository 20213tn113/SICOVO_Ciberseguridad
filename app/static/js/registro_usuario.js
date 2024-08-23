(function () {
    const body = document.querySelector('body');
    body.classList.add('text-center');
})();

function convertirAMayusculasU() {
    var input = document.getElementById("usuario");
    input.value = input.value.toUpperCase();
}


function convertirAMayusculasN() {
    var input = document.getElementById("nombre");
    input.value = input.value.toUpperCase();
}

function convertirAMayusculasA() {
    var input = document.getElementById("apellido");
    input.value = input.value.toUpperCase();
}

function validarNumeros(input) {
    input.value = input.value.replace(/[^0-9]/g, '');
    if (input.value.length > 10) {
        input.value = input.value.slice(0, 10);
    }
}

(function () {
    const btnRegistrarUsuario = document.querySelectorAll('.btnRegistrarUsuario');
    let usuario = null;
    // const csrf_token = document.querySelector("[name='csrf-token']").value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    btnRegistrarUsuario.forEach((btn) => {
        btn.addEventListener('click', function () {
            nombre = document.getElementById('nombre').value;
            apellido = document.getElementById('apellido').value;
            usuario = document.getElementById('usuario').value;
            password = document.getElementById('password').value;
            correo = document.getElementById('correo').value;
            domicilio = document.getElementById('domicilio').value;
            telefono = document.getElementById('telefono').value;

            if (usuario.trim() === '', apellido.trim() === '', password.trim() === '', correo.trim() === '', domicilio.trim() === '', telefono.trim() === '') {
                Swal.fire({
                    position: "top-start",
                    icon: "warning",
                    title: "Llene todos los campos",
                    showConfirmButton: false,
                    timer: 1500
                });
            } else if (emailRegex.test(correo)) {
                confirmarComprar();
            } else {
                Swal.fire({
                    position: "top-start",
                    icon: "warning",
                    title: "Inserte un correo valido",
                    showConfirmButton: false,
                    timer: 1500
                });
            }
        })
    });

    const confirmarComprar = () => {

        Swal.fire({
            title: '¿Desea continuar con el registro?',
            inputAttributes: {
                autocapitalize: 'off'
            },
            showCancelButton: true,
            confirmButtonText: 'Registrar',
            showLoaderOnConfirm: true,
            preConfirm: async () => {
                console.log(window.origin);
                return await fetch(`${window.origin}/registrar`, {
                    method: 'POST',
                    mode: 'same-origin',
                    credentials: 'same-origin',
                    headers: {
                        'Content-Type': 'application/json',
                        // 'X-CSRF-TOKEN': csrf_token
                    },
                    body: JSON.stringify({
                        'nombre' : nombre,
                        'apellido' : apellido,
                        'usuario' : usuario,
                        'password' : password,
                        'correo' : correo,
                        'domicilio' : domicilio,
                        'telefono' : telefono
                    })
                }).then(response => {
                    if (!response.ok) {
                        notificacionSwal('Error', response.statusText, 'error', 'Cerrar');
                    }
                    return response.json();

                }).then(data => {
                    if (data.exito) {
                        Swal.fire({
                            position: "Center",
                            titleText: '¡Éxito!',
                            icon: "success",
                            title: "Usuario registrado exitosamente",
                            showConfirmButton: '¡Ok!',
                            timer: 1500
                            
                        }).then((result) => {
                            if (result.dismiss === Swal.DismissReason.timer) {
                                window.location.href = '/registroExitoso';
                            } else if (result.isConfirmed) {
                                window.location.href = '/registroExitoso';
                            }
                        });
                        
                    } else {
                        notificacionSwal('¡Alerta!', data.mensaje, 'warning', 'Ok');
                    }
                }).catch(error => {
                    notificacionSwal('Error', error, 'error', 'Cerrar');
                });
            },
            allowOutsideClick: () => false,
            allowEscapeKey: () => false
        });
    };
})();