(function($,window,document,UCD,Unicopy){

var urlParam = function(name) {
	var re = new RegExp('[\?&]' + name + '=([^&#]*)');
	var results = re.exec(window.location.href);
	return results ? decodeURIComponent(results[1]) : '';
};

var egg = [
	'WIRELESS WIZARD',
	'TEXTING FROM A FEW FEET AWAY',
	'FOR SHAME',
	'AND WHAT IS THIS OTHER TEXT MESS',
	'THAT IS A FRONTWAYS CUPID',
	'LOOKS MORE LIKE A USB DONGLE GOBLIN'
];

$(document).ready(function() {

var input = $('.whatis-input');
var output = $('.whatis-output');
var last_s = null;

var update = function() {
	var s = input.val();
	if (s === last_s) return;
	last_s = s;
	var isegg = (s === '>KO)->');
	var chars = Unicopy.stringToChars(s);
	var elems = [];
	for (var i = 0, n = chars.length; i < n; i++) {
		var data = Unicopy.getCharacterData(chars[i]);
		var tr = $('<tr/>');
		tr.append($('<td/>').addClass('whatis-codepoint').text(data[0]));
		tr.append($('<td/>').addClass('whatis-charglyph').text(String.fromCodePoint(chars[i])));
		var td = $('<td/>').addClass('whatis-charname');
		if (data[15]) {
			var tag = $('<div/>');
			tag.addClass('whatis-tag');
			tag.text('PUA');
			tag.attr('title', (
				'This is a private use character. Its use and ' +
				'interpretation is not specified by the Unicode ' +
				'Standard but may be determined by private agreement ' +
				'among cooperating users. The interpretation shown ' +
				'here is only one of many possible interpretations.'
			));
			td.append(tag);
		}
		var charname = isegg ? egg[i] : (data[1] === '<control>') ? data[10] : data[1];
		if (UCD['chars'][chars[i]]) {
			var a = $('<a/>');
			a.text(charname);
			a.attr('href', '/charset/unicode/char/' + data[0]);
			a.attr('target', '_blank');
			td.append(a);
		} else {
			var span = $('<span/>');
			span.text(charname);
			td.append(span);
		}
		tr.append(td);
		elems.push(tr);
	}
	output.empty().append(elems);
	Unicopy.bindToPopups($('.whatis-charglyph'));
};

var q = urlParam('q');
if (q) {
	input.val(q);
	update();
}

input.bind('change', update);
input.bind('keydown', update);
input.bind('keyup', update);

$('body').bind('keydown', function(e) {
	if (e.which === 27) {
		input.val('');
		input.focus();
		e.preventDefault();
		e.stopPropagation();
	}
});

});

})(jQuery,window,document,UCD,Unicopy);