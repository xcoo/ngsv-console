var console = console || {};
console.manager = console.manager || {};

(function() {

    console.manager.main = function() {
        $('#new-tag-btn').click(console.manager.addTag);
    };

    console.manager.addTag = function() {
        if ($('#new-tag > div').size() > 0) return;
        var $e = $('#new-tag-tmpl').tmpl();
        $e.find('.add-sam').click(function() {
            $('#select-sam-tmpl').tmpl().appendTo($e.find('.select-data')).hide().fadeIn(200);
        });
        $e.find('.add-bed').click(function() {
            $('#select-bed-tmpl').tmpl().appendTo($e.find('.select-data')).hide().fadeIn(200);
        });
        $e.appendTo('#new-tag').hide().fadeIn(200);
    };
}());

$(document).ready(console.manager.main);
