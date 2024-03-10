from blog_summarizer.datastore.notion import (
    get_url_database_items,
    upsert_blog_database_document,
)
from blog_summarizer.llm.openai import get_blog_post_insights
from blog_summarizer.scraper.apify import retrieve_dataset_items


def retrieve_scraped_data(event, context):
    datasetId = event["resource"]["defaultDatasetId"]
    exitCode = event["resource"]["exitCode"]
    print(f"[DEBUG] datasetId: {datasetId}")
    print(f"[DEBUG] exitCode: {exitCode}")

    if exitCode != 0:
        return []

    items = retrieve_dataset_items(datasetId)
    print(f"[DEBUG] number_of_items: {len(items)}")

    return items


def check_document_exist(event, context):
    url = event["url"]
    print(f"[DEBUG] url: {url}")

    items = get_url_database_items(url)

    if len(items) == 0:
        return {"documentExist": False}

    return {"documentExist": True}


def extract_insights(event, context):
    title = event["title"]
    text = event["text"]
    print(f"[DEBUG] title: {title}")
    print(f"[DEBUG] text: {text}")

    insights = get_blog_post_insights(title, text, "Azure")
    print(f"[DEBUG] insights: {insights}")

    return insights


def upsert_document(event, context):
    print(f"[DEBUG] event: {event}")

    document = event
    document["authors"] = [event["author"]]
    result = upsert_blog_database_document("Azure", document)
    print(f"[DEBUG] result: {result}")

    if result is not True:
        return {"documentInserted": False}

    return {"documentInserted": True}
