$(document).ready(function()
{
    var $container = $('#masonry_container');
    $container.imagesLoaded( function() {
        $container.masonry();
    });
});
