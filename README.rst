Tag diff
========

This tool annotates diffs from geographical files.

Installation
------------

You may install the tool using:

.. code-block:: bash

 $ python setup install --user

Example
-------

Suppose we have two tab-separated files, formatted like this (code, name, lat, lng):

.. code-block:: bash

 $ head -n3 examples/2.txt
 MLC	Mc Alester Regonal Airport	34.882403	-95.783463
 NDS	Sandtone Airport	-28	119.4
 SPY	San Pedro	4.746717	-6.660817

Now we do a unified diff between them:

.. code-block:: bash

 $ diff -u examples/*.txt
 --- examples/1.txt	2012-12-20 13:57:47.292866371 +0100
 +++ examples/2.txt	2012-12-20 12:31:58.828420437 +0100
 @@ -1,9 +1,8 @@
 -MLC	Mc Alester Regional Airport	34.882403	-95.783463
 -MLC	M Alester Regional Airport	34.882403	-95.783463
 -NDS	Sandstone Airport	-28	119.3
 -SPX	HOUSTON/TX/US:SPACELAND	29.52	-95.24
 +MLC	Mc Alester Regonal Airport	34.882403	-95.783463
 +NDS	Sandtone Airport	-28	119.4
  SPY	San Pedro	4.746717	-6.660817
  SPZ	Springdale Municipal Airport	36.18	-94.13
 -NDR	Nador	35.2	-2.917
 +NDR	Nador	35.3	-2.97
  SPP	Menongue Airport	-14.657583	17.719833
 +AAA	HOUSTON/TX/US:SPACELAND	29.52	-95.24
  NDU	Rundu Airport	-17.956461	19.719439

We want to annotate the differences in this diff to see which changes were:

+ a move (M)
+ a property change (P)
+ both (PM)
+ an addition (+)
+ a deletion (-)
+ no change (a space)

.. code-block:: bash

 $ diff -u examples/*.txt | tag_diff -
 -	-	SPX	HOUSTON/TX/US:SPACELAND	29.52	-95.24
 P	-	MLC	Mc Alester Regional Airport	34.882403	-95.783463
 P	+	MLC	Mc Alester Regonal Airport	34.882403	-95.783463
  	 	SPZ	Springdale Municipal Airport	36.18	-94.13
 +	+	AAA	HOUSTON/TX/US:SPACELAND	29.52	-95.24
  	 	SPY	San Pedro	4.746717	-6.660817
  	 	SPP	Menongue Airport	-14.657583	17.719833
 MP	-	NDS	Sandstone Airport	-28	119.3
 MP	+	NDS	Sandtone Airport	-28	119.4
 M	-	NDR	Nador	35.2	-2.917
 M	+	NDR	Nador	35.3	-2.97
  	 	NDU	Rundu Airport	-17.956461	19.719439

*tag_diff* has added a column in first position where we see the tags P, M, PM, +, -, etc...

Options
-------

You can customize:

+ the columns where *tag_diff* is looking for code and geocodes with *-i*. This takes 3 arguments which are column indexes: key, lat and lng. key is the column used as an id for each line. Default is 0 2 3.
+ the delimiter with *-d*. Default is tabulation.

Displaying annotated differences
--------------------------------

You may use `GeoBases <http://opentraveldata.github.io/geobases/>`_ to display the results like this (here we color using the column H0, the first column):

.. code-block:: bash

 $ diff -u examples/*.txt |tag_diff - |GeoBase -m -M _ _ H0

