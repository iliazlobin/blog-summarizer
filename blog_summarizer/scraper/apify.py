from apify_client import ApifyClient

from blog_summarizer.config.aws import get_secret_or_env


def retrieve_dataset_items(dataset_id):
    token = get_secret_or_env("APIFY_TOKEN")

    apify_client = ApifyClient(token=token)
    dataset_client = apify_client.dataset(dataset_id)
    dataset_items = dataset_client.list_items().items

    return dataset_items
