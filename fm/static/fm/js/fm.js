;(function (jQuery) {
    jQuery.extend({
        fm: function (custom_options) {

            var defaults = {
                debug: false,
                create_button_selector: ".fm-create",
                update_button_selector: ".fm-update",
                delete_button_selector: ".fm-delete",
                modal_selector: '#fm-modal',
                modal_wrapper_selector: '.modal-wrapper',
                modal_head_selector: '.modal-head',
                modal_body_selector: '.modal-body',
                modal_buttons_selector: '.modal-buttons',
                modal_loader_selector: '.modal-loader',
                modal_load_error: "Error occurred while loading",
                delegate_target: 'body',
                trigger_event_name: 'fm.success',
                ready_event_name: 'fm.ready'
            };

            var global_options = jQuery.extend(defaults, custom_options);

            // using jQuery
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            function sameOrigin(url) {
                // test that a given url is a same-origin URL
                // url could be relative or scheme relative or absolute
                var host = document.location.host; // host + port
                var protocol = document.location.protocol;
                var sr_origin = '//' + host;
                var origin = protocol + sr_origin;
                // Allow absolute or scheme relative URLs to same origin
                return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                    (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                    // or any other URL that isn't scheme relative or absolute i.e relative.
                    !(/^(\/\/|http:|https:).*/.test(url));
            }

            $.ajaxPrefilter(function(options, originalOptions, jqXHR){
                var request_method = options['type'].toLowerCase();
                if ((request_method === "post" || request_method === "delete") && sameOrigin(options.url)) {
                    jqXHR.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
                }
            });

            var delegate_target = $(global_options.delegate_target);
            var modal = $(global_options.modal_selector);
            var modal_loader = $(global_options.modal_loader_selector);
            var modal_wrapper = $(global_options.modal_wrapper_selector);
            var modal_head = $(global_options.modal_head_selector);
            var modal_body = $(global_options.modal_body_selector);
            var modal_buttons = $(global_options.modal_buttons_selector);

            function debug(data) {
                if (global_options.debug === true) {
                    console.log(data);
                }
            }

            function load_content(options) {
                if (!options.url) {
                    debug("no URL found to load data from");
                    return;
                }
                modal_loader.show();
                $.ajax({
                    url: options.url,
                    type: "GET",
                    dataType: "html",
                    error: function () {
                        debug("error occurred while loading modal body from URL");
                        modal_body.text(global_options.modal_load_error);
                    },
                    success: function (data) {
                        debug("modal body successfully loaded");
                        modal_body.html(data);
                        show_modal_wrapper();
                        var form = modal.find('form');
                        form.on('submit', function () {
                            submit_form(form, options);
                            return false;
                        });
                        modal.trigger(global_options.ready_event_name);
                    }
                }).done(function(){
                    modal_head.html(options.modal_head);
                    modal_loader.hide();
                });
            }

            function clear_modal() {
                hide_modal_wrapper();
                modal_head.html('');
                modal_body.html('');
            }

            function show_modal(element, action) {
                debug("showing modal");
                var options = extract_modal_options(element, action);
                debug("options:");
                debug(options);
                modal.modal('show');
                modal_buttons.find('[type="submit"]').unbind('click').bind("click", function () {
                    var form = modal.find('form');
                    submit_form(form, options);
                });
                load_content(options);
            }

            function show_delete_modal(element) {
                debug("showing delete modal");
                var options = extract_modal_options(element, 'delete');
                debug(options);
                modal.modal('show');
                modal_head.html(options.modal_head);
                modal_wrapper.show();
                modal_buttons.find('[type="submit"]').unbind('click').bind("click", function () {
                    var url = options.url;
                    disable_modal_buttons();
                    $.ajax({
                        url: url,
                        type: 'DELETE',
                        dataType: "json",
                        success: function(data) {
                            debug(data);
                            process_response_data(data, options);
                        }
                    });
                });
            }

            function extract_modal_options(element, action) {
                return {
                    url: element.attr('href'),
                    action: action,
                    modal_head: element.attr('data-fm-head'),
                    modal_callback: element.attr('data-fm-callback'),
                    modal_target: element.attr('data-fm-target')
                };
            }

            function submit_form(form, options) {

                var params = {
                    url: options.url,
                    type: form.attr('method').toUpperCase(),
                    dataType: "json"
                };

                var data;
                if (!window.FormData) {
                    // for old browsers - do not support forms with file input fields.
                    data = form.serialize();
                } else {
                    data = new FormData(form[0]);
                    params['processData'] = false;
                    params['contentType'] = false;
                }
                params['data'] = data;
                disable_modal_buttons();
                $.ajax(params).success(function (data) {
                    process_response_data(data, options);
                }).error(function () {
                    enable_modal_buttons();
                    modal_body.text(global_options.modal_load_error);
                });
                return false;
            }

            function process_response_data(data, options) {
                if (data.status === 'ok') {
                    modal.modal("hide");
                    if (options.modal_callback === null || options.modal_callback === undefined) {
                        $.noop();
                    } else if (options.modal_callback === 'reload') {
                        window.location.reload();
                    } else if (options.modal_callback === 'redirect') {
                        window.location = options.modal_target;
                    } else if (options.modal_callback === 'remove' || options.modal_callback === 'delete') {
                        $(options.modal_target).remove();
                    } else if (options.modal_callback === 'append') {
                        $(options.modal_target).append(data.message);
                    } else if (options.modal_callback === 'prepend') {
                        $(options.modal_target).prepend(data.message);
                    } else if (options.modal_callback === 'replace') {
                        $(options.modal_target).replaceWith(data.message);
                    } else if (options.modal_callback === 'trigger') {
                        delegate_target.trigger(global_options.trigger_event_name, {
                            data: data,
                            options: options
                        });
                    } else {
                        debug("unknown action " + data.action);
                    }
                } else {
                    modal_body.html(data.message);
                    // Also reinstate bindings on submit buttons (in case a
                    // form is invalid, subsequent invalid submissions should
                    // keep the user on the form):
                    var form = modal.find('form');
                    form.on('submit', function () {
                            submit_form(form, options);
                            return false;
                    });
                    // and set event ready:
                    modal.trigger(global_options.ready_event_name);
                }
                enable_modal_buttons();
            }

            function hide_modal_wrapper() {
                modal_wrapper.hide();
            }

            function show_modal_wrapper() {
                modal_wrapper.show();
            }

            function disable_modal_buttons() {
                modal_buttons.find('[type="submit"]').attr('disabled', true);
            }

            function enable_modal_buttons() {
                modal_buttons.find('[type="submit"]').attr('disabled', false);
            }

            function init() {

                modal.on('hidden.bs.modal', function () {
                    debug("modal hidden event fired");
                    clear_modal();
                });

                delegate_target.on('click', global_options.create_button_selector, function () {
                    var self = $(this);
                    show_modal(self, 'create');
                    return false;
                });

                delegate_target.on('click', global_options.update_button_selector, function () {
                    var self = $(this);
                    show_modal(self, 'update');
                    return false;
                });

                delegate_target.on('click', global_options.delete_button_selector, function () {
                    var self = $(this);
                    show_delete_modal(self);
                    return false;
                });
            }

            return init();

        }
    });
})(jQuery);

