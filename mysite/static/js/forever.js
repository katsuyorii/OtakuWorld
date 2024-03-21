$(document).ready(function() {
    $('.product-detail-stars-forever-link').click(function(event) {
        event.preventDefault(); // Предотвращаем переход по ссылке по умолчанию

        var link = $(this); // Получаем ссылку, по которой был выполнен клик
    });
});
