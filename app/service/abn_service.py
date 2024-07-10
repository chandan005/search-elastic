import os
from io import BytesIO
import zipfile
import time
import xml.etree.ElementTree as ET

import requests
from app.elastic import abn_elastic_service

DATA_FOLDER="app/resources/downloads"
INGEST_FOLDER="app/resources/ingests"

def download_and_unzip():
    file_urls = ["https://data.gov.au/data/dataset/5bd7fcab-e315-42cb-8daf-50b7efc2027e/resource/0ae4d427-6fa8-4d40-8e76-c6909b5a071b/download/public_split_11_20.zip", "https://data.gov.au/data/dataset/5bd7fcab-e315-42cb-8daf-50b7efc2027e/resource/635fcb95-7864-4509-9fa7-a62a6e32b62d/download/public_split_1_10.zip"]
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    for url in file_urls:
        response = requests.get(url)
        with zipfile.ZipFile(BytesIO(response.content)) as zipped:
            zipped.extractall(DATA_FOLDER)

def process_xml_v2(file_path):
    print("Preparing to process file:", file_path)
    records = []

    # Start parsing the XML file incrementally
    context = ET.iterparse(file_path, events=('start', 'end'))
    context = iter(context)
    _, root = next(context)  # Get the root element

    for event, elem in context:
        if event == 'end' and elem.tag == 'ABR':  # Adjust tag as per your XML structure
            try:
                abn_status = elem.find('ABN').attrib.get('status') if elem.find('ABN') is not None else None
                abn_status_from_date = elem.find('ABN').attrib.get('ABNStatusFromDate') if elem.find('ABN') is not None else None
                abn_value = elem.find('ABN').text if elem.find('ABN') is not None else None
                entity_type_ind = elem.find('EntityType/EntityTypeInd').text if elem.find('EntityType/EntityTypeInd') is not None else None
                entity_type_text = elem.find('EntityType/EntityTypeText').text if elem.find('EntityType/EntityTypeText') is not None else None
                non_ind_name_type = elem.find('MainEntity/NonIndividualName').attrib.get('type') if elem.find('MainEntity/NonIndividualName') is not None else None
                non_ind_name_text = elem.find('MainEntity/NonIndividualName/NonIndividualNameText').text if elem.find('MainEntity/NonIndividualName/NonIndividualNameText') is not None else None
                business_address_state = elem.find('MainEntity/BusinessAddress/AddressDetails/State').text if elem.find('MainEntity/BusinessAddress/AddressDetails/State') is not None else None
                business_address_postcode = elem.find('MainEntity/BusinessAddress/AddressDetails/Postcode').text if elem.find('MainEntity/BusinessAddress/AddressDetails/Postcode') is not None else None
                asic_type = elem.find('ASICNumber').attrib.get('ASICNumberType') if elem.find('ASICNumber') is not None else None
                asic_value = elem.find('ASICNumber').text if elem.find('ASICNumber') is not None else None
                gst_status = elem.find('GST').attrib.get('status') if elem.find('GST') is not None else None
                gst_status_from_date = elem.find('GST').attrib.get('GSTStatusFromDate') if elem.find('GST') is not None else None
                other_non_ind_name_type = elem.find('OtherEntity/NonIndividualName').attrib.get('type') if elem.find('OtherEntity/NonIndividualName') is not None else None
                other_non_ind_name_text = elem.find('OtherEntity/NonIndividualName/NonIndividualNameText').text if elem.find('OtherEntity/NonIndividualName/NonIndividualNameText') is not None else None

                # Create record dictionary
                record = {
                    'abn': {
                        'status': abn_status if abn_status is not None else None,
                        'statusFromDate': abn_status_from_date if abn_status_from_date is not None else None,
                        'value': abn_value if abn_value is not None else None
                    },
                    'entityType': {
                        'type': entity_type_ind if entity_type_ind is not None else None,
                        'value': entity_type_text if entity_type_text is not None else None
                    },
                    'mainEntity': {
                        'nonIndividualName': {
                            'type': non_ind_name_type if non_ind_name_type is not None else None,
                            'value': non_ind_name_text if non_ind_name_text is not None else None
                        },
                        'businessAddress': {
                            'state': business_address_state if business_address_state is not None else None,
                            'postCode': business_address_postcode if business_address_postcode is not None else None
                        }
                    },
                    'asic': {
                        'type': asic_type if asic_type is not None else None,
                        'value': asic_value if asic_value is not None else None
                    },
                    'gst': {
                        'status': gst_status if gst_status is not None else None,
                        'statusFromDate': gst_status_from_date if gst_status_from_date is not None else None
                    },
                    'otherEntity': {
                        'nonIndividualName': {
                            'type': other_non_ind_name_type if other_non_ind_name_type is not None else None,
                            'value': other_non_ind_name_text if other_non_ind_name_text is not None else None
                        }
                    }
                }

                records.append(record)
            except Exception as e:
                print('Exception processing XML:', e)
            finally:
                # Clear the element to free memory
                root.clear()

    print('Parsing XML to JSON completed.')
    return records

def download_all_and_ingest():
    try:
        start_time = time.time()
        download_and_unzip()
        for file_name in os.listdir(DATA_FOLDER):
            print("Processing records for file: ", file_name)
            if file_name.endswith('.xml'):
                file_path = os.path.join(DATA_FOLDER, file_name)
                records = process_xml_v2(file_path)
                print('Records count', len(records))
                if len(records) > 0:
                    print('checking / creating Index')
                    abn_elastic_service.create_abn_index()
                    print('Ingesting data.')
                    abn_elastic_service.ingest_data(data=records)
                else:
                    print('No records found after parsing xml.')
    except Exception as e:
        print(e)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Process completed in {elapsed_time:.2f} seconds")

def ingest_one():
    try:
        start_time = time.time()
        for file_name in os.listdir(INGEST_FOLDER):
            print("Processing records for file: ", file_name)
            if file_name.endswith('.xml'):
                file_path = os.path.join(INGEST_FOLDER, file_name)
                records = process_xml_v2(file_path)
                print('Records count', len(records))
                if len(records) > 0:
                    print('checking / creating Index')
                    abn_elastic_service.create_abn_index()
                    print('Ingesting data.')
                    abn_elastic_service.ingest_data(data=records)
                else:
                    print('No records found after parsing xml.')
    except Exception as e:
        print(e)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Process completed in {elapsed_time:.2f} seconds")
