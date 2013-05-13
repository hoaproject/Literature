<?php

require '/usr/local/lib/Hoa/Core/Core.php';

from('Hoa')
-> import('Console.Readline.~')
-> import('Console.Processus');

class Patcher {

    protected $_readline = null;
    protected $_editors  = array();
    protected $_filename = null;
    protected $_glutton  = false;
    protected $_diff     = null;
    protected $_timeline = array();

    public function __construct ( $repository ) {

        $this->_readline = new Hoa\Console\Readline();
        $git             = new Hoa\Console\Processus(
            'git log --pretty=\'format:\' --patch --reverse --raw -z',
            null,
            null,
            $repository
        );
        $git->on('output', xcallable($this, 'output'));
        $git->on('stop',   xcallable($this, 'over'));
        $git->run();
    }

    public function output ( Hoa\Core\Event\Bucket $bucket ) {

        $data = $bucket->getData();
        $line = $data['line'];

        if(empty($line))
            return;

        if(true === $this->_glutton) {

            if("\0" === $line) {

                $this->keyframe();

                return;
            }

            $this->_diff .= $line . "\n";

            return;
        }

        if('+++' === substr($line, 0, 3)) {

            $this->_glutton = true;

            return;
        }

        if(':' === $line[0]) {

            list(, $this->_filename,,) = explode("\0", $line);

            if(!isset($this->_editors[$this->_filename])) {

                while(false == $id = $this->_readline->readLine('(id#' . $this->_filename . ') > '));

                $this->_editors[$this->_filename] = array(
                    'id'        => $id,
                    'name'      => $this->_filename,
                    'keyframes' => array()
                );
            }

            return;
        }

        return;
    }

    public function keyframe ( ) {

        $editor = &$this->_editors[$this->_filename];
        $name   = $editor['name'];

        $editor['keyframes'][] = array(
            'start' => 0,
            'end'   => 0,
            'diff'  => rtrim($this->_diff)
        );
        end($editor['keyframes']);

        $this->_timeline[] = &$editor['keyframes'][key($editor['keyframes'])];
        $this->_glutton    = false;
        $this->_diff       = null;
    }

    public function over ( ) {

        // empty buffer.
        $this->keyframe();

        echo "\n\n", 'Ready to set the timeline? (y/n)', "\n";
        while('y' !== $this->_readline->readLine('> '));

        echo "\n", 'Start by pressing Enter', "\n";
        $this->_readline->readLine();

        $start    = 0;
        $end      = 0;
        $time     = time();
        $previous = null;

        foreach($this->_timeline as &$keyframe) {

            echo $keyframe['diff'], "\n";

            $this->_readline->readLine();

            $keyframe['start'] = time() - $time;

            if(null === $previous) {

                $previous = &$keyframe;

                continue;
            }

            $previous['end'] = $keyframe['start'];
            $previous        = &$keyframe;
        }

        echo 'End', "\n";
        $this->_readline->readLine();
        $previous['end'] = time() - $time;

        echo "\n\n", 'Where to save it?', "\n";

        while(false === $save = $this->_readline->readLine('> '));

        $out = json_encode(array_values($this->_editors));
        echo $out, "\n\n";

        var_dump(file_put_contents($save, $out));

        return;
    }
}

if(!isset($_SERVER['argv'][1]))
    exit('A repository path must be given.');

$p = new Patcher($_SERVER['argv'][1]);
