import yaml
import json
import click
import os
import concurrent.futures
from elasticsearch import Elasticsearch


files_indexed = 0
total_exceptions = 0


@click.command()
@click.option("--config", help="Path to the YAML config file.")
@click.option("--source", help="Path to the source folder containing json files.")
def main(config, source):
    with open(config) as f:
        config_dict = yaml.safe_load(f)
    INDEX_NAME = config_dict["index"]
    DOC_NAME = config_dict["type"]
    mappings_dict = config_dict["mapping"]
    spin_this_up(INDEX_NAME, DOC_NAME, mappings_dict, source)


def index_data(INDEX_NAME, DOC_NAME, es, filename):
        # Do let me know if there's a better way to handle globals without oops
    global files_indexed
    global total_exceptions
    if filename.name.endswith('.json'):
        try:
            with open(filename) as open_file:
                es.index(index=INDEX_NAME, doc_type=DOC_NAME,
                         body=json.load(open_file))
            files_indexed += 1
            return "{0} Files(s) indexed successfully - {1}".format(files_indexed, filename.name)
        except Exception as exc:
            total_exceptions += 1
            return "Inner Exception in file - {0} - Exception - {1}".format(filename.name, exc)


def spin_this_up(INDEX_NAME, DOC_NAME, mappings_dict, source):
    es = Elasticsearch()
    if es.indices.exists(INDEX_NAME) == False:
        es.indices.create(index=INDEX_NAME, body=dict(mappings_dict))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        check_indexed = {executor.submit(
            index_data, INDEX_NAME, DOC_NAME, es, filename): filename for filename in os.scandir(source)}
        for future in concurrent.futures.as_completed(check_indexed):
            data = check_indexed[future]
            try:
                data = future.result()
            except Exception as exc:
                total_exceptions += 1
                print(
                    "Total exceptions - {0} - {1}".format(total_exceptions, exc))
            else:
                print(data)
