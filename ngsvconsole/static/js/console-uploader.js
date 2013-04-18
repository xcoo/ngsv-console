var console = console || {};
console.uploader = console.uploader || {};

(function() {

    console.uploader.main = function() {
        $('#sam-upload-select-btn').click(console.uploader.addSamUploader);
        $('#bed-upload-select-btn').click(console.uploader.addBedUploader);

        $('.progress .bar').each(function() {
            if ($(this).html() == '100%') {
                $(this).parent('div').removeClass('active progress-striped');
            } else {
                $(this).parent('div').addClass('active progress-striped');
            }
        });
    };

    console.uploader.addSamUploader = function() {
        var id = 0;
        while (1) {
            if ($($.format('#sam-upload_%02d', id)).length == 0)
                break;
            id++;
        };

        var upload = $.format('sam-upload_%02d', id);
        var cover = $.format('sam-upload-cover_%02d', id);
        var btn = $.format('sam-upload-btn_%02d', id);
        var progress = $.format('sam-upload-progress_%02d', id);

        var $e = $('#new-sam-tmpl').tmpl({
            upload: upload,
            cover: cover,
            btn: btn,
            progress: progress });
        $e.prependTo('#new-task').hide().fadeIn(200);

        $('#' + upload).change(function() {
            $('#' + cover).html($(this).val());
        });

        console.uploader.initUploader('/api/upload-sam', $('#' + upload), $('#' + btn), $('#' + progress));

        $e.find('button.close').click(function() {
            $e.fadeOut(200, function() { $(this).remove(); });
        });
    };

    console.uploader.addBedUploader = function() {
        var id = 0;
        while (1) {
            if ($($.format('#bed-upload_%02d', id)).length == 0)
                break;
            id++;
        };

        var upload = $.format('bed-upload_%02d', id);
        var cover = $.format('bed-upload-cover_%02d', id);
        var btn = $.format('bed-upload-btn_%02d', id);
        var progress = $.format('bed-upload-progress_%02d', id);

        var $e =  $('#new-bed-tmpl').tmpl({
            upload: upload,
            cover: cover,
            btn: btn,
            progress: progress });
        $e.prependTo('#new-task').hide().fadeIn(200);

        $('#' + upload).change(function() {
            $('#' + cover).html($(this).val());
        });

        console.uploader.initUploader('/api/upload-bed', $('#' + upload), $('#' + btn), $('#' + progress));

        $e.find('button.close').click(function() {
            $e.fadeOut(200, function() { $(this).remove(); });
        });
    };

    console.uploader.initUploader = function(url, file, button, progress) {
        var up = new uploader(file.get(0), {
            url: url,
			progress: function(ev) {
                var value = (ev.loaded / ev.total) * 100;
                progress.html(Math.floor(value) + '%');
                progress.css('width', value + '%');
            },
			error: function(ev) {
                console.log('error');
            },
			success: function(data) {
                progress.html('100%');
                progress.css('width', '100%');
                progress.parent('div').removeClass('active progress-striped');
            }
        });

		button.click(function() {
            progress.parent('div').addClass('active progress-striped');
			up.send();
		});
    };
}());

$(document).ready(console.uploader.main);
