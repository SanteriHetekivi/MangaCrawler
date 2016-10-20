# MangaCrawler

**Simple crawler for finding new chapters to read.**

1. Reads mangalist file for supported list site from data directory.  
1. Finds all of the mangas that has 5 or more new chapters from supported manga sites.  
3. Outputs .csv file with all of the needed data.  

## Deployment information

### Deploying
1. Install ```python3``` and ```pip```
2. Run command to build dependencies.  
    ``` pip install -r requirements.txt ```
3. Make config.ini file that has all fields filled from [config.ini.example](https://raw.githubusercontent.com/SanteriHetekivi/MangaCrawler/master/config.ini.example) file.
3. Add myanimelist mangalist xml file to data directory.  
    * Export your mangalist from [MyAnimeList](https://myanimelist.net/panel.php?go=export).
    * Decompress the .gz file  
        ```unzip -d mangalist.xml.gz```
    * Copy/Move mangalist.xml file to projects data directory.
4. Run the program  
    * With output  
    ```python manga-crawler.py -f updated -s mangafox -v```
    * Without output  
    ```python manga-crawler.py -f updated -s mangafox```

### Keys from config.ini descriptions
| Name              | Description   |
| ----------------- | ------------- |
| azure_account_key | Account key for azure that has [Bing Search API](https://datamarket.azure.com/dataset/5BA839F1-12CE-4CCE-BF57-A49D98D29A44) access. |

### Start parameters  
| Short | Long   | Description |
| ----- | ------ |  ---------- |
| -v    |        |  Print verbose status messages. |
| -h    | --help |  Print Help message. |
| -f    | --find |  Manga find mode to use (new or updated (-f updated)). |
| -s    | --site |  Manga site to use (-s mangafox). |
| -c    | --min_chapters |  Minimum amount of new chapters that manga has to have before it gets to output csv. (-c 5) |

## Support and licenses

### Supported List Sites  
* [MyAnimeList](https://myanimelist.net/)

### Supported Manga Sites   
* [Manga Fox](http://mangafox.me/)

### Credits and license

* Made by [Santeri Hetekivi](https://github.com/SanteriHetekivi), for his personal needs.
* This code is licensed under [Apache License 2.0](https://raw.githubusercontent.com/SanteriHetekivi/MangaCrawler/master/LICENSE).
