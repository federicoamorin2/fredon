from src.rerank.run import rerank_prompt
from src.rerank.model import MonoT5
from src.opensearch import get_passages_from_index, get_adjacent_passages_from_index, Handler
from src.event_ import RagEvent

print("Carregando modelo...")
RERANKER =  MonoT5('artifacts/ptt5-base-en-pt-msmarco-100k-v2')
OPENSEARCH_HANDLER = Handler()

def handler(event, context):
    rag_event = RagEvent.from_event(event)
    print(f"Evento recebido: {rag_event}")
    # Here's our query:
    OPENSEARCH_HANDLER.index = rag_event.index
    passages = get_passages_from_index(
        rag_event.query, OPENSEARCH_HANDLER, rag_event.filters, rag_event.top_k_passages
    )
    if rag_event.has_min_score:
        passages = passages.filter_by_score(rag_event.min_score)

    if rag_event.has_get_adjacent_passages:
       passages = get_adjacent_passages_from_index(passages, OPENSEARCH_HANDLER) 

    if rag_event.has_rerank:
        passages = rerank_prompt(
            rag_event.query,
            passages,
            rag_event.rerank_config,
            RERANKER,
        )
    return {
        "body": {"ragPrompt": passages.build_prompt()},
        "statusCode": 200
    }
