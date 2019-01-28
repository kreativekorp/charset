(function($,window,document,Unicopy){
	$(document).ready(function() {
		puaName = $('.pua-notice').attr('data-pua-name');
		$('.char-table td').each(function() {
			var elem = $(this);
			Unicopy.bindToPopup(
				elem,
				String.fromCodePoint(elem.attr('data-codepoint')),
				puaName && [puaName]
			);
		});
		$('.charlist-charglyph').each(function() {
			var elem = $(this);
			Unicopy.bindToPopup(
				elem,
				String.fromCodePoint(elem.attr('data-codepoint')),
				puaName && [puaName]
			);
		});
	});
})(jQuery,window,document,Unicopy);