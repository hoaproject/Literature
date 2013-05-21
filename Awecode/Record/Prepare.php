<?php

require '/usr/local/lib/Hoa/Core/Core.php';

from('Hoa')
-> import('Console.Processus')
-> import('Console.Window');

$windowSize = Hoa\Console\Window::getSize();
$screenSize = array('x' => 0, 'y' => 0);

if(null !== $osascript = Hoa\Console\Processus::locate('osascript')) {

    $handle = Hoa\Console\Processus::execute(
        $osascript .
        ' -e \'tell application "Finder" to get bounds of window of desktop\'',
        false
    );

    list(,, $screenSize['x'], $screenSize['y']) = preg_split('#\s*,\s*#', $handle);
}
elseif(null !== $xwininfo = Hoa\Console\Processus::locate('xwininfo')) {

    preg_match(
        '#\-geometry (\d+)x(\d+)#m',
        Hoa\Console\Processus::execute($xwininfo . ' -root'),
        $matches
    );
    list(, $screenSize['x'], $screenSize['y']) = $matches;
}

Hoa\Console\Window::setSize(89, 26);
Hoa\Console\Window::moveTo(212, 174);
