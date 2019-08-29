
$('.single-post-link').click( function(e) {
    // console.log(e);
    // e.preventDefault();
    var item_id = e.target.id;
    console.log(item_id);
    var clicked_items = Cookies.get('clicked_items') ? Cookies.get('clicked_items') : '';
    Cookies.set('clicked_items', clicked_items + item_id + ',');
    return true;
} );
