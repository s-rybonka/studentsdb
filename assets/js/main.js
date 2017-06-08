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


function initEditStudentPage() {

    $('a.student_edit_form_link').click(function (event) {
        var link = $(this);

        $.ajax({
            'url': link.attr('href'),
            'dataType': 'html',
            'type': 'get',
            'success': function (data, status, xhr) {
                // check if we got successfull response from the server
                if (status != 'success') {
                    alert('Error on  server');

                    return false;
                }

                // update modal window with arrived content from the server

                var modal = $('#myModal'),
                    html = $(data), form = html.find('#content-column form');
                modal.find('.modal-title').html(html.find('#content-column h2').text());
                modal.find('.modal-body').html(form);

                // init our edit form
                initEditStudentForm(form, modal);


                modal.show();
                // setup and show modal window finally
                modal.modal({
                    'show': true,
                    'keyboard': false,
                    'backdrop': false,
                });

                initHistoryBack(link.attr('href'));
                initPhotoPreview();
            },
            'error': function () {
                alert('Error on server try again later');
                return false;

            }
        });
        return false;

    });

}

function initEditStudentForm(form, modal) {

    // atach datepicker
    initDateFields();

    // close modal window on Cancel button click
    form.find('input[name="cancel_button"]').click(function (event) {
        modal.modal('hide');
        return false;
    });

    // make form work in ajax mode
    form.ajaxForm({
        'dataType': 'html',
        'error': function () {
            alert('Error on server');
            return false;

        },
        'success': function (data, status, xhr) {
            var html = $(data), newform = html.find('#content-column form');

            // copy alert to modal window
            modal.find('.modal-body').html(html.find('.alert'));

            // copy form to modal window if we found it in server response
            if (newform.length > 0) {
                modal.find('.modal-body').append(newform);

                // initialie form fields and buttons
                initEditStudentForm(newform, modal);

            } else {
                // if no form, it means success and we need to reload page
                // to get updated student list
                // reload after 2 seconds, so that user can read
                // success message
                setTimeout(function () {
                    window.history.pushState(null, null, '/');
                    location.reload(true);

                }, 1000)
            }

        }
    });

}


function initSitePages() {

    $('a.menu_item_url').click(function (event) {

        // get url address for all views with data
        var url = $(this);

        // remove active status from link by click
        $('.nav-tabs li').removeClass('active');

        // add class active for current button
        $(this).parent().addClass('active');

        // this ajax return html, that I have in template, Python views stay unchanged
        $.ajax({
            'url': url.attr('href'),
            'dataType': 'html',
            'type': 'get',
            'success': function (data, status, xhr) {


                var html = $(data);
                var body = html.find('#content-column');

                $(function () {
                    initEditStudentPage();
                    orderByStudents();
                    initJournal();
                    initPaginate();
                    initPhotoPreview();
                });

                $('#content-columns').html(body);

            }

        });

        return false
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


function initHistoryBack(url) {

    window.history.pushState('/', null, url);

    window.onpopstate = function (e) {

        $('.modal').hide();

    };

    return true;

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
    initEditStudentPage();
    initSitePages();
    orderByStudents();
    initPaginate();
    initPhotoPreview();
    initChangeLanguage();

});

