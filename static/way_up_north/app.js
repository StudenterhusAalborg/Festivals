
function insertSeperators() {
    $(".artist").each( function (index) {
        const el = $(this);
        if(index !== 0 && el.position().top === el.prev().position().top)
        {
            el.addClass("sep");
        }
        else {
            el.removeClass("sep");
        }
    });
}
$( document ).ready( insertSeperators);
$( window ).resize( insertSeperators);