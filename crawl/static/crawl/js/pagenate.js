
$.fn.pagenate = function() {
    var table = this;
    var pager = $('#pager');
    var perPage;
    var content_div = document.getElementById('content');

    var height = window.innerHeight
                 || document.documentElement.clientHeight
                 || document.body.clientHeight;

    var width = window.innerWidth
                || document.documentElement.clientWidth
                || document.body.clientWidth;

    if (width < 1000) {
        var content_div_height;
        if (height >= 500)
            content_div_height = height - 400;
        else
            content_div_height = 100;
        content_div.style.height = content_div_height + 'px';
        perPage = Math.floor(content_div_height / 80);
    }
    else {
        var content_div_height;
        if (height >= 350)
            content_div_height = height - 250;
        else
            content_div_height = 100;
        content_div.style.height = content_div_height + 'px';
        perPage = Math.floor(content_div_height / 60);
    }

    var children = table.children();
    var numPages = Math.ceil(children.size() / perPage);

    if (numPages <= 1)
        return;

    if (numPages > 20) {
        numPages = 20;
        perPage = Math.floor(children.size() / numPages);
        content_div_height = ($('tr').eq(0).height() + 6) * perPage;
        content_div.style.height = content_div_height + 'px';
    }

    var curr = 1;
    pager.children().remove();
    while (curr <= numPages) {
        $('<li><a href="#" class="pager_page">' + curr + '</a></li>').appendTo(pager);
        curr++;
    }

    children.hide();
    goTo(0);

    pager.find('li .pager_page').click(function() {
        var clickedPage = $(this).html().valueOf() - 1;
        goTo(clickedPage);
        return false;
    });

    function goTo(page) {
        var startAt = page * perPage,
            endOn = startAt + perPage;

        children.css('display','none').slice(startAt, endOn).show();

        pager.children().removeClass("active");
        pager.children().eq(page).addClass("active");
    }
};
