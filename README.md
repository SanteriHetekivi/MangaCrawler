# MangaCrawler

**Simple crawler for finding new chapters to read.**

1. Reads mangalist file for supported list site.  
1. Finds all of the mangas that has 5 or more new chapters from supported manga sites.  
3. Outputs .csv file with all of the needed data.  

## Installing and usage

### Installing
1. Install ```python3``` and ```pip```.
1. Install with pip or Build from source.
    * Install with pip:
        * ```pip install MangaCrawler```
    * Build from source:
        * ```git clone https://github.com/SanteriHetekivi/MangaCrawler.git```
        * ```cd MangaCrawler/```
        * ```python setup.py install```

### Usage
1. Run the program with arguments
    * For example: ```MangaCrawler -f new -s mangafox -v -c 5 -m manga.xml```
1. Will output result to CSV file. (**HTML output is under development**)

#### Arguments
| Short | Long   | Description |
| ----- | ------ |  ---------- |
| -v    |        |  Print verbose status messages. |
| -h    | --help |  Print Help message. |
| -f    | --find |  Manga find mode to use. (new or updated) (```-f updated```) |
| -s    | --site |  Manga site to use. (```-s mangafox```) |
| -c    | --min-chapters |  Minimum amount of new chapters that manga has to have before it gets to output csv. (```-c 5```) |
| -m    | --manga-xml-file |  MyAnimeList mangalist xml file. (```-m manga.xml```) **If NOT given and current directory has XML files, program gives a opportunity to choose from them.** |
| -a    | --azure-account-key | API key for [Bing Web Search API](https://www.microsoft.com/cognitive-services/en-us/bing-web-search-api). |
| -o    | --output-file | File to put output on. **If NOT given will make file to current directory.**|

## Deployment information

### Deploying
1. Install ```python3``` and ```pip```
2. Run command to build dependencies.  
    ``` pip install -r requirements.txt ```
4. Run the program
    * With output  
    ```python manga-crawler.py -f updated -s mangafox -v```
    * Without output  
    ```python manga-crawler.py -f updated -s mangafox```

## Support and licenses

### Supported List Sites  
* [MyAnimeList](https://myanimelist.net/)

### Supported Manga Sites   
* [Manga Fox](http://mangafox.me/)

### Credits and license

* Made by [Santeri Hetekivi](https://github.com/SanteriHetekivi), for his personal needs.
* This code is licensed under [Apache License 2.0](https://raw.githubusercontent.com/SanteriHetekivi/MangaCrawler/master/LICENSE).
