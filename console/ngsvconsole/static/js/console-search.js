var ngsvConsole = ngsvConsole || {};
ngsvConsole.search = ngsvConsole.search || {};

(function() {

    ngsvConsole.search.main = function() {
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

        ngsvConsole.search.setupTopRow();
    };

    ngsvConsole.search.setupTopRow = function() {
        var $icon = $('<i class="icon-chevron-down"></i>');
        var params = ngsvConsole.getUrlVars();

        $('#top-row').find('div').each(function() {
            var dataSort = $(this).attr('data-sort');

            if (dataSort == sort) {
                $(this).append($icon);

                $(this).click(function() {
                    var newParams = {};
                    for (var i = 0; i < params.length; ++i) {
                        var key = params[i];
                        newParams[key] = params[key];
                    }

                    newParams['sort'] = sort;
                    newParams['desc'] = !desc;

                    var href = '/search?';
                    i = 0;
                    for (key in newParams) {
                        if (i > 0) href += '&';
                        href += key + '=' + newParams[key];
                        i++;
                    }

                    location.href = href;
                });
            } else if (dataSort != 'tag') {
                $(this).click(function() {
                    var newParams = {};
                    for (var i = 0; i < params.length; ++i) {
                        var key = params[i];
                        newParams[key] = params[key];
                    }

                    newParams['sort'] = dataSort;
                    newParams['desc'] = 'false';

                    var href = '/search?';
                    i = 0;
                    for (key in newParams) {
                        if (i > 0) href += '&';
                        href += key + '=' + newParams[key];
                        i++;
                    }
                    location.href = href;
                });
            }
        });
    };
})();

$(document).ready(ngsvConsole.search.main);
