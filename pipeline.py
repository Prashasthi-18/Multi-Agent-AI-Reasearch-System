from agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)


def run_research_pipeline(topic: str):

    state = {
        "search_results": "",
        "scraped_content": "",
        "report": "",
        "feedback": "",
        "progress": [],
    }

    # ----------------------------
    # STEP 1 : Search Agent
    # ----------------------------
    search_agent = build_search_agent()

    search_result = search_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"Find recent, reliable and detailed information about {topic}"
                )
            ]
        }
    )

    state["search_results"] = search_result["messages"][-1].content
    state["progress"].append("🔍 Search Agent completed")

    # ----------------------------
    # STEP 2 : Reader Agent
    # ----------------------------
    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"""
Based on the following search results about "{topic}",

Pick the most relevant URL and scrape it for detailed content.

Search Results:

{state["search_results"][:1000]}
"""
                )
            ]
        }
    )

    state["scraped_content"] = reader_result["messages"][-1].content
    state["progress"].append("📖 Reader Agent completed")

    # ----------------------------
    # STEP 3 : Writer Chain
    # ----------------------------

    research = f"""SEARCH RESULTS{state["search_results"]}
                SCRAPED CONTENT{state["scraped_content"]}  """

    state["report"] = writer_chain.invoke(
        {
            "topic": topic,
            "research": research,
        }
    )

    state["progress"].append("✍ Writer completed")

    # ----------------------------
    # STEP 4 : Critic Chain
    # ----------------------------

    state["feedback"] = critic_chain.invoke(
        {
            "report": state["report"],
        }
    )

    state["progress"].append("🧠 Critic completed")

    return state