(function($,window,document,UCD,PUA,Unicopy){

var urlParam = function(name) {
	var re = new RegExp('[\?&]' + name + '=([^&#]*)');
	var results = re.exec(window.location.href);
	return results ? decodeURIComponent(results[1]) : '';
};

var splitTokens = function(s) {
	var tokens = [];
	var a = s.replace(/^\s+/, '').replace(/\s+$/, '').split(/\s+/);
	for (var i = 0, n = a.length; i < n; i++) {
		var f = 1, w = undefined, t = a[i], o;
		if ((o = t.indexOf(':')) >= 0) {
			switch (t.substr(0, o)) {
				case 'name': f = 1; t = t.substr(o + 1); break;
				case 'prop': f = 2; t = t.substr(o + 1); break;
				case 'comb': f = 3; t = t.substr(o + 1); break;
				case 'bidi': f = 4; t = t.substr(o + 1); break;
				case 'decomp': f = 5; t = t.substr(o + 1); break;
				case 'number': f = 8; t = t.substr(o + 1); break;
				case 'mirror': f = 9; t = t.substr(o + 1); break;
			}
		}
		if ((o = t.indexOf(':')) >= 0) {
			switch (t.substr(0, o)) {
				case 'whole': w = true; t = t.substr(o + 1); break;
				case 'string': w = false; t = t.substr(o + 1); break;
			}
		}
		if (w === undefined) w = (t.length < 4);
		if (t.length > 0) tokens.push([f, w, t]);
	}
	return tokens;
};

var dataMatches = function(data, tokens) {
	for (var i = 0, n = tokens.length; i < n; i++) {
		var a = (tokens[i][0] === 1) ? (data[1] + ' ' + data[10]) : data[tokens[i][0]];
		var e = tokens[i][2];
		if (tokens[i][1]) {
			a = ' ' + a + ' ';
			e = ' ' + e + ' ';
		}
		if (a.toUpperCase().indexOf(e.toUpperCase()) < 0) {
			return false;
		}
	}
	return true;
};

var createTable = function(chars, tokens, baseURL) {
	var table = $('<table/>').addClass('whereis-table');
	$.each(chars, function(cp, data) {
		if (dataMatches(data, tokens)) {
			var tr = $('<tr/>');
			tr.append($('<td/>').addClass('whereis-codepoint').text(data[0]));
			tr.append($('<td/>').addClass('whereis-charglyph').text(String.fromCodePoint(cp)));
			var td = $('<td/>').addClass('whereis-charname');
			var a = $('<a/>');
			a.text((data[1] === '<control>') ? data[10] : data[1]);
			a.attr('href', baseURL + data[0]);
			a.attr('target', '_blank');
			td.append(a);
			tr.append(td);
			table.append(tr);
		}
	});
	return table;
};

$(document).ready(function() {

var input = $('.whereis-input');
var output = $('.whereis-output');
var last_s = null;

var update = function() {
	var s = input.val();
	if (s === last_s) return;
	last_s = s;
	output.empty();
	var tokens = splitTokens(s);
	if (tokens && tokens.length) {
		var table = createTable(UCD['chars'], tokens, '/charset/unicode/char/');
		if (!table.is(':empty')) {
			output.append(table);
			Unicopy.bindToPopups(table.find('.whereis-charglyph'));
		}
		var tables = [];
		$.each(PUA, function(name, pua) {
			var url = '/charset/pua/' + name.replace(/[^A-Za-z0-9]+/g, '');
			var table = createTable(pua['chars'], tokens, url + '/char/');
			if (!table.is(':empty')) {
				var h3 = $('<h3/>').append($('<a/>').text(name).attr('href', url));
				tables.push([[h3, table], table.find('.whereis-charglyph'), [name]]);
			}
		});
		if (tables.length) {
			tables.sort(function(a, b) {
				a = a[2][0];
				b = b[2][0];
				if (a < b) return -1;
				if (a > b) return 1;
				return 0;
			});
			output.append($('<h2/>').text('Private Use Characters'));
			for (var i = 0, n = tables.length; i < n; i++) {
				output.append(tables[i][0]);
				Unicopy.bindToPopups(tables[i][1], tables[i][2]);
			}
		}
		if (output.is(':empty')) {
			var p = $('<p/>');
			p.addClass('whereis-notfound');
			p.text('No results found. Try using fewer terms or alternate spellings.');
			output.append(p);
		}
	} else {
		var optable = $('<table/>').addClass('whereis-table');
		optable.append($('<tr><td class="whereis-operator">name:</td><td class="whereis-oplabel">Search by character name (the default).</td></tr>'));
		optable.append($('<tr><td class="whereis-operator">prop:</td><td class="whereis-oplabel">Search by character property.</td></tr>'));
		optable.append($('<tr><td class="whereis-operator">comb:</td><td class="whereis-oplabel">Search by combining class.</td></tr>'));
		optable.append($('<tr><td class="whereis-operator">bidi:</td><td class="whereis-oplabel">Search by bidi class.</td></tr>'));
		optable.append($('<tr><td class="whereis-operator">decomp:</td><td class="whereis-oplabel">Search by decomposition.</td></tr>'));
		optable.append($('<tr><td class="whereis-operator">number:</td><td class="whereis-oplabel">Search by numeric value.</td></tr>'));
		optable.append($('<tr><td class="whereis-operator">mirror:</td><td class="whereis-oplabel">Search by bidi mirrored.</td></tr>'));
		optable.append($('<tr><td class="whereis-operator">whole:</td><td class="whereis-oplabel">Search for a whole word (default for words 1 to 3 letters long).</td></tr>'));
		optable.append($('<tr><td class="whereis-operator">string:</td><td class="whereis-oplabel">Search for a partial word (default for words 4 letters or longer).</td></tr>'));
		output.append(optable);
	}
};

input.val(urlParam('q'));
update();

var updateTimeout = null;
var updateWithDebounce = function() {
	window.clearTimeout(updateTimeout);
	updateTimeout = window.setTimeout(update, 250);
};

input.bind('change', updateWithDebounce);
input.bind('keydown', updateWithDebounce);
input.bind('keyup', updateWithDebounce);

$('body').bind('keydown', function(e) {
	if (e.which === 27) {
		input.val('');
		input.focus();
		e.preventDefault();
		e.stopPropagation();
	}
});

});

})(jQuery,window,document,UCD,PUA,Unicopy);