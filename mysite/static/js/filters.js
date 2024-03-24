$(document).ready(function() {
    $('.product-list-main-filters-checkbox').change(function() {
        var all_filters = []
        $('.product-list-main-filters-checkbox:checked').each(function() {
            all_filters[$(this).attr('name')] = $(this).val();
        });

        console.log(all_filters);

        $.ajax({
            url: '/catalog/dynamic-filters/',  // URL представления для фильтрации
            type: 'GET',
            data: all_filters,
            success: function(response) {
                // Обновляем содержимое страницы с помощью полученных данных
                var productsHtml = '';
                response.products.forEach(function(product) {
                    productsHtml += `
                        <div class="product-list-main-row-products-grid-item">
                            <a href="${product.absolute_url}">
                                <img class="product-list-main-row-products-grid-item-img" src="${product.icon_image_url}" alt="Logo">
                                <a class="product-list-main-row-products-grid-item-name" href="${product.absolute_url}">${product.name}</a>
                                <p class="product-list-main-row-products-grid-item-price">${product.price} ₽</p>
                                <a class="product-list-main-row-products-grid-item-btn" href="#">В корзину</a>
                            </a>
                        </div>
                    `;
                });
                $('.product-list-main-row-products-grid').html(productsHtml);
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });
});