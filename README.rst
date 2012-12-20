
========
Tag diff
========

This tool tags diff.


Installation
------------

You may install the tool using::

 % python setup install --user

Example
-------

Example::

 % diff -u examples/*.txt | tag_diff -
 % cat examples/1.txt | tag_diff - -n

