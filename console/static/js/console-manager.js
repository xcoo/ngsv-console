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
        });

        $('.chzn-select').chosen();
        $('.chzn-select-deselect').chosen({allow_single_deselect: true});
    };

    ngsvConsole.manager.addTag = function() {
        if ($('#new-tag > div').size() > 0) return;
        var $newTag = $('#new-tag-tmpl').tmpl();
        $newTag.find('.add-sam').click(function() {
            var $selectSam = $('#select-sam-tmpl').tmpl();
            $selectSam.appendTo($newTag.find('.select-data')).hide().fadeIn(200);
            $selectSam.chosen();
        });
        $newTag.find('.add-bed').click(function() {
            var $selectBed = $('#select-bed-tmpl').tmpl();
            $selectBed.appendTo($newTag.find('.select-data')).hide().fadeIn(200);
            $selectBed.chosen();
        });
        $newTag.appendTo('#new-tag').hide().fadeIn(200);
    };
})();

$(document).ready(ngsvConsole.manager.main);
