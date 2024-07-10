import warnings

from elasticsearch import Elasticsearch
import elasticsearch.helpers
from elasticsearch.exceptions import ElasticsearchWarning


warnings.filterwarnings('ignore', category=ElasticsearchWarning)

es = Elasticsearch(['http://localhost:9200'])

INDEX_NAME = 'abn'

SEARCH_TEMPLATES = {
    "wildcard_search_template": {
        "script": {
            "lang": "mustache",
            "source": {
                "query": {
                    "wildcard": {
                        "{{ field }}": {
                            "value": "{{ value }}"
                        }
                    }
                }
            }
        }
    },
    "range_query_template": {
        "script": {
            "lang": "mustache",
            "source": {
                "query": {
                    "range": {
                        "{{ field }}": {
                            "gte": "{{ min_value }}",
                            "lte": "{{ max_value }}"
                        }
                    }
                }
            }
        }
    },
    "exact_match_template": {
        "script": {
            "lang": "mustache",
            "source": {
                "query": {
                    "match": {
                        "{{ field }}": {
                            "query": "{{ value }}",
                            "operator": "and",
                            "boost": 1.0
                        }
                    }
                }
            }
        }
    },
    "fuzzy_proximity_template": {
        "script": {
            "lang": "mustache",
            "source": {
                "query": {
                    "match": {
                        "{{ field }}": {
                            "query": "{{ value }}",
                            "fuzziness": "{{ fuzziness }}",
                            "operator": "or",
                            "boost": 1.0
                        }
                    }
                }
            }
        }
    },
    "phrase_proximity_template": {
        "script": {
            "lang": "mustache",
            "source": {
                "query": {
                    "match_phrase": {
                        "{{ field }}": {
                            "query": "{{ value }}",
                            "slop": "{{ slop }}",
                            "boost": 1.0
                        }
                    }
                }
            }
        }
    },
    "multi_match_boost_template" : {
        "script": {
            "lang": "mustache",
            "source": {
                "query": {
                    "multi_match": {
                        "query": "{{ query_string }}",
                        "fields": ["{{ field1 }}", "{{ field2 }}"],
                        "type": "best_fields",
                        "tie_breaker": 0.3,
                        "boost": 1.0
                    }
                }
            }
        }
    }
}

def create_abn_index():
    index_definition = {
        "settings": {
            "number_of_shards": 3,
            "number_of_replicas": 0,
            "refresh_interval" : -1,
            "analysis": {
                "analyzer": "standard"
            }
        }
    }

    try:
        # Check if the index is created successfully
        if es.indices.exists(index=INDEX_NAME):
            print(f"Index already exists. '{INDEX_NAME}'.")
        else:
            es.indices.create(index=INDEX_NAME, settings=index_definition['settings'])
            register_search_templates()
            print(f"Index '{INDEX_NAME}' created successfully.")
    except Exception as e:
        print('Exception creating index', e)


def register_search_templates():
    for template_name, template_body in SEARCH_TEMPLATES.items():
        es.put_script(id=template_name, script=template_body)
        print(f"Registered template '{template_name}'")

def get_data(data):
    return data

def ingest_data(data):
    try:
        parallel = True

        if parallel:
            for success, error in elasticsearch.helpers.parallel_bulk(client=es, actions=get_data(data), thread_count=4,index=INDEX_NAME):
                if not success:
                    print('Failed')
                    print(error)
            print('Records Inserted')
        else:
            elasticsearch.helpers.bulk(client=es,index=INDEX_NAME,actions=get_data(data))
    except Exception as e:
        print('Exception bulk inserting', e)
