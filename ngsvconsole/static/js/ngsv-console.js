var ngsvConsole = ngsvConsole || {};

(function() {

    ngsvConsole.getUrlVars = function() {
        var vars = [], hash;
        var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
        for(var i = 0; i <hashes.length; i++)
        {
            hash = hashes[i].split('=');
            vars.push(hash[0]);
            vars[hash[0]] = hash[1];
        }
        return vars;
    };

    ngsvConsole.formatSize = function(size) {
        if (size < 1000)
            return $.format('%dB', size);
        else if ( size < Math.pow(1000, 2))
            return $.format('%f.1KB', (size / 1000.0));
        else if (size < Math.pow(1000, 3))
            return $.format('%.1fMB', (size / Math.pow(1000.0, 2)));
        else if (size < Math.pow(1000, 4))
            return $.format('%.1fGB', (size / Math.pow(1000.0, 3)));
        else if (size < Math.pow(1000, 5))
            return $.format('%.1fTB', (size / Math.pow(1000.0, 4)));
        else
            return $.format('%.1fPB', (size / Math.pow(1000.0, 5)));
    };
})();
