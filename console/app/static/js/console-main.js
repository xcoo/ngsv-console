var ngsvConsole = ngsvConsole || {};
ngsvConsole.main = ngsvConsole.main || {};

(function() {

    ngsvConsole.main.main = function() {
        $('.tags').each(function() {
            var tagsId = $(this).attr('id');

            var tags = tagInfos[tagsId];
            $(this).find('select[name="tags"] > option').each(function() {
                if ($.inArray($(this).val(), tags) != -1) {
                    $(this).attr('selected', 'selected');
                }
            });
        });

        $('.chzn-select').chosen();
        $('.chzn-select-deselect').chosen({allow_single_deselect: true});
    };
})();

$(document).ready(ngsvConsole.main.main);
