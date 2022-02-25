import os
import pickle
from enum import Enum
from functools import lru_cache
from pathlib import Path

import numpy as np


class RetrieverType(str, Enum):
    CUSTOM = "custom"


class BaseRetriever:
    def __init__(self):
        pass

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


@lru_cache(maxsize=len(RetrieverType))
def get_retriever(type: RetrieverType) -> BaseRetriever:
    if type == RetrieverType.CUSTOM:
        return CustomRetriever()
    raise NotImplementedError


# class ElasticSearchRetriever(BaseRetriever):
#     es_obj: Elasticsearch
#
#     def __init__(self, es_host: str="localhost", es_port: int = 9200):
#         super().__init__()
#         self.es_obj = Elasticsearch(f"http://{es_host}:{es_port}")
#
#     def get_relevant_doc_bulk(self, query: str, topk: int) -> np.typing.NDArray:
#         query = {
#             'query': {
#                 'match': {
#                     'document_text': query
#                 }
#             }
#         }
#         res = self.es_obj.search(index=index_name, body=query, size=topk)
