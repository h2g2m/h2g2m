(function($) {
    'use strict';

    var languages = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: '/language.json'
    });
    $(document).ready(function() {
        $('input[name=language]').typeahead({
            hint: true,
            highlight: true,
            minLength: 1
        },
        {
            name: 'languages',
            source: languages
        });
    });
})(jQuery);
