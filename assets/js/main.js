function initJournal() {
    var indicator = $('#ajax-progress-indicator');
    var show_errors = $('#ajax-request-errors');

    $('.day-box input[type="checkbox"]').click(function (event) {
        var box = $(this);
        $.ajax(box.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'pk': box.data('student-id'),
                'date': box.data('date'),
                'present': box.is(':checked') ? '1' : '',
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'beforeSend': function (xhr, settings) {
                indicator.show();
            },
            'error': function (xhr, status, error) {
                indicator.hide();
                show_errors.show();
                show_errors.html(error);
                setTimeout(function () {

                    show_errors.hide();


                }, 2000);

            },
            'success': function (data, status, xhr) {
                indicator.hide();
            }
        })
    })
}

function initGroupSelector() {
    // look up select element with groups and attach our even handler
    // on find change event
    $('#group-selector select').change(function (event) {
        var group = $(this).val();

        if (group) {
            // set cookie with expiration date q year since now
            // cookie creation function takes period in days
            $.cookie('current_group', group, {'path': '/', 'expires': 365});
        } else {
            // otherwise we delete the cookie
            $.removeCookie('current_group', {'path': '/'});
        }

        // and reload a page
        location.reload(true);

        return true;

    })
}

function initDateFields() {

    $('input.dateinput').datetimepicker({
        'format': 'YYYY-MM-DD'

    }).on('dp.hide', function (event) {
        $(this).blur();

    });

}

function orderByStudents() {

    $('a.order_by_students').click(function (event) {

        var url_address = $(this);

        $.ajax({
            'url': url_address.attr('href'),
            'dataType': 'html',
            'type': 'get',
            'success': function (data, status, xhr) {

                var html = $(data);
                var body = html.find('#content-column');

                $('#content-columns').html(body);

                $(function () {
                    initEditStudentPage();
                    orderByStudents();
                    initPaginate();

                });

            }

        });

        return false;

    });
}

function initPaginate() {
    $('a.paginate_by').click(function (event) {

        var paginate_url = $(this).attr('href');
        var current_page_url = $('table').attr('data-url');
        $.ajax({
            'url': current_page_url + paginate_url,
            'dataType': 'html',
            'type': 'get',
            'success': function (data) {
                var html = $(data);
                var body = html.find('table');
                $('table').html(body);

                $(function () {
                    initEditStudentPage();
                    orderByStudents();
                });

            }

        });

        return false

    });

}

function initPhotoPreview() {

    var block_preview = $('#image-preview');

    block_preview.hide();

    $('#id_photo').change(function (e) {

        block_preview.show();
        if (this.files && this.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#preview').attr('src', e.target.result);
            };

            reader.readAsDataURL(this.files[0]);
        }

    });
}

function initChangeLanguage() {

    $(".current-lang").click(function (event) {

        var lang = $(this).data('lang');

        $('#set_language').val(lang);

        $('#language-form').submit();
    });
}

$(document).ready(function () {
    initJournal();
    initGroupSelector();
    initDateFields();
    orderByStudents();
    initPhotoPreview();
    initChangeLanguage();
});

