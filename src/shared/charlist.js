(function($,window,document,Unicopy){
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
		puaName = $('.char-table').attr('data-pua-name');
		$('.char-table td').each(function() {
			var elem = $(this);
			var cp = elem.attr('data-codepoint');
			if (cp) Unicopy.bindToPopup(
				elem,
				String.fromCodePoint(cp),
				puaName && puaName.split(',')
			);
		});
		$('.charlist-charglyph').each(function() {
			var elem = $(this);
			var cp = elem.attr('data-codepoint');
			if (cp) Unicopy.bindToPopup(
				elem,
				String.fromCodePoint(cp),
				puaName && puaName.split(',')
			);
		});
		if ($('#font-selector')) {
			$('#font-selector').bind('change', function() {
				var fontName = $('#font-selector').val();
				if (fontName != 'inherit') fontName = '"' + fontName + '"';
				$('.char-table td').css('font-family', fontName);
				$('.charlist-charglyph').css('font-family', fontName);
			});
			var detector = new Detector();
			var newSelector = '<option selected value="inherit">Default</option>';
			$('#font-selector option').each(function() {
				var fontName = $(this).attr('value');
				if (fontName !== 'inherit' && detector.detect(fontName)) {
					fontName = fontName.replace('&', '&amp;')
									   .replace('<', '&lt;')
									   .replace('>', '&gt;')
									   .replace('"', '&quot;');
					newSelector += (
						'<option value="' + fontName + '">' +
						fontName + '</option>'
					);
				}
			});
			detector.dispose();
			$('#font-selector').html(newSelector);
		}
	});
})(jQuery,window,document,Unicopy);