$(document).ready(function()
{

    Array.prototype.last = Array.prototype.last || function() {
        var l = this.length;
        return this[l-1];
    }

    var $container = $('#masonry_container');
    $container.imagesLoaded( function() {
        rows = []

        var Row = function(target_width)
        {
            this.target_width = target_width;
            this.width = function()
            {
                return _.reduce(this.items, function(memo, item){return $(item).outerWidth()+memo;}, 0);
            }
            this.items = [];
            this.push = function(item)
            {
                w = $(item).outerWidth();
                if(this.width() + w < $container.width()) {
                    this.items.push(item);
                    return true;
                }
                else{
                    return false;
                }
            };

            this.inflate = function(offset)
            {
                factor = this.target_width / this.width();
                console.log("factor", factor, "since", this.width(), "times", factor, "is", this.target_width);
                offset_left = 0;
                $.each(this.items, function(index, item){
                    w = $(item).outerWidth();
                    h = $(item).outerHeight();
                    //console.log("w, h", w, h);
                    new_w = w * factor;
                    new_h = h * factor;
                    //console.log("->", new_w, new_h);
                    $(item).outerWidth(new_w);
                    $(item).outerHeight(new_h);
                    $(item).css("top", offset);
                    $(item).css("left", offset_left);
                    offset_left += new_w
                });

                highest =  _.max(this.items, function(item){return $(item).outerHeight();});
                new_offset = $(highest).outerHeight() + offset;
                console.log("new offset:", new_offset);
                return new_offset;
            };
        }

        target_width = $container.innerWidth() * 0.8;

        rows.push(new Row(target_width));

        $('.item').each(function(index, item){
            if(!rows.last().push(item)){
                rows.push(new Row(target_width));
                rows.last().push(item);
            }
        });
        console.log('rows', rows)

        offset = 0;

        $.each(rows, function(index, row){
            offset = row.inflate(offset);
            console.log("row width", row.width());
        });

    });


});
