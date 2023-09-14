$(document).ready(function () {
    // BUTTON to scroll up
    $('.btn-scroll').click(function (e) {
        window.scrollTo(0, 0)
    });

    // SORTING on a dedicated page
    $('#sort-selector').on('change', function () {
        let selectedValue = $(this).val();

        if (selectedValue != 'reset') {
            let parts = selectedValue.split('_');
            let domain = parts[0];
            let sort = parts[1];
            let direction = parts[2];

            // URL Construction
            let url = domain + "?sort=" + sort + "&direction=" + direction;

            // Redirection to the constructed URL
            window.location.href = url;
        }
    });

    // SORTING on the same page
    function rearrangeItems() {
        let selectedOption = $('#sort-selector-product').val();
        let itemElements = [];

        $('.item').each(function () {
            let $item = $(this);
            let priceContent = parseFloat($item.find('.price').html());
            let likesCount = parseFloat($item.find('.likes').html());
            let transactionsCount = parseFloat($item.find('.transactions').html());
            let titleContent = $item.find('.title').html();

            itemElements.push({
                element: $item,
                price: priceContent,
                likes: likesCount,
                transactions: transactionsCount,
                title: titleContent
            });
        });

        // Sorting arrow functions as per selected option
        const sortingFunctions = {
            'price_asc': (a, b) => a.price - b.price,
            'price_desc': (a, b) => b.price - a.price,

            'likes_asc': (a, b) => a.likes - b.likes,
            'likes_desc': (a, b) => b.likes - a.likes,

            'transactions_asc': (a, b) => a.transactions - b.transactions,
            'transactions_desc': (a, b) => b.transactions - a.transactions,

            'title_asc': (a, b) => a.title.localeCompare(b.title),
            'title_desc': (a, b) => b.title.localeCompare(a.title),
        };

        if (selectedOption in sortingFunctions) {
            itemElements.sort(sortingFunctions[selectedOption]);

            for (let i = 0; i < itemElements.length; i++) {
                $('#item-container').append(itemElements[i].element);
            }

        } else {
            let currentUrl = new URL(window.location);
            window.location.replace(currentUrl);
        }
    }

    // CALL the rearrangeItems function when the selector changes
    $('#sort-selector-product').on('change', rearrangeItems);

});