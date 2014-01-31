/* Layouting fotto.
 *
 * * each row has a given length(e.g. determined by the browser window)
 * * images (or 'items' in general) have a desired height, e.g. 300px.
 * * items are bin-packed to best match the row width
 * * rows are rescaled in height to exactly match the row width
 */
Array.prototype.last = Array.prototype.last || function() {
        var l = this.length;
        return this[l-1];
}

jQuery.fn.center = function(parent) {
    if (parent) {
        parent = this.parent();
    } else {
        parent = window;
    }
    this.css({
        "position": "absolute",
        "top": ((($(parent).height() - this.outerHeight()) / 2)),
        "left": ((($(parent).width() - this.outerWidth()) / 2) )
    });
    return this;
}

var animation_lock = false;
var deferreds = []

var Item = function(item)
{
    this.item = item;
    this.ar = parseFloat($(item).attr('data-aspect'));

    this.width = function(h)
    {
        return h * this.ar;
    };

    this.overhead = $(item).outerWidth() - $(item).width();
}

var Row = function(target_width, target_height)
{
    this.target_width = target_width;
    this.target_height = target_height;
    this.width = function()
    {
        return _.reduce(this.items, function(memo, item){return item.width(this.target_height)+memo;}, 0);
    }

    this.overhead_y = function()
    {
        lst = _.map(this.items, function(item){return $(item.item).outerHeight() - $(item.item).height();})
        return _.max(lst)
    }

    this.overhead = function()
    {
        return _.reduce(this.items, function(memo, item){return item.overhead + memo;}, 0);
    }

    this.items = [];
    this.push = function(item)
    {
        if(this.width() + this.overhead() + item.width(this.target_height) + item.overhead < this.target_width) {
            this.items.push(item);
            return true;
        }
        else{
            return false;
        }
    };

    this.inflate = function(offset)
    {
        factor = (this.target_width - this.overhead()) / this.width();
        var h_ref = this.target_height * factor;
        // console.log("factor", factor, "since", this.width(), "times", factor, "plus", this.overhead(), "is", this.target_width);
        var offset_left = 0;

        $.each(this.items, function(index, item)
        {
            // console.log("inflating", item)
            // console.log("h_ref=", h_ref)
            new_w = h_ref * item.ar;
            // console.log("->", new_w, h_ref);

            deferred = $(item.item).animate(
                {
                    width: new_w,
                    height: h_ref,
                    top: offset,
                    left: offset_left
                },
                2000,
                function(){}
            ).promise();

            deferreds.push(deferred);
            offset_left += (new_w + item.overhead);
        });

        new_offset = (this.overhead_y() + h_ref) + offset;
        // console.log("new offset:", new_offset);
        return new_offset;
    };
};

var Bricking = function(container, item_selector)
{
    this.container = $(container);
    this.items = $(item_selector, this.container);


    this.layout = function()
    {
        this.items.css("position", "absolute");
        rows = []

        target_width = this.container.innerWidth();
        target_height  = 200;

        rows.push(new Row(target_width, target_height));

        this.items.each(function(index, item){
            var _i = new Item(item);
            if(!rows.last().push(_i)){
                rows.push(new Row(target_width, target_height));
                rows.last().push(_i);
            }
        });
        // console.log('rows', rows)

        offset = 0;

        $.each(rows, function(index, row){
            offset = row.inflate(offset);
        //    console.log("row width", row.width());
        });
    };
};

var lightbox = function(item, images)
{
    this.images = images;
    this.container = item;

    images.each(function(index, image)
    {
        $(image).clone().appendTo(this.container);
        console.log(this);
    }.bind(this));

    $('img', this.container).css('position', 'absolute').css('top', 0).css('left', 0);
};

$(document).ready(function()
{
    $elem = $('#lightbox');

    //var lb = new lightbox($elem, $('#masonry_container img'));

    $('.item img').bind('click', function(event){
        src = $(this).attr("src");
        $('img', $elem).attr("src", src);
        var width = $('img', $elem).prop('naturalWidth');
        var height = $('img', $elem).prop('naturalHeight');
        ratio = width/height;

        winheight = $(window).height();
        winwidth = $(window).width();

        maxwidth = 0.9 * winwidth;
        maxheight = 0.9 * winheight;

        maxwidth = Math.min(maxwidth, width);
        maxheight = Math.min(maxheight, height);

        ratio_window = maxwidth/maxheight;

        if(ratio_window > ratio){
            // need to set height of the image
            $('img', $elem).css('height', maxheight).css('width', maxheight * ratio);
            console.log("setting height", maxheight)
        }
        else{
            $('img', $elem).css('width', maxwidth).css('height', maxwidth / ratio);
            console.log("setting width", maxwidth)
        }

        console.log("new size:", $('img', $elem).width(), $('img', $elem).height());

        // set img to window center
        _top = 0.5 * (winheight - $('img', $elem).height());
        _left = 0.5 * (winwidth - $('img', $elem).width());

        console.log("top/left", _top, _left);

        $('img', $elem).css('left', _left).css('top', _top);

        $elem.show();
    });

    $($elem).bind('click', function(event){
        $elem.hide();
    });


    var $container = $('#masonry_container');

    $container.imagesLoaded( function() {
        var brick_layout = new Bricking($container, '.item');
        brick_layout.layout();

        $(window).resize(function(){
            console.log("resize");
            brick_layout.layout();
        });
    });

});
