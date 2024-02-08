from fastapi import APIRouter, HTTPException, status
from src.elastic import elastic_client

router = APIRouter(
    prefix="/elasticsearch",
    tags=["Elasticsearch"]
)


def answer_transformation(result):
    elastic_answer = []
    for el in result:
        elastic_answer.append({
            'title_en': el['_source']['title_en'],
            'title_ru': el['_source']['title_ru'],
            'href': el['_source']['href'],
            'date': el['_source']['date'],
            'image': f"http://localhost:8000/photos/{el['_source']['image']}",
            'country': el['_source']['country'],
            'city': el['_source']['city'],
            'relevant_score': el['_score'],
        })

    return elastic_answer


@router.get("/get_elastic_data")
async def get_elastic_data():
    search_results = await elastic_client.search(
        index='news',
        query={
            "match_all": {}
        },
    )
    hits = search_results['hits']['hits']
    return {"status": status.HTTP_200_OK, "result": answer_transformation(hits)}


@router.post("/search")
async def search_by_title(message: str):
    try:
        search_params_en = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "title_en": {
                                    "query": message,
                                    "operator": "and",
                                    "fuzziness": 'AUTO'
                                }
                            }
                        }
                    ]
                }
            }
        }

        search_results_en = await elastic_client.search(index='news', body=search_params_en)

        search_params_ru = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "title_ru": {
                                    "query": message,
                                    "operator": "and",
                                    "fuzziness": 'AUTO'
                                }
                            }
                        }
                    ]
                }
            }
        }

        search_results_ru = await elastic_client.search(index='news', body=search_params_ru)

        hits_en = search_results_en['hits']['hits']
        hits_ru = search_results_ru['hits']['hits']

        combined_results = hits_en + hits_ru

        return {"results": answer_transformation(combined_results), "status": status.HTTP_200_OK}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @router.post("/search_by_date")
# async def search_by_title_and_date(search: InputUserMessageDate):
#     try:
#         search_params_en = {
#             "query": {
#                 "bool": {
#                     "must": [
#                         {
#                             "match": {
#                                 "title_en": {
#                                     "query": search.message,
#                                     "operator": "and",
#                                     "fuzziness": 'AUTO'
#                                 }
#                             }
#                         },
#                         {
#                             "range": {
#                                 "date": {
#                                     "gte": search.begin,
#                                     "lte": search.end
#                                 }
#                             }
#                         }
#                     ]
#                 }
#             }
#         }

#         search_results_en = await elastic_client.search(index='news', body=search_params_en)

#         search_params_ru = {
#             "query": {
#                 "bool": {
#                     "must": [
#                         {
#                             "match": {
#                                 "title_ru": {
#                                     "query": search.message,
#                                     "operator": "and",
#                                     "fuzziness": 'AUTO'
#                                 }
#                             }
#                         },
#                         {
#                             "range": {
#                                 "date": {
#                                     "gte": search.begin,
#                                     "lte": search.end
#                                 }
#                             }
#                         }
#                     ]
#                 }
#             }
#         }

#         search_results_ru = await elastic_client.search(index='news', body=search_params_ru)

#         hits_en = search_results_en['hits']['hits']
#         hits_ru = search_results_ru['hits']['hits']

#         combined_results = hits_en + hits_ru

#         return {"results": answer_transformation(combined_results), "status": status.HTTP_200_OK}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
