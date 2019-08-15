function fallbackCopyTextToClipboard(text) {
    var textArea = document.createElement("textarea");
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
        var successful = document.execCommand('copy');
        var msg = successful ? 'successful' : 'unsuccessful';
    } catch (err) {
        console.error('Fallback: Oops, unable to copy', err);
    }

    document.body.removeChild(textArea);
}

function copyTextToClipboard(text) {
    if (!navigator.clipboard) {
        fallbackCopyTextToClipboard(text);
        return;
    }
    navigator.clipboard.writeText(text).then(function () {
    }, function (err) {
        console.error('Async: Could not copy text: ', err);
    });
}

$(document).ready(function () {
    $('.copy_link').click(function (e) {
        e.preventDefault();
        link = window.location.protocol + '//' + window.location.host + $(this).attr('href');
        copyTextToClipboard(link);
    });
    $('.publish_tabligh').click(function () {
        $('#confirm_modal').modal('toggle');
        var url = window.where_to_publish + $(this).attr('data-data');
        if (location.pathname.search('dashboard') >= 0) {
            url += '?ref=dashboard'
        }
        $('.yes_button').attr('href', url);
        console.log(window.where_to_publish);
    })
});