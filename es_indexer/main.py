import yaml
import json
import click
import os
import logging
from concurrent.futures import ThreadPoolExecutor
from elasticsearch import Elasticsearch
from threading import Lock

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Indexer:
    def __init__(self):
        self.files_indexed = 0
        self.total_exceptions = 0
        self.lock = Lock()

    def index_data(self, index_name, es, filepath):
        try:
            with open(filepath, encoding='utf-8') as file:
                es.index(index=index_name, body=json.load(file))
            with self.lock:
                self.files_indexed += 1
            return f"File indexed successfully: {filepath}"
        except Exception as exc:
            with self.lock:
                self.total_exceptions += 1
            logger.error(f"Error indexing file {filepath}: {exc}")
            return None

    def create_index_and_index_files(self, index_name, mappings, source_path, es_host, max_workers=8):
        es = Elasticsearch([es_host])
        if not es.indices.exists(index=index_name):
            es.indices.create(index=index_name, body={"mappings": mappings})
            logger.info(f"Index {index_name} created successfully.")

        json_files = [entry for entry in os.scandir(
            source_path) if entry.is_file() and entry.name.endswith('.json')]
        if not json_files:
            raise ValueError(
                f"No JSON files found in the source directory: {source_path}")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(
                self.index_data, index_name, es, entry.path): entry.path for entry in json_files}
            for future in futures:
                try:
                    result = future.result()
                    if result:
                        logger.info(result)
                except Exception as exc:
                    logger.error(f"Unexpected error: {exc}")


@click.command()
@click.option("--config", required=True, help="Path to the YAML config file.")
@click.option("--source", required=True, help="Path to the folder containing JSON files.")
@click.option("--es_host", default="http://localhost:9200", help="Elasticsearch host URL.")
def main(config, source, es_host):
    if not os.path.exists(config):
        raise FileNotFoundError(f"Config file {config} does not exist.")
    if not os.path.isdir(source):
        raise NotADirectoryError(f"Source path {source} is not a directory.")

    with open(config) as f:
        config_data = yaml.safe_load(f)

    index_name = config_data.get("index")
    mappings = config_data.get("mapping", {})

    if not index_name:
        raise ValueError("Index name not specified in the config.")

    indexer = Indexer()
    indexer.create_index_and_index_files(index_name, mappings, source, es_host)
