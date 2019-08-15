window.data_table_cool_options = {
    columnDefs: [
        {className: "text-center", targets: "_all"},
    ],
    "aaSorting": [],
    'paging': true,
    'lengthChange': true,
    'searching': true,
    'ordering': true,
    'info': true,
    'autoWidth': false,
    'responsive': true,
    'oLanguage': {
        "sSearch": "جستجو: ",
        "sLengthMenu": "نمایش _MENU_ مورد",
        "sInfo": "نمایش _START_ تا _END_ از _TOTAL_ مورد",
        "oPaginate": {
            "sFirst": "صفحه اول", // This is the link to the first page
            "sPrevious": "قبلی", // This is the link to the previous page
            "sNext": "بعدی", // This is the link to the next page
            "sLast": "صفحه آخر", // This is the link to the last page
        },
        "sEmptyTable": "اطلاعاتی در جدول شما ثبت نشده است.",
        "sInfoEmpty": "اطلاعات یافت نشد.",
        "sZeroRecords": "اطلاعاتی برای نمایش وجود ندارد.",
        "sInfoFiltered": " - فیلتر اطلاعات از  _MAX_ رکورد",
        sProcessing: ''
    }
};
var raw_data_table_cool_options = JSON.parse(JSON.stringify(window.data_table_cool_options));
window.getId = function (oTable, ele) {
    return oTable.row(ele.closest('tr')).data()[0]
};

window.datatable_connect_to_webservice = function (options) {
    window.data_table_cool_options["processing"] = true;
    window.data_table_cool_options["serverSide"] = true;
    // url which we get table's data from
    window.data_table_cool_options["ajax"] = {
        url: options['address'],
        data: options['extra_fields']
    };
    // add a column to overall columns so we can have delete and edit buttons
    window.data_table_cool_options["columns"] = [];
    for (var i = 0; i < options['real_fields']; i++)
        window.data_table_cool_options["columns"].append(null);
    window.data_table_cool_options["columns"] = [
        // this is a column which we add
        {
            data: null,
            className: "text-center",
            defaultContent: '<a href="" class="btn btn-primary select_button"><b>انتخاب</b></a>'
        }
    ];
    // hide id column
    window.data_table_cool_options["columnDefs"] = [
        {
            "targets": [0],
            "visible": false,
            "searchable": false
        }
    ];
    window.data_table_cool_options["responsive"] = true;
    // create datatable
    window.oTable = $('#Datatable').DataTable(window.data_table_cool_options);


    // a returns data of column
    function getData(oTable, ele) {
        return oTable.row(ele.closest('tr')).data();
    }

    // a returns id of a column
    function getId(oTable, ele) {
        return getData(oTable, ele)[0]
    }

    // on redraw re listen to delete and edit buttons
    oTable.on('draw.dt', function () {

        $('.select_button').on('click', function (e) {
            e.preventDefault();
            var data = getData($(this));
            $('#user_code_melli').val(data[1]);
            $('#id_number_finder_model').modal('toggle');
        });
        $("#Datatable tr").dblclick(function () {
            var data = oTable.row($(this)).data();
            $('#user_code_melli').val(data[1]);
            $('#id_number_finder_model').modal('toggle');
        });
    });

    $('#user_code_melli').dblclick(function () {
        $('#id_number_finder_model').modal('show');
        if ($(this).val().length > 3) {
            $("#filter_id_number").val($(this).val())
        }
        oTable.draw();
        $(".filter_field").keyup(function (e) {
            k = e.keyCode;
            if (k !== 17 || k !== 9)
                oTable.draw();
        });
    });
};

window.datatable_simple_show = function (options) {
    window.data_table_cool_options["processing"] = true;
    window.data_table_cool_options["serverSide"] = true;
    // url which we get table's data from
    if (options['extra_filters']) {
        window.data_table_cool_options["ajax"] = {
            url: options['url'],
            data: function (d) {
                options['extra_filters'](d);
                console.log(d);
            }
        };
    } else
        window.data_table_cool_options["ajax"] = options['url'];
    // add a column to overall columns so we can have delete and edit buttons
    window.data_table_cool_options["columns"] = [];
    do_not_order = options["do_not_order"] ? options["do_not_order"] : [];
    for (var i = 0; i < options['real_cols']; i++) {
        defaulta = {
            className: "text-center",
        };
        if (options['this_column_data']) {
            options['this_column_data'](i, defaulta);
        }
        if (do_not_order.includes(i)) {
            defaulta['orderable'] = false;
        }
        window.data_table_cool_options["columns"].push(defaulta);
    }
    extra_buttons = options["ex_buttons"] ? options["ex_buttons"] : "";
    delete_text = options['delete_text'] ? options['delete_text'] : "حذف";
    edit_text = options['edit_text'] ? options['edit_text'] : "ویرایش";
    if (!options["no_action_nutton"]) {
        buttons = '';
        if (options["icon_edit"]) {
            buttons += '<a href="" class="btn edit_button" ><i class="fas fa-edit"></i></a> ';
        } else if (!options["not_edit_able"]) {
            buttons += '<a href="" class="btn btn-primary edit_button"><b>' + edit_text + '</b></a> ';
        }
        if (options["icon_delete"]) {
            buttons += '<a href="" class="btn delete_button" ><i class="fas fa-trash-alt"></i></a> ';

        } else if (!options["not_delete_able"]) {
            buttons += '<a href="" class="btn btn-danger delete_button"><b>' + delete_text + '</b></a>';
        }
        window.data_table_cool_options["columns"].push(
            {
                data: null,
                className: "text-center",
                orderable: false,
                defaultContent: extra_buttons + buttons
            });
    }
    // hide id columnRadeNezami
    if (!window.data_table_cool_options["columnDefs"])
        window.data_table_cool_options["columnDefs"] = [];

    if (options['hide_id']) {
        window.data_table_cool_options["columnDefs"].push({
            "targets": [0],
            "visible": false,
            "searchable": false
        });
    }
    if (options['responsive']) {
    }
    // window.data_table_cool_options["scrollX"] = true;
    // window.data_table_cool_options["responsive"] = true;
    // create datatable
    var oTable = $(options['datable_id']).DataTable(window.data_table_cool_options);
    // a returns id of a column
    if (!options["no_action_nutton"]) {
        if (!options["not_edit_able"]) {
            // parse urls for deleting and editing
            var update_url = options['up_url'];
            var delete_url = options['del_url'];
            delete_url = delete_url.substr(0, delete_url.length - 1);
            update_url = update_url.substr(0, update_url.length - 1);
        }
        if (!options["not_delete_able"]) {
            var update_url = options['up_url'];
            var delete_url = options['del_url'];
            delete_url = delete_url.substr(0, delete_url.length - 1);
            update_url = update_url.substr(0, update_url.length - 1);
        }
    }

    function ref_applier(url) {
        var ref = options['ref'];
        if (ref) {
            if (url.search('\\?') > -1) {
                url += '&ref=' + ref;
            } else {
                url += '?ref=' + ref;
            }
        }
        return url
    }

    // on redraw re listen to delete and edit buttons
    oTable.on('draw.dt', function () {
        // edit button
        $(options['datable_id'] + " " + '.edit_button').on('click', function (e) {
            e.preventDefault();
            var id = getId(oTable, $(this));
            window.location.href = ref_applier(update_url + id);
        });
        // delete button
        if (options['do_before_initializing']) {
            options['do_before_initializing'](oTable);
        }
        $('.dataTables_filter').parent().parent().addClass('modal-header').css({"margin-left": "0px", "margin-right": "0px"});
        $('.dataTables_filter input')
            .css('color', '#2d2d2d').css('font-size', '16px').parent().parent().parent().removeClass('col-sm-6').addClass('col-sm-12 col-lg-6')
            .siblings().removeClass('col-sm-6').addClass('col-sm-12 col-lg-6');
        $(options['datable_id'] + " " + '.delete_button').on('click', function (e) {
            e.preventDefault();
            var id = getId(oTable, $(this));
            $(options["modal_id"]).modal('show');
            $(options['modal_id'] + " " + '.yes_button').click(function () {
                $(options["modal_id"]).modal('toggle');
                window.location.href = ref_applier(delete_url + id);
            });
        });
        if (options['do_after_initializing']) {
            options['do_after_initializing'](oTable);
        }
    });
    return {
        table: oTable,
        getData: function (ele) {
            return this.table.row(ele.closest('tr')).data()
        },
        getId: function (ele) {
            return this.getData(ele)[0]
        }
    };
};

$(function () {
    $('#example2').DataTable({
        columnDefs: [
            {className: "text-center", targets: "_all"},
        ],
        // 'order': [[ 3, "desc" ]]
        "aaSorting": [],
        'paging': true,
        'lengthChange': true,
        'searching': true,
        'ordering': true,
        'info': true,
        'autoWidth': false,
        'responsive': true,
        'oLanguage': {
            "sSearch": "جستجو: ",
            "sLengthMenu": "نمایش _MENU_ مورد",
            "sInfo": "نمایش _START_ تا _END_ از _TOTAL_ مورد",
            "oPaginate": {
                "sFirst": "صفحه اول", // This is the link to the first page
                "sPrevious": "قبلی", // This is the link to the previous page
                "sNext": "بعدی", // This is the link to the next page
                "sLast": "صفحه آخر", // This is the link to the last page
            },
            "sEmptyTable": "اطلاعاتی در جدول شما ثبت نشده است.",
            "sInfoEmpty": "اطلاعات یافت نشد.",
            "sZeroRecords": "اطلاعاتی برای نمایش وجود ندارد.",
            "sInfoFiltered": " - فیلتر اطلاعات از  _MAX_ رکورد"
        },

    });
    if ($('#example3').length > 0) {

        $('#example3').DataTable({
            columnDefs: [
                {className: "text-center", targets: "_all"},
            ],
            // 'order': [[ 3, "desc" ]]
            "aaSorting": [],
            'paging': true,
            'lengthChange': true,
            'searching': true,
            'ordering': true,
            'info': true,
            'autoWidth': false,
            'responsive': true,
            'oLanguage': {
                "sSearch": "جستجو: ",
                "sLengthMenu": "نمایش _MENU_ مورد",
                "sInfo": "نمایش _START_ تا _END_ از _TOTAL_ مورد",
                "oPaginate": {
                    "sFirst": "صفحه اول", // This is the link to the first page
                    "sPrevious": "قبلی", // This is the link to the previous page
                    "sNext": "بعدی", // This is the link to the next page
                    "sLast": "صفحه آخر", // This is the link to the last page
                },
                "sEmptyTable": "اطلاعاتی در جدول شما ثبت نشده است.",
                "sInfoEmpty": "اطلاعات یافت نشد.",
                "sZeroRecords": "اطلاعاتی برای نمایش وجود ندارد.",
                "sInfoFiltered": " - فیلتر اطلاعات از  _MAX_ رکورد"
            },

        })

    }
});

window.soldier_finder = function (options) {
    console.log(options);
    // ----------------------- DATATABLE --------------------------------
    var some_cool_options = JSON.parse(JSON.stringify(raw_data_table_cool_options));
    some_cool_options["processing"] = true;
    some_cool_options["serverSide"] = true;
    some_cool_options['searching'] = false;
    // url which we get table's data from
    some_cool_options["ajax"] = {
        url: options['data_table_address'],
        data: function (d) {
            d.id_number = $(options['modal_id'] + " .filter_id_number").val();
            d.first_name = $(options['modal_id'] + " .filter_first_name").val();
            d.last_name = $(options['modal_id'] + " .filter_last_name").val();
            if (options['extra_filters']) {
                options['extra_filters'](d);
            }
            console.log(d);
        }
    };
    var select_text = options['select_text'] ? options['select_text'] : "انتخاب";
    var select_class = options['select_class'] ? options['select_class'] : "select_button";
    var extra_buttons = options['extra_buttons'] ? options['extra_buttons'] : function () {
        return "";
    };
    // add a column to overall columns so we can have delete and edit buttons
    some_cool_options["columns"] = [
        // set null for real columns
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        // this is a column which we add
        {
            data: null,
            className: "center",
            defaultContent: '<a href="" class="btn btn-primary ' + select_class + '"><b>' + select_text + '</b></a>' + extra_buttons()
        }
    ];
    // hide id column
    some_cool_options["columnDefs"] = [
        {
            "targets": [0],
            "visible": false,
            "searchable": false
        }
    ];
    // create datatable
    var oTable = $(options['table_id']).DataTable(some_cool_options);

    // a returns data of column
    function getData(ele) {
        return oTable.row(ele.closest('tr')).data()
    }

    // a returns id of a column
    function getId(ele) {
        return getData(ele)[0]
    }

    // on redraw re listen to delete and edit buttons
    oTable.on('draw.dt', function () {
        if (options["on_table_draw"]) {
            options["on_table_draw"](oTable, options);
        }

        if (options['modal_title']) {
            $(options['modal_id'] + ' .modal-title').text(options['modal_title']());
        }

        $(options['modal_id'] + ' .select_button').on('click', function (e) {
            e.preventDefault();
            var data = getData($(this));
            if (options['on_select_clicked']) {
                options['on_select_clicked']($(this), getData($(this)), data);
            }
            if (options['set_value']) {
                $('input[name="soldier"]').val(data[0]);
                $(options['element_to_open']).val(data[1]);
            }
            $(options['modal_id']).modal('toggle');
        });
        $(options['table_id'] + ' tr').dblclick(function () {
            var data = oTable.row($(this)).data();
            if (options['on_select_clicked']) {
                options['on_select_clicked']($(this), oTable.row($(this)), data);
            }
            if (options['set_value']) {
                $('input[name="soldier"]').val(data[0]);
                $(options['element_to_open']).val(data[1]);
            }
            $(options['modal_id']).modal('toggle');
        });
    });

    if (!options["disable_dbl"]) {
        $(options['element_to_open']).dblclick(function () {
            $(options['modal_id']).modal('show');
            if (options['set_value']) {
                if ($(this).val().length > 3) {
                    $(options['modal_id'] + " .filter_id_number").val($(this).val().substr(0, 10))
                }
                oTable.draw();
            }
        });
    }
    $(options["modal_id"]).on('show.bs.modal', function () {
        $(options["modal_id"] + " .filter_field").keyup(function (e) {
            k = e.keyCode;
            if (k !== 17 || k !== 9)
                oTable.draw();
        });
    });
    return {
        data_table: oTable,
        modal: $(options['modal_id']),
    };
};
window.object_finder = function (options) {
    console.log(options);
    // ----------------------- DATATABLE --------------------------------
    var some_cool_options = JSON.parse(JSON.stringify(raw_data_table_cool_options));
    some_cool_options["processing"] = true;
    some_cool_options["serverSide"] = true;
    some_cool_options['searching'] = false;
    // url which we get table's data from
    some_cool_options["ajax"] = {
        url: options['data_table_address'],
        data: function (d) {
            if (options['extra_filters']) {
                options['extra_filters'](d);
            }
        }
    };
    var select_text = options['select_text'] ? options['select_text'] : "انتخاب";
    var select_class = options['select_class'] ? options['select_class'] : "select_button";
    // add a column to overall columns so we can have delete and edit buttons
    some_cool_options["columns"] = [];
    var real_cols = options["real_cols"] ? options["real_cols"] : 0;
    for (var i = 0; i < real_cols; i++) {
        var changer = null;
        if (options['real_cols_fallback']) {
            changer = options['real_cols_fallback']();
        }
        if (changer === undefined) {
            changer = null;
        }
    }
    some_cool_options["columns"].push(
        // set null for real columns
        // this is a column which we add
        {
            data: null,
            className: "center",
            defaultContent: '<a href="" class="btn btn-primary ' + select_class + '"><b>' + select_text + '</b></a>'
        }
    );
    // hide id column
    some_cool_options["columnDefs"] = [
        {
            "targets": [0],
            "visible": false,
            "searchable": false
        }
    ];
    // create datatable
    var oTable = $(options['table_id']).DataTable(some_cool_options);

    // a returns data of column
    function getData(ele) {
        return oTable.row(ele.closest('tr')).data()
    }

    // a returns id of a column
    function getId(ele) {
        return getData(ele)[0]
    }

    // on redraw re listen to delete and edit buttons
    oTable.on('draw.dt', function () {
        $(options['modal_id'] + ' .select_button').on('click', function (e) {
            e.preventDefault();
            var data = getData($(this));
            if (options['on_select_clicked']) {
                options['on_select_clicked']($(this), getData($(this)), data);
            }
            if (options['set_value']) {
                $('input[name="soldier"]').val(data[0]);
                $(options['element_to_open']).val(data[1]);
            }
            $(options['modal_id']).modal('toggle');
        });
        $(options['table_id'] + ' tr').dblclick(function () {
            var data = oTable.row($(this)).data();
            if (options['on_select_clicked']) {
                options['on_select_clicked']($(this), oTable.row($(this)), data);
            }
            if (options['set_value']) {
                $('input[name="soldier"]').val(data[0]);
                $(options['element_to_open']).val(data[1]);
            }
            $(options['modal_id']).modal('toggle');
        });
    });

    if (options['set_value']) {
        $(options['element_to_open']).dblclick(function () {
            $(options['modal_id']).modal('show');
            if ($(this).val().length > 3) {
                $(options['modal_id'] + " .filter_id_number").val($(this).val())
            }
            oTable.draw();
            $(".filter_field").keyup(function (e) {
                k = e.keyCode;
                if (k !== 17 || k !== 9)
                    oTable.draw();
            });
        });
    }
    return {
        data_table: oTable,
        modal: $(options['modal_id']),
    };
};

function ConvertNumberToPersion(text) {
    persian = {0: '۰', 1: '۱', 2: '۲', 3: '۳', 4: '۴', 5: '۵', 6: '۶', 7: '۷', 8: '۸', 9: '۹'};
    var replaced = "";
    for (var index in text) {
        var found = false;
        for (var per_s in persian) {
            if (text[index] === "/") {
                replaced += "/";
                found = true;
                break;
            } else if (persian[per_s] === text[index]) {
                replaced += per_s;
                found = true;
                break;
            }
        }
        if (!found) {
            return "bad";
        }
    }

    return replaced;
}

function show_error(text) {
    var element = $('<h5 class="text-danger alert alert-danger alert-dismissible"><button type="button" class="close pull-left" data-dismiss="alert" aria-hidden="true">×</button><ul class="errorlist"><li>' + text + '</li></ul></h5>');
    $('#filter_form').prepend(element);
    setInterval(function () {
        element.remove();
    }, 6000);
}

function check_for_numeric(numeric, errors) {
    for (var numeric_field in numeric) {
        var field = numeric[numeric_field];
        var value = field.val();
        if (value !== undefined && value !== "") {
            if (isNaN(value)) {
                show_error("فیلد " + $('label[for="' + field.attr('id') + '"]').text().replace(':', '') + " باید عددی باشد");
                errors++;
            } else {
                if (Number(value) < 0) {
                    show_error("فیلد " + $('label[for="' + field.attr('id') + '"]').text().replace(':', '') + " باید عددی بزرگتر از 0 باشد");
                    errors++;
                }
            }
        }
    }
    return errors;
}

function check_date_(dates, errors) {
    var regex = /\d\d\d\d\/\d\d\/\d{1,2}/;
    for (var date_field in dates) {
        var field = dates[date_field];
        var value = field.val();
        if (value !== undefined && value !== "") {
            console.log(value);
            value = ConvertNumberToPersion(value);
            console.log(value, value === "bad", regex.test(value));
            if (value === "bad" || !regex.test(value)) {
                show_error("در فیلد " + $('label[for="' + field.attr('id') + '"]').text().replace(':', '') + " فرمت تاریخ اشتباه است");
                errors++;
            }
        }
    }
    return errors;
}

