(function($,window,document){
	var Detector = function() {
		var baseFonts = ['monospace', 'sans-serif', 'serif'];
		var testString = 'mmmmmmmmmmlli';
		var testSize = '72px';
		var defaultWidth = {};
		var defaultHeight = {};
		var body = $('body');
		var span = $('<span/>');
		span.text(testString);
		span.css('font-size', testSize);
		body.append(span);
		for (var i in baseFonts) {
			span.css('font-family', baseFonts[i]);
			defaultWidth[i] = span.width();
			defaultHeight[i] = span.height();
		}
		this.detect = function(font) {
			for (var i in baseFonts) {
				span.css('font-family', '"' + font + '", ' + baseFonts[i]);
				if (span.width() != defaultWidth[i]) return true;
				if (span.height() != defaultHeight[i]) return true;
			}
			return false;
		};
		this.dispose = function() {
			span.remove();
		};
	};
	$(document).ready(function() {
		var detector = new Detector();
		$('.char-glyph-item').each(function() {
			var elem = $(this);
			var fontName = elem.attr('data-font-name');
			if (!detector.detect(fontName)) elem.remove();
		});
		detector.dispose();
	});
})(jQuery,window,document);