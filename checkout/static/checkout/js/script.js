$(document).ready(function () {
    // Use jQuery to select the collapse elements
    let firstCollapse = $('#multiCollapseExample1');
    let secondCollapse = $('#multiCollapseExample2');
    let thirdCollapse = $('#multiCollapseExample3');

    // Use jQuery to select the toggle buttons
    let toggleFirstButton = $('#toggleFirst');
    let toggleSecondButton = $('#toggleSecond');
    let toggleThirdButton = $('#toggleThird');

    function toggleCollapseWithoutTransition(collapseElement) {
        collapseElement.removeClass('show');
    }

    // Add an event listener to the first toggle button
    $(toggleFirstButton).on('click', function () {
        if (secondCollapse.hasClass('show')) {
            toggleCollapseWithoutTransition(secondCollapse);

        }
        if (thirdCollapse.hasClass('show')) {
            toggleCollapseWithoutTransition(thirdCollapse);
        }
    });

    // Add an event listener to the second toggle button
    $(toggleSecondButton).on('click', function () {
        if (firstCollapse.hasClass('show')) {
            toggleCollapseWithoutTransition(firstCollapse);
        }
        if (thirdCollapse.hasClass('show')) {
            toggleCollapseWithoutTransition(thirdCollapse);
        }
    });

    // Add an event listener to the third toggle button
    $(toggleThirdButton).on('click', function () {
        if (firstCollapse.hasClass('show')) {
            toggleCollapseWithoutTransition(firstCollapse);
        }
        if (secondCollapse.hasClass('show')) {
            toggleCollapseWithoutTransition(secondCollapse);
        }
    });

    // Repopulate the ACTION & METHOD attributes
    let manualdUrl = "/checkout/stripe/form/";
    let stripeUrl = "/checkout/stripe/";
    let cryptodUrl = "/checkout/stripe/form/";

    let paymentForm = $('#payment-form')
    $('#submit-button-1').on('click', function () {
        paymentForm.attr({
            'action': manualdUrl,
            'method': 'POST'
        });
    })
    $('#submit-button-2').on('click', function () {
        paymentForm.attr({
            'action': stripeUrl,
            'method': 'GET'
        });
    })
    $('#submit-button-3').on('click', function () {
        paymentForm.attr({
            'action': cryptodUrl,
            'method': 'POST'
        });
    })
});