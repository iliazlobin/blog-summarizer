import os

from notion_client import Client

from blog_summarizer.config.aws import get_secret_or_env


def get_url_database_items(value, property="Url"):
    database_id = os.environ.get("NOTION_DATABASE_ID")
    token = get_secret_or_env("NOTION_TOKEN")

    notion = Client(
        auth=token,
        # log_level=logging.DEBUG
    )

    results = notion.databases.query(
        **{
            "database_id": database_id,
            "filter": {"property": property, "url": {"equals": value}},
        }
    ).get("results")

    print(f"[DEBUG] len(results): {len(results)}")
    print(f"[DEBUG] results: {results}")
    return results


def upsert_blog_database_document(cloud, document) -> dict[str, bool]:
    database_id = os.environ.get("NOTION_DATABASE_ID")

    takeaways_str = "\n".join(document["takeaways"])
    categories_dict = [{"name": category} for category in document["categories"]] if "categories" in document else []
    tags_dict = [{"name": tag} for tag in document["tags"]] if "tags" in document else []
    technologies_dict = [
        {"name": technology} for technology in document["technologies"]
    ]
    stakeholders_dict = [
        {"name": stakeholder} for stakeholder in document["stakeholders"]
    ]
    authors_str = "\n".join(document["authors"])

    token = get_secret_or_env("NOTION_TOKEN")
    notion = Client(
        auth=token,
        # log_level=logging.DEBUG
    )

    entry = {
        "parent": {"database_id": database_id},
        "properties": {
            "Url": {"url": document["url"]},
            "Cloud": {"select": {"name": cloud}},
            "Title": {"title": [{"text": {"content": document["title"]}}]},
            "Date": {"date": {"start": document["date"]}},
            "Summary": {"rich_text": [{"text": {"content": document["summary"]}}]},
            "Takeaways": {"rich_text": [{"text": {"content": takeaways_str}}]},
            "Blog": {"select": {"name": document["blog"]}},
            "Technologies": {"multi_select": technologies_dict},
            "Stakeholders": {"multi_select": stakeholders_dict},
            "Authors": {"rich_text": [{"text": {"content": authors_str}}]},
        },
    }
    if categories_dict:
        entry["properties"]["Categories"] = {"multi_select": categories_dict}
    if tags_dict:
        entry["properties"]["Tags"] = {"multi_select": tags_dict}

    result = notion.pages.create(**entry)
    created_time = result["created_time"]
    print(f"[DEBUG] created_time: {created_time}")

    return True
