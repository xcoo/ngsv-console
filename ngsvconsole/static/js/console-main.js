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

        ngsvConsole.main.setupTopRow();
    };

    ngsvConsole.main.setupTopRow = function() {
        $('#top-row').find('div').each(function() {
            var dataSort = $(this).attr('data-sort');

            if (dataSort == sort) {
                var $icon = $('<i class="icon-chevron-down"></i>');
                $(this).append($icon);

                var href = $.format('/?sort=%s&desc=%s', sort, !desc);
                $(this).click(function() {
                    location.href = href;
                });
            } else if (dataSort != 'tag') {
                href = $.format('/?sort=%s&desc=%s', dataSort, false);
                $(this).click(function() {
                    location.href = href;
                });
            }
        });
    };
})();

$(document).ready(ngsvConsole.main.main);
