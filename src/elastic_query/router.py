
from fastapi import APIRouter, status
from src.elastic import elastic_client


router = APIRouter(
    prefix="/elasticsearch",
    tags=["Elasticsearch"]
)


def answer_transformation(result):
    elastic_answer = []
    for el in result:
        elastic_answer.append({
            'result': el['_source']['result'],
            'ip': el['_source']['ip'],
            'login': el['_source']['login'],
            'password': el['_source']['password'],
        })

    return elastic_answer


@router.get("/get_elastic_data")
async def get_elastic_data():
    try:
        search_results = elastic_client.search(
            index='results',
            query={
                "match_all": {}
            },
        )
        hits = search_results['hits']['hits']
        return {"status": status.HTTP_200_OK, "result": answer_transformation(hits)}
    except Exception as e:
        return {f"warning: {e}"}
