$(document).ready(function() {
	var noselect = {
		'-webkit-user-select': 'none',
		'-khtml-user-select': 'none',
		'-moz-user-select': 'none',
		'-ms-user-select': 'none',
		'user-select': 'none',
		'cursor': 'default'
	};
	var bindSwitch = function(i) {
		var bls = $('#block-list-switch-' + i);
		var brs = $('#block-roadmap-switch-' + i);
		var bl = $('#block-list-' + i);
		var br = $('#block-roadmap-' + i);
		bls.find('a').bind('click', function(e) {
			bls.addClass('hidden');
			brs.removeClass('hidden');
			bl.removeClass('hidden');
			br.addClass('hidden');
			e.stopPropagation();
			e.preventDefault();
		});
		brs.find('a').bind('click', function(e) {
			bls.removeClass('hidden');
			brs.addClass('hidden');
			bl.addClass('hidden');
			br.removeClass('hidden');
			e.stopPropagation();
			e.preventDefault();
		});
		bls.find('b').css(noselect);
		brs.find('b').css(noselect);
	};
	for (var i = 0; i < 17; i++) bindSwitch(i);
});