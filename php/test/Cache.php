<?php
namespace ccxtpro;
include_once __DIR__ . '/../../vendor/autoload.php';
// ----------------------------------------------------------------------------

// PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
// https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

// -----------------------------------------------------------------------------

function equals($a, $b) {
    return json_encode($a) === json_encode($b);
}

// --------------------------------------------------------------------------------------------------------------------

$cache = new ArrayCache (3);

$cache->append (1);
$cache->append (2);
$cache->append (3);
$cache->append (4);

assert (equals ($cache, [2, 3, 4]));

$cache->append (5);
$cache->append (6);
$cache->append (7);
$cache->append (8);

assert (equals ($cache, [6, 7, 8]));

$cache->clear ();

assert (equals ($cache, array()));

$cache->append (1);

assert (equals ($cache, [1]));

// --------------------------------------------------------------------------------------------------------------------

$cache = new ArrayCache (1);

$cache->append (1);
$cache->append (2);

assert (equals ($cache, [2]));
