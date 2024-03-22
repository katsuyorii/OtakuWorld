$(document).ready(function() {
    $('a[id="forever"]').click(function(event) {
        event.preventDefault(); // Предотвращаем переход по ссылке по умолчанию

        var link = $(this); // Получаем ссылку, по которой был выполнен клик

        $.ajax({
            url: link.attr('href'), // URL для добавления в избранное, взятый из атрибута href ссылки
            type: 'GET', // Метод запроса GET, так как мы просто добавляем в избранное
            success: function(response) {
                // Когда запрос успешно выполнен, меняем цвет текста ссылки и заменяем изображение
                link.css('color', response.button_color); // Изменяем цвет текста ссылки на красный
                link.text(response.button_text)
                $('#forever_id').attr('src', response.new_img);
            },
            error: function(xhr, errmsg, err) {
                // Обработка ошибок, если что-то пошло не так
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });
});
