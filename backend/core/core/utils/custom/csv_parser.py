import pandas as pd
import json
from core.crud.algorithm_crud import CRUDAlgorithms
from core.crud.cloud_service_crud import CRUDCloudService


def algorithm_parser(file_path):
    file_data = pd.read_csv(file_path)
    all_data = []
    for _, data in file_data.iterrows():
        row_data = data.to_list()
        id = row_data[0]
        name = row_data[1]
        complex_score = row_data[2]
        row_dict = {
            "name": name,
            "complexity_score": complex_score,
        }
        all_data.append(row_dict)
    return all_data


def cloud_services_parser(file_path: str):
    file_data = pd.read_csv(file_path)
    all_data = []
    for _, data in file_data.iterrows():
        row_data = data.to_list()
        id = row_data[0]
        name = row_data[1]
        cloud_provider = row_data[2]
        complex_score = row_data[3]
        row_dict = {
            "name": name,
            "cloud_provider": cloud_provider,
            "complexity_score": complex_score,
        }
        all_data.append(row_dict)
    return all_data


def pricing_parser(file_path: str):
    file_data = pd.read_csv(file_path)
    all_data = []
    for _, data in file_data.iterrows():
        row_data = data.to_list()
        id = row_data[0]
        uom = row_data[1]
        cost = row_data[2]
        calculator = row_data[3]
        example = row_data[4]
        cognitive_service = row_data[5]
        row_dict = {
            "id": id,
            "cognitive_service": cognitive_service,
            "uom": uom,
            "cost": cost,
            "calculator": calculator,
            "example": example,
        }
        all_data.append(row_dict)
    return all_data


def service_catalog_parser(file_path: str):
    file_data = pd.read_csv(file_path)
    all_data = []
    for _, data in file_data.iterrows():
        row_data = data.to_list()
        catalog_id = row_data[0]
        technical_use_case_id = row_data[1]
        algorith_name = row_data[2]
        algorithm_id = (
            CRUDAlgorithms().read_by_name(algorithm_name=algorith_name).get("id")
        )
        cloud_service_name = row_data[3]
        cloud_service_id = (
            CRUDCloudService()
            .read_by_service_name(service_name=cloud_service_name)
            .get("id")
        )
        pricing_id = row_data[4]
        complexity_score = row_data[5]
        service_metadata = json.loads(row_data[6])
        row_dict = {
            "id": catalog_id,
            "technical_use_case_id": technical_use_case_id,
            "algorithm_id": algorithm_id,
            "cloud_service_id": cloud_service_id,
            "complexity_score": complexity_score,
            "pricing_id": pricing_id,
            "service_metadata": service_metadata,
        }
        all_data.append(row_dict)
    print(all_data)
    return all_data
