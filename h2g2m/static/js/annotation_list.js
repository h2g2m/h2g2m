$(function() {
    $('.annotation-list tr').each(function(i, tr) {
        $(tr).find('td:first-child').each(function(i, td) {
            var a = $(document.createElement('a'))
            var new_tr;
            a.attr('href', '#');
            a.html('<i class="icon-plus-sign"></i>');
            $(td).prepend(a);
            a.toggle(function() {
                var id = $(tr).attr('class').split(/\s+/)[1].replace('annotation-id-', '');
                new_tr = $(document.createElement('tr'));
                $.getJSON('/a/'+id+'/', {}).done(function( json ) {
                    s  = '<td colspan="6">';
                    s += '<p>'+json['annotation']['html_content']+'</p>';
                    s += '</td>'
                    new_tr.html(s);
                    new_tr.ready(function() {
                        MathJax.Hub.Queue(["Typeset",MathJax.Hub, new_tr[0]]);
                    });
                });
                new_tr.insertAfter($(tr));
            }, function() { new_tr.remove(); });
        });
    });
});

