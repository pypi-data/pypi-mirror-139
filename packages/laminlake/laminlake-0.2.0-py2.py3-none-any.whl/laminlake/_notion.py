import requests
import json


def insert(database_id, name):
    dict = {
        "parent": {
            "database_id": database_id,
        },
        "properties": {"name": {"title": [{"text": {"content": name}}]}},
    }
    return json.dumps(dict)


class Database:
    # The implementation is based on the following two links
    # * https://developers.notion.com/docs/getting-started
    # * https://developers.notion.com/docs/working-with-databases

    def __init__(self, database_id):
        try:  # env variable fails in Jupyter notebooks
            from ._secrets import NOTION_API_KEY
        except ImportError:
            raise RuntimeError("Please run: laminlake configure")

        self._base_url = "https://api.notion.com/v1/pages"
        self._headers = {
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2021-08-16",
        }
        self._database_id = database_id

    def __getitem__(self, row_id):
        response = requests.get(f"{self._base_url}/{row_id}", headers=self._headers)
        return response.json()

    def insert(self, name):
        data = insert(self._database_id, name)
        response = requests.post(self._base_url, headers=self._headers, data=data)
        return response.json()


class Dataset(Database):
    def __init__(self):
        super().__init__(database_id="4499c79c6e9141c8bbdcb251a24d901a")
