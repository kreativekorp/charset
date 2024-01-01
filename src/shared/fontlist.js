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
		var filterInput = $('.font-options input[name=q]');
		var filterValue = null;
		var filterUpdate = function () {
			var s = filterInput.val().replaceAll(/^\s+|\s+$/g, '').replaceAll(/\s+/g, ' ').toLowerCase();
			if (s === filterValue) return;
			filterValue = s;
			$('.font-item').each(function() {
				var fontItem = $(this);
				var keywords = fontItem.attr('data-keywords');
				if (keywords.indexOf(s) >= 0) {
					fontItem.removeClass('hidden');
				} else {
					fontItem.addClass('hidden');
				}
			});
		};
		filterInput.bind('change', filterUpdate);
		filterInput.bind('keydown', filterUpdate);
		filterInput.bind('keyup', filterUpdate);
		$('body').bind('keydown', function(e) {
			if (e.which === 27) {
				filterInput.val('');
				filterInput.focus();
				e.preventDefault();
				e.stopPropagation();
			}
		});

		var nameButton = $('.font-options input[name=s][value=n]');
		var countButton = $('.font-options input[name=s][value=c]');
		nameButton.click(function (e) {
			$($('.font-item').toArray().sort(function (a, b) {
				var aVal = a.getAttribute('data-font-name').toLowerCase();
				var bVal = b.getAttribute('data-font-name').toLowerCase();
				return aVal.localeCompare(bVal);
			})).detach().appendTo($('.font-list'));
		});
		countButton.click(function (e) {
			$($('.font-item').toArray().sort(function (a, b) {
				var aVal = parseInt($(a).find('.font-ccount .value').text(), 10);
				var bVal = parseInt($(b).find('.font-ccount .value').text(), 10);
				return bVal - aVal;
			})).detach().appendTo($('.font-list'));
		});

		var detector = new Detector();
		$('.font-item').each(function() {
			var fontItem = $(this);
			var fontName = fontItem.attr('data-font-name');
			var pswitch = fontItem.find('.font-pswitch');
			var preview = fontItem.find('.font-preview');
			var bcount = fontItem.find('.font-bcount');
			var blocks = fontItem.find('.font-blocks');
			var keywords = (blocks.text().replaceAll(/\s+\(\d+\)/g, '').replaceAll(', ', '\u007F') + '\u007F' + fontName).toLowerCase();
			fontItem.attr('data-keywords', keywords);
			bcount.click(function (e) {
				blocks.toggleClass('hidden');
				e.stopPropagation();
				e.preventDefault();
				return false;
			});
			if (detector.detect(fontName)) {
				pswitch.click(function (e) {
					preview.toggleClass('hidden');
					e.stopPropagation();
					e.preventDefault();
					return false;
				});
			} else {
				pswitch.text('Not Installed');
				preview.remove();
			}
		});
		detector.dispose();
	});
})(jQuery,window,document);