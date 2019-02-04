<?php
if (isset($_GET['q'])) {
	header('Location: /charset/whatis/?q=' . urlencode($_GET['q']));
} else {
	header('Location: /charset/whatis/');
}