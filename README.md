# es-indexer
[![PyPI version](https://badge.fury.io/py/es-indexer.svg)](https://badge.fury.io/py/es-indexer)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
![Linux](https://img.shields.io/badge/Supports-Linux-green.svg)
![macOS](https://img.shields.io/badge/Supports-macOS-green.svg)
![windows](https://img.shields.io/badge/Supports-windows-green.svg)

**es-indexer** (Elasticsearch Indexer) is a simple concurrent command line tool written in Python to help you quickly populate some json data into Elasticsearch. <br><br>

## About

Usually you'll have to use a third-party software or a client library to index data to Elasticsearch and setting that up can be really time consuming and tiresome (*cough*_logstash_*cough*). **es-indexer** helps in indexing raw contents of `*.json` documents quickly with the help of multi-threading. <br><br>

**es-indexer** currently doesn't provide any syncing of the data, you'll have to reindex the data if it changes, but will always populate a new index and then create an alias, the old data will be present while re-indexing until the new index is fully populated. A future update might include syncing. <br>

Since Elasticsearch exposes a REST-API on Port 9200, there's no need for es-indexer providing a REST-API itself.

## Installation

> Requires Python 3.x and is compatible with Elasticsearch 7.x.x.

* es-indexer can be installed with the help of pip.
  ```
  $ pip install es-indexer
  ```
**(OR)**

* Clone the repository.
  ```
  $ git clone https://github.com/itsron717/es-indexer.git
  ```

* Move inside the repo.
  ```
  $ cd es-indexer
  ```

* Install the package locally.
  ```
  $ pip install .
  ```

## Usage
### Config
You need to create a `config.yml` before running es-indexer:

    host: http://127.0.0.1:9200
    index: twitter-example
    type: documents
    mapping:
        settings:
            number_of_shards: 1
            number_of_replicas: 0
            
You can provide a custom mapping in the config file, es-indexer will convert the yaml mapping 1:1 to json.
```
$ es-indexer --config path/to/config/file --source path/to/json/folder
```

## Adding more Data Sources
More data sources other than `json` such as `SQL`, `Filesystem`, etc are also to be added to the es-indexer tool such that it can be a one stop shop for all the indexing needs of Elasticsearch. Anybody who'd like to contribute in integrating other data sources can raise and issue and we can start working on it!. 

## To-Do
- [x] Add `json` support.
- [ ] Add `SQL` data source integration.
- [ ] Add `FileSystem` data source integration.
- [ ] Increase the speed of indexing.
- [ ] Add tests.

## References

es-indexer was built using the insipiration of [this](https://github.com/arkste/elsi) amazing tool written in Go.

## License
 
The MIT License (MIT)

Copyright (c) 2019 [Rounak Vyas](https://www.linkedin.com/in/itsron143/)
