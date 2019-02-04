<?php
if (isset($_GET['font'])) {
	$font = preg_replace('/[^A-Za-z0-9]+/', '', $_GET['font']);
	if ($font && file_exists('font/' . $font)) {
		header('Location: /charset/font/' . $font);
		exit(0);
	}
}
header('Location: /charset/font/');