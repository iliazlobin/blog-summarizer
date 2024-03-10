import json
import os

from .azure_blog import (
    check_document_exist,
    extract_insights,
    retrieve_scraped_data,
    upsert_document,
)

current_directory = os.path.dirname(os.path.abspath(__file__))
test_directory = os.path.join(current_directory, "test_data")

if __name__ == "__main__":
    with open(os.path.join(test_directory, "apify_payload.json"), "r") as file:
        apify_payload_json = file.read()
    apify_payload = json.loads(apify_payload_json)

    dataset_items = retrieve_scraped_data(apify_payload, None)
    with open(os.path.join(test_directory, "dataset_items.json"), "w") as f:
        json.dump(dataset_items, f, indent=4)

    # with open(os.path.join(test_directory, "dataset_items.json"), "r") as file:
    #     dataset_items_json = file.read()
    # dataset_items = json.loads(dataset_items_json)
    # first_database_item = dataset_items[0]

    # output = check_document_exist(first_database_item, None)
    # assert output is not None

    # event = {"title": first_database_item["title"], "text": first_database_item["text"]}
    # insights = extract_insights(event, None)
    # assert insights is not None

    # with open(os.path.join(test_directory, "insights.json"), "w") as f:
    #     json.dump(insights, f, indent=4)

    # with open(os.path.join(test_directory, 'insights.json'), 'r') as file:
    #     insights_json: str = file.read()
    # insights = json.loads(s=insights_json)

    # merged_data = dataset_items[0]
    # merged_data.update(insights)

    # result = upsert_document(merged_data, None)
    # assert result is not None


def test_process_apify_event():
    var = os.environ.get("NEW_VAR")
    print(f"[DEBUG] var: {var}")

    with open(os.path.join(test_directory, "apify_payload.json"), "r") as file:
        apify_payload_json = file.read()
    apify_payload = json.loads(apify_payload_json)

    dataset_items = retrieve_scraped_data(apify_payload, None)
    assert len(dataset_items) == 15
