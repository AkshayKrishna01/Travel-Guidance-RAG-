import os
import json
import boto3
from typing import List, Tuple
from llama_index.core import Document
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.node_parser import SemanticSplitterNodeParser


class EmbeddedModelConnectionError(Exception):
    pass


class EmbeddedModel(BaseEmbedding):
    def __init__(self):
        super().__init__()
        self._client = boto3.client(
            "bedrock-runtime",
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        self._model_id = os.getenv("EMBEDDING_MODEL_Id")

    def _get_query_embedding(self, query: str) -> List[float]:
        return self._get_text_embedding(query)

    def _get_text_embedding(self, text: str) -> List[float]:
        try:
            res = self._client.invoke_model(
                modelId=self._model_id,
                body=json.dumps({"inputText": text}),
            )
            out = json.loads(res["body"].read())
            return out["embedding"]
        except Exception as e:
            raise EmbeddedModelConnectionError(str(e)) from e

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        return [self._get_text_embedding(t) for t in texts]


    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)

    async def _aget_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding(text)

    async def _aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        return [self._get_text_embedding(t) for t in texts]

    def health_check(self) -> bool:
        try:
            _ = self._get_text_embedding("ping")
            return True
        except Exception:
            return False

    def split_into_chunks_from_text(self, text: str):
        doc = Document(text=text)
        splitter = SemanticSplitterNodeParser(
            buffer_size=1,
            breakpoint_percentile_threshold=30,
            embed_model=self,
        )
        nodes = splitter.get_nodes_from_documents([doc])
        return nodes

    def generate_embeddings(self, nodes) -> List[Tuple[str, list]]:
        results: List[Tuple[str, list]] = []
        for node in nodes:
            content = node.get_content()
            emb = node.embedding if getattr(node, "embedding", None) else self._get_text_embedding(content)
            results.append((content, emb))
        return results