(function($) {

  class TightGrid {
    constructor($el, options = {}) {
      this.options = options;
      this.$el     = $el;

      this.columnWidth  =
        this.options.columnWidth ||
        this.$el.find(this.options.itemSelector).first().outerWidth(true);

      this.build();

      if (this.options.resize) {
        this.resizeHandler = this.rebuild.bind(this);
        $(window).on('resize', this.resizeHandler);
      }
    }

    build() {
      const colsInRow = Math.floor(this.$el.width() / this.columnWidth);
      let $items      = [];

      this.$el.find(this.options.itemSelector).each((_, item) => {
        let $item = $(item);
        let cols  = Math.floor($item.outerWidth(true) / this.columnWidth);

        for(let i = 0; i < cols; i++) { $items.push($item) };
      });

      $items.forEach(($item, i) => {
        if (i < colsInRow) { return }

        const $itemAbove = $items[i - colsInRow];

        const bottomOffsetOfItemAbove =
          $itemAbove.offset().top +
          $itemAbove.outerHeight() +
          parseInt($itemAbove.css('margin-bottom'));

        const topOffsetOfItem =
          $item.offset().top -
          parseInt($item.css('margin-top')) -
          parseInt($itemAbove.css('margin-bottom'));

        const delta = topOffsetOfItem - bottomOffsetOfItemAbove;

        if (delta) { $item.css('margin-top', -delta) }
      });
    }

    rebuild() {
      this.reset();
      this.build();
    }

    reset() {
      this.$el.find(this.options.itemSelector).css('margin-top', '');
    }

    destroy() {
      this.reset();

      this.options.resize && $(window).off('resize', this.resizeHandler);
    }
  }

  $.fn.tightGrid = function(options = {}) {
    options = $.extend({}, $.fn.tightGrid.defaults, options);

    this.each(function() {
      let $this = $(this);

      if (!$this.data('tightGrid')) {
        $this.data('tightGrid', new TightGrid($this, options));
      }
    });
  }

  $.fn.tightGrid.defaults = {
    itemSelector: '.js-item',
    columnWidth: null,
    resize: true
  }

}(jQuery));
