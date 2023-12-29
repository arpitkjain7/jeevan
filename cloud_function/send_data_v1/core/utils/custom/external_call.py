import requests
import json
import http.client


class APIInterface:
    @staticmethod
    def post(route, data=None, headers=None):
        try:
            url = route
            print("POST request sent")
            print(f"url = {url}, data = {data}")
            response = requests.post(url, json=data, headers=headers)
            # if response.status_code >= 400:
            #     raise Exception(
            #         f"Call to {route} failed with {response.status_code} and response {response.text}"
            #     )
            # print(f"response = {response}")
            print(
                f"response.text = {response.text}, response.status_code = {response.status_code}"
            )
            if response.text:
                return json.loads(response.text), response.status_code
            return None, response.status_code
        except Exception as error:
            print(f"Error in POST API request: {error}")
            raise error

    @staticmethod
    def get(route, params=None, data=None, headers=None):
        try:
            url = route
            print("GET request sent")
            print(f"{url=}, {params=},{data=}")
            response = requests.get(url, params=params, data=data, headers=headers)
            if response.status_code >= 400:
                raise Exception(
                    f"Call to {route} failed with {response.status_code} and response {response.text}"
                )
            return json.loads(response.text), response.status_code
        except Exception as error:
            print(f"Error in GET API request: {error}")

    @staticmethod
    def put(route, data=None, headers=None):
        try:
            url = route
            print("PUT request sent")
            print(f"url = {url}, data = {data}")
            response = requests.put(url, json=data, headers=headers)
            if response.status_code >= 400:
                raise Exception(
                    f"Call to {route} failed with {response.status_code} and response {response.text}"
                )
            return json.loads(response.text), response.status_code
        except Exception as error:
            print(f"Error in PUT API request: {error}")

    @staticmethod
    def delete(route, headers=None):
        try:
            url = route
            print("DELETE request sent")
            print(f"url = {url}")
            response = requests.delete(url, headers=headers)
            if response.status_code >= 400:
                raise Exception(
                    f"Call to {route} failed with {response.status_code} and response {response.text}"
                )
            return response.status_code
        except Exception as error:
            print(f"Error in DELETE API request: {error}")

    @staticmethod
    def get_bytes(route, params=None, data=None, headers=None):
        try:
            url = route
            print("get_bytes request sent")
            print(f"{url=}, {params=},{data=}")
            response = requests.get(url, params=params, data=data, headers=headers)
            return response.content, response.status_code
        except Exception as error:
            print(f"Error in get_bytes API request: {error}")

    @staticmethod
    def post_with_params(route, params=None, headers=None, data=None):
        try:
            url = route
            print("POST request sent")
            print(f"url = {url}, params = {params}")
            response = requests.post(url, json=data, params=params, headers=headers)
            print(
                f"response.text = {response.text}, response.status_code = {response.status_code}"
            )
            if response.text:
                return json.loads(response.text), response.status_code
            return None, response.status_code
        except Exception as error:
            print(f"Error in post_with_params request: {error}")
            raise error
