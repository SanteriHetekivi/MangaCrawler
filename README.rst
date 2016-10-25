MangaCrawler
============

**Simple crawler for finding new chapters to read.**

#. Reads mangalist file for supported list site.
#. Finds all of the mangas that has 5 or more new chapters from
   supported manga sites.
#. Outputs .csv file with all of the needed data.

Installing and usage
--------------------

Installing
~~~~~~~~~~

#. Install ``python3`` and ``pip``.
#. Install with pip or Build from source.

   -  Install with pip:

      -  ``pip install MangaCrawler``

   -  Build from source:

      -  ``git clone https://github.com/SanteriHetekivi/MangaCrawler.git``
      -  ``cd MangaCrawler/``
      -  ``python setup.py install``

Usage
~~~~~

#. Run the program with arguments

   -  For example:
      ``MangaCrawler -f new -s mangafox -v -c 5 -m manga.xml``

#. Will output result to CSV file. (**HTML output is under
   development**)

Arguments
^^^^^^^^^

+-------+--------+-----------+
| Short | Long   | Descripti |
|       |        | on        |
+=======+========+===========+
| -v    |        | Print     |
|       |        | verbose   |
|       |        | status    |
|       |        | messages. |
+-------+--------+-----------+
| -h    | –help  | Print     |
|       |        | Help      |
|       |        | message.  |
+-------+--------+-----------+
| -f    | –find  | Manga     |
|       |        | find mode |
|       |        | to use.   |
|       |        | (new or   |
|       |        | updated)  |
|       |        | (``-f upd |
|       |        | ated``)   |
+-------+--------+-----------+
| -s    | –site  | Manga     |
|       |        | site to   |
|       |        | use.      |
|       |        | (``-s man |
|       |        | gafox``)  |
+-------+--------+-----------+
| -c    | –min-c | Minimum   |
|       | hapter | amount of |
|       | s      | new       |
|       |        | chapters  |
|       |        | that      |
|       |        | manga has |
|       |        | to have   |
|       |        | before it |
|       |        | gets to   |
|       |        | output    |
|       |        | csv.      |
|       |        | (``-c 5`` |
|       |        | )         |
+-------+--------+-----------+
| -m    | –manga | MyAnimeLi |
|       | -xml-f | st        |
|       | ile    | mangalist |
|       |        | xml file. |
|       |        | (``-m man |
|       |        | ga.xml``) |
|       |        | **If NOT  |
|       |        | given and |
|       |        | current   |
|       |        | directory |
|       |        | has XML   |
|       |        | files,    |
|       |        | program   |
|       |        | gives a   |
|       |        | opportuni |
|       |        | ty        |
|       |        | to choose |
|       |        | from      |
|       |        | them.**   |
+-------+--------+-----------+
| -a    | –azure | Account   |
|       | -accou | key for   |
|       | nt-key | azure     |
|       |        | that has  |
|       |        | `Bing     |
|       |        | Search    |
|       |        | API`_     |
|       |        | access.   |
+-------+--------+-----------+
| -o    | –outpu | File to   |
|       | t-file | put       |
|       |        | output    |
|       |        | on. **If  |
|       |        | NOT given |
|       |        | will make |
|       |        | file to   |
|       |        | current   |
|       |        | directory |
|       |        | .**       |
+-------+--------+-----------+

Deployment information
----------------------

Deploying
~~~~~~~~~

#. Install ``python3`` and ``pip``
#. Run command to build dependencies.
   ``pip install -r requirements.txt``
#. Run the program

   -  With output
      ``python manga-crawler.py -f updated -s mangafox -v``
   -  Without output
      ``python manga-crawler.py -f updated -s mangafox``

Support and licenses
--------------------

Supported List Sites
~~~~~~~~~~~~~~~~~~~~

-  `MyAnimeList`_

Supported Manga Sites
~~~~~~~~~~~~~~~~~~~~~

-  `Manga Fox`_

Credits and license
~~~~~~~~~~~~~~~~~~~

-  Made by `Santeri Hetekivi`_, for his personal needs.
-  This code is licensed under `Apache License 2.0`_.

.. _Bing Search API: https://datamarket.azure.com/dataset/5BA839F1-12CE-4CCE-BF57-A49D98D29A44
.. _MyAnimeList: https://myanimelist.net/
.. _Manga Fox: http://mangafox.me/
.. _Santeri Hetekivi: https://github.com/SanteriHetekivi
.. _Apache License 2.0: https://raw.githubusercontent.com/SanteriHetekivi/MangaCrawler/master/LICENSE