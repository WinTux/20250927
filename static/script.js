$(document).ready(function () {
    $('#loginForm').on('submit', function (e) {
        e.preventDefault();

        const username = $('input[name="username"]').val();
        const password = $('input[name="password"]').val();

        $.ajax({
            url: '/login',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ username, password }),
            success: function (response) {
                if (response.success) {
                    window.location.href = '/chat';
                } else {
                    $('#mensaje').text(response.error);
                }
            },
            error: function () {
                $('#mensaje').text('Error en el servidor.');
            }
        });
    });
});
