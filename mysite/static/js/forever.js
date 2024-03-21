$(document).ready(function() {
    $('a[id="forever"]').click(function(event) {
        event.preventDefault(); // Предотвращаем переход по ссылке по умолчанию

        var link = $(this); // Получаем ссылку, по которой был выполнен клик

        $.ajax({
            url: link.attr('href'), // URL для добавления в избранное, взятый из атрибута href ссылки
            type: 'GET', // Метод запроса GET, так как мы просто добавляем в избранное
            success: function(response) {
                // Когда запрос успешно выполнен, меняем цвет текста ссылки и заменяем изображение
                link.css('color', 'red'); // Изменяем цвет текста ссылки на красный
                link.text('В избранном')
                $('#forever_id').attr('src', '/static/img/icons/heart-red.png');
            },
            error: function(xhr, errmsg, err) {
                // Обработка ошибок, если что-то пошло не так
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });
});
