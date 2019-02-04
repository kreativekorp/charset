<?php
if (isset($_GET['q'])) {
	header('Location: /charset/whereis/?q=' . urlencode($_GET['q']));
} else {
	header('Location: /charset/whereis/');
}