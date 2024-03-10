import os
from typing import List

from langchain.output_parsers.openai_functions import PydanticOutputFunctionsParser
from langchain.prompts import HumanMessagePromptTemplate
from langchain_community.utils.openai_functions import (
    convert_pydantic_to_openai_function,
)
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

from blog_summarizer.config.aws import get_secret_or_env


class BlogPostInsights(BaseModel):
    """Blog post insights."""

    summary: str = Field(description="one sentence sumamry of the blog post")
    takeaways: List[str] = Field(
        description="3-5 (depending on the length of the blog post) key takeaways from the blog post"
    )
    technologies: List[str] = Field(
        description="the key cloud services and technologies mentioined in the blog post"
    )
    stakeholders: List[str] = Field(
        description="groups of stakeholders who would be interested in the blog post"
    )

    # @validator("setup")
    # def question_ends_with_question_mark(cls, field):
    #     if field[-1] != "?":
    #         raise ValueError("Badly formed question!")
    #     return field


def get_blog_post_insights(title, text, cloud):
    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    "You are a professional cloud architect with solid analytic skills. "
                    "You know everything about {cloud} and are always up to date with the latest news. "
                    "You excel at analyzing blog post articles taking clear summaries and takeaways. "
                )
            ),
            HumanMessagePromptTemplate.from_template(
                "I want you to analize this blog post and provide me with the key insights about it. "
                "Blog post title: {title}. "
                "Blog post text: {text}. "
            ),
        ]
    )
    messages = chat_template.format_messages(title=title, text=text)

    key = get_secret_or_env("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = key

    openai_model = os.environ.get("OPENAI_MODEL")
    print(f"[DEBUG] openai_model: {openai_model}")

    model = ChatOpenAI(model=openai_model)

    openai_functions = [convert_pydantic_to_openai_function(BlogPostInsights)]

    parser = PydanticOutputFunctionsParser(pydantic_schema=BlogPostInsights)
    chain = model.bind(functions=openai_functions) | parser
    output = chain.invoke(messages)
    output_dict = output.dict()

    return output_dict
