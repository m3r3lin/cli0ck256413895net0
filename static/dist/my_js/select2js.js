
$(document).ready(function () {
    $('.select_2_generator').select2({
        dir: "rtl",
        ajax: {
            url: window.select2_maintainer_url,
            data: function (params) {
                console.log($(this).attr('data-filters').replace("search_term", params.term ? params.term : ''));
                // Query parameters will be ?search=[term]&page=[page]
                return {
                    app: $(this).attr('data-app'),
                    table: $(this).attr('data-table'),
                    filters: $(this).attr('data-filters').replace("search_term", params.term ? params.term : ""),
                    settings: $(this).attr('data-settings'),
                    page: params.page || 1
                };
            }
        }
    });
    $('.select_2_generator_with_tags').select2({
        dir: "rtl",
        tags: true,
        ajax: {
            url: window.select2_maintainer_url,
            data: function (params) {
                console.log($(this).attr('data-filters').replace("search_term", params.term ? params.term : ''));
                // Query parameters will be ?search=[term]&page=[page]
                return {
                    app: $(this).attr('data-app'),
                    table: $(this).attr('data-table'),
                    filters: $(this).attr('data-filters').replace("search_term", params.term ? params.term : ""),
                    settings: $(this).attr('data-settings'),
                    page: params.page || 1
                };
            }
        }
    });
});