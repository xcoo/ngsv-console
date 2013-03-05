var ngsvConsole = ngsvConsole || {};
ngsvConsole.manager = ngsvConsole.manager || {};

(function() {

    ngsvConsole.manager.main = function() {
        $('#new-tag-btn').click(ngsvConsole.manager.addTag);

        $('.old-tag').each(function() {
            var tagId = $(this).attr('data-tag-id');

            var samFileNames = tags[tagId].samFileNames;
            $(this).find('select[name="sam"] > option').each(function() {
                if ($.inArray($(this).val(), samFileNames) != -1) {
                    $(this).attr('selected', 'selected');
                }
            });

            var bedFileNames = tags[tagId].bedFileNames;
            $(this).find('select[name="bed"] > option').each(function() {
                if ($.inArray($(this).val(), bedFileNames) != -1) {
                    $(this).attr('selected', 'selected');
                }
            });
        });

        $('.chzn-select').chosen();
        $('.chzn-select-deselect').chosen({allow_single_deselect: true});
    };

    ngsvConsole.manager.addTag = function() {
        if ($('#new-tag > div').size() > 0) return;

        var $newTag = $('#new-tag-tmpl').tmpl();

        $newTag.find('button.close').click(function() {
            $newTag.fadeOut(200, function() { $(this).remove(); });
        });

        $newTag.appendTo('#new-tag').hide().fadeIn(200);

        $newTag.find('.chzn-select').chosen();
    };
})();

$(document).ready(ngsvConsole.manager.main);
