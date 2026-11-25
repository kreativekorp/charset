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
		$('[data-codepoint]').each(function() {
			var elem = $(this);
			var cp = elem.attr('data-codepoint');
			if (cp) Unicopy.bindToPopup(
				elem,
				String.fromCodePoint.apply(String, cp.split(',')),
				puaName && puaName.split(',')
			);
		});
		if ($('#font-selector').length) {
			$('#font-selector').bind('change', function() {
				var fontName = $('#font-selector').val();
				if (fontName !== 'inherit') fontName = '"' + fontName + '"';
				$('.char-glyph').css('font-family', fontName);
				$('.charlist-charglyph').css('font-family', fontName);
			});
			var detector = new Detector();
			$('#font-selector optgroup').each(function() {
				var elem = $(this);
				var newOptions = '';
				elem.children('option').each(function() {
					var fontName = $(this).attr('value');
					if (detector.detect(fontName)) {
						newOptions += this.outerHTML;
					}
				});
				if (newOptions) elem.html(newOptions);
				else elem.remove();
			});
			detector.dispose();
		}
		$('button.show-alt-codes').bind('click', function() {
			$('.char-box:not(:first-child)').show();
		});
		$('button.hide-alt-codes').bind('click', function() {
			$('.char-box:not(:first-child)').hide();
		});
		$('body').bind('keydown', function(e) {
			if (e.which === 0x70) {
				$('.char-box:not(:first-child)').toggle();
				e.stopPropagation();
				e.preventDefault();
			}
		});
	});
})(jQuery,window,document,Unicopy);