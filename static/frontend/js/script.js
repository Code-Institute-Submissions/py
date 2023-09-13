$(document).ready(function () {
    $('#sort-selector').on('change', function () {
        var selectedValue = $(this).val();

        if (selectedValue != 'reset') {
            var parts = selectedValue.split('_');
            var domain = parts[0];
            var sort = parts[1];
            var direction = parts[2];

            // URL Construction
            var url = domain + "?sort=" + sort + "&direction=" + direction;

            // Redirection to the constructed URL
            window.location.href = url;
        }
    });
});