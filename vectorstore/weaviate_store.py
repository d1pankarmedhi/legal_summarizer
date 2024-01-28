import weaviate
import uuid
from utils.env_util import EnvironmentVariables

class WeaviateStore:
    def __init__(self) -> None:

        self.api_key = EnvironmentVariables.WEAVIATE_API_KEY
        self.api_key = EnvironmentVariables.WEAVIATE_URL
        self.client = weaviate.Client(
            auth_client_secret=weaviate.AuthApiKey(self.api_key),
            url=self.url,
        )

    def generate_class_name(self, class_name: str = None):
        id = uuid.uuid4()
        name = "Class_"
        if class_name is None:
            name = "Class_" + str(id.int)
        else:
            name += class_name
        return name



    def create_class_obj(self, class_name: str):
        try:
            properties = [
                {
                    "name": "content",
                    "dataType": ["text"],
                },
                {
                    "name": "tag",
                    "dataType": ["text"],
                },
            ]
            class_obj = {
                "class": class_name,
                "properties": properties,
            }
            self.client.schema.create_class(class_obj)
        except Exception as e:
            print(e)

    def add_documents(self, class_name: str, tagged_documents: list):
        try:
            data_objs = []
            for i, d in enumerate(tagged_documents):
                for doc in d["documents"]:
                    data_objs.append(
                        {
                            "content": doc.page_content,
                            "tag": d["heading"],
                        },
                    )

            self.client.batch.configure(batch_size=100)
            with self.client.batch as batch:
                for data_obj in data_objs:
                    batch.add_data_object(data_obj, class_name)

        except Exception as e:
            print(e)


    def bm25_search_weaviate(self, query: str, class_name: str) -> list:
        result = []
        response = (
            self.client.query.get(class_name, ["content", "tag"])
            .with_bm25(
                query=query,
            )
            .with_limit(4)
            .do()
        )
        for content in response["data"]["Get"][class_name]:
            result.append(content["content"])

        return result
    


    def delete_class(self, class_name: str):
        try:
            self.client.schema.delete_class(class_name)
        except Exception as e:
            print(e)