import logging
import os
import pickle
from abc import ABCMeta, abstractmethod
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import List

import numpy as np
from elasticsearch import Elasticsearch

from core.config import settings


class RetrieverType(str, Enum):
    CUSTOM = "custom"
    ES = "elasticsearch"


class BaseRetriever(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def get_relevant_doc_bulk(self, query: str, topk: int) -> np.ndarray:
        pass


class CustomRetriever(BaseRetriever):
    task_name: str = "lyrics_retrieval"
    embed_name: str = "tfidf_embed.bin"
    encoder_name: str = "tfidf_encoder.bin"

    def __init__(self):
        super().__init__()
        current_dir = Path(__file__).parent
        asset_dir = os.path.join(current_dir, self.task_name)

        embed_path = os.path.join(asset_dir, self.embed_name)
        encoder_path = os.path.join(asset_dir, self.encoder_name)

        self.encoder = pickle.load(open(encoder_path, "rb"))
        self.embedding = pickle.load(open(embed_path, "rb"))

    async def get_relevant_doc_bulk(self, query: str, topk: int) -> np.ndarray:
        query_vec = self.encoder.transform([query])
        result = query_vec * self.embedding.T
        result = result.toarray()
        doc_indices = np.argsort(result[0])[::-1][:topk]
        return doc_indices


class ElasticSearchRetriever(BaseRetriever):
    es_server: Elasticsearch

    def __init__(self, es_host: str = "localhost", es_port: int = 9200):
        super().__init__()
        self.es_server = Elasticsearch(f"http://{es_host}:{es_port}")

    def _get_structured_query(self, user_input) -> dict:
        query = {"_source": False, "query": {"match": {"context": user_input}}}
        return query

    async def _request_search(self, index_name: str, query: dict, topk: int) -> List[int]:
        try:
            result = self.es_server.search(index=index_name, body=query, size=topk)
            doc_indices = list(hit["_id"] for hit in result["hits"]["hits"])
        except Exception as e:
            logging.error(str(e))
        return doc_indices

    async def get_relevant_doc_bulk(self, query: str, topk: int) -> np.ndarray:
        structured_query = self._get_structured_query(query)
        doc_indices = await self._request_search("lyrics", query=structured_query, topk=topk)
        return np.array(list(map(int, doc_indices)))


@lru_cache(maxsize=len(RetrieverType))
def get_retriever(type: RetrieverType) -> BaseRetriever:
    if type == RetrieverType.CUSTOM:
        return CustomRetriever()
    elif type == RetrieverType.ES:
        return ElasticSearchRetriever(es_host=settings.ES_HOST, es_port=settings.ES_PORT)
    raise NotImplementedError
