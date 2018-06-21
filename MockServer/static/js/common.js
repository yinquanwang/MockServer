function post_project(url) {
    var data = {
        "name": $('#project_name').val(),
        'desc': $('#desc').val()
    };
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            response = JSON.parse(data);
            if (response.msg === 'success') {
                window.location.reload();
            } else {
                alert(data)
            }
        },
        error: function () {
            alert('可能是潜在的bug')
        }
    });
}

function post_mock(url) {
    var data = {
        "name": $('#api_name').val(),
        'project': $('#project').val(),
        'url': $('#url').val(),
        'method': $('#method').val()
    };
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            response = JSON.parse(data);
            if (response.msg === 'success') {
                window.location.reload();
            } else {
                alert(data)
            }
        },
        error: function () {
            alert('可能是潜在的bug')
        }
    });
}


function collapse_api(id) {

    var element = $(id);
    if (element.hasClass('collapse')) {
        element.removeClass('collapse');
        element.addClass('collapse.in')
    } else {
        element.removeClass('collapse.in');
        element.addClass('collapse')
    }

}

function init_acs(language, theme, editor) {
    editor.setTheme("ace/theme/" + theme);
    editor.session.setMode("ace/mode/" + language);
    editor.setFontSize(15);
    editor.setReadOnly(false);
    editor.setOption("wrap", "free");
    ace.require("ace/ext/language_tools");
    editor.setOptions({
        enableBasicAutocompletion: true,
        enableSnippets: true,
        enableLiveAutocompletion: true,
        autoScrollEditorIntoView: true
    });
}