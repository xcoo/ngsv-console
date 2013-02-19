var console = console || {};
console.manager = console.manager || {};

(function() {

    console.manager.main = function() {
        $('#new-tag-btn').click(console.manager.addTag);
    };

    console.manager.addTag = function() {
        if ($('#new-tag > div').size() > 0) return;

        var $template = $('#new-tag-template > div:first');
        $template.appendTo('#new-tag').hide().fadeIn(200);
    };
}());

$(document).ready(console.manager.main);
