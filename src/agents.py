import autogen
from src.config import llm_config

OUTPUTS_DIR = "outputs"


def create_financial_assistant():
    return autogen.AssistantAgent(
        name="Financial_assistant",
        llm_config=llm_config,
    )


def create_research_assistant():
    return autogen.AssistantAgent(
        name="Researcher",
        llm_config=llm_config,
    )


def create_writer():
    return autogen.AssistantAgent(
        name="Writer",
        llm_config=llm_config,
        system_message=(
            "You are a professional financial writer. "
            "You write clear, data-driven financial reports in markdown. "
            "Rules you must always follow:\n"
            "1. Use ONLY the real data values provided in the conversation — never write N/A for values that were given.\n"
            "2. NEVER embed images or use markdown image syntax like ![...](...). Images are displayed separately.\n"
            "3. NEVER wrap your output in a markdown code block.\n"
            "4. Always include a markdown table comparing fundamental ratios.\n"
            "5. Return only the report text — no preamble or closing comments."
        ),
    )


def create_critic():
    return autogen.AssistantAgent(
        name="Critic",
        is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
        llm_config=llm_config,
        system_message=(
            "You are a critic. You review the work of the writer and provide "
            "constructive feedback to help improve the quality of the content."
        ),
    )


def create_legal_reviewer():
    return autogen.AssistantAgent(
        name="Legal_Reviewer",
        llm_config=llm_config,
        system_message=(
            "You are a legal reviewer, known for your ability to ensure that content "
            "is legally compliant and free from any potential legal issues. "
            "Make sure your suggestion is concise (within 3 bullet points), "
            "concrete and to the point. Begin the review by stating your role."
        ),
    )


def create_consistency_reviewer():
    return autogen.AssistantAgent(
        name="Consistency_Reviewer",
        llm_config=llm_config,
        system_message=(
            "You are a consistency reviewer, known for your ability to ensure that "
            "the written content is consistent throughout the report. "
            "Refer numbers and data in the report to determine which version should "
            "be chosen in case of contradictions. "
            "Make sure your suggestion is concise (within 3 bullet points), "
            "concrete and to the point. Begin the review by stating your role."
        ),
    )


def create_textalignment_reviewer():
    return autogen.AssistantAgent(
        name="Text_Alignment_Reviewer",
        llm_config=llm_config,
        system_message=(
            "You are a text data alignment reviewer, known for your ability to ensure "
            "that the meaning of the written content is aligned with the numbers in the "
            "text. You must ensure that the text clearly describes the numbers provided "
            "without contradictions. "
            "Make sure your suggestion is concise (within 3 bullet points), "
            "concrete and to the point. Begin the review by stating your role."
        ),
    )


def create_completion_reviewer():
    return autogen.AssistantAgent(
        name="Completion_Reviewer",
        llm_config=llm_config,
        system_message=(
            "You are a content completion reviewer, known for your ability to check "
            "that financial reports contain all the required elements. "
            "You always verify that the report contains: a news report about each asset, "
            "a description of the different ratios and prices, "
            "a description of possible future scenarios, a table comparing fundamental "
            "ratios and at least a single figure. "
            "Make sure your suggestion is concise (within 3 bullet points), "
            "concrete and to the point. Begin the review by stating your role."
        ),
    )


def create_meta_reviewer():
    return autogen.AssistantAgent(
        name="Meta_Reviewer",
        llm_config=llm_config,
        system_message=(
            "You are a meta reviewer. You aggregate and review the work of other "
            "reviewers and give a final suggestion on the content."
        ),
    )


def create_user_proxy_auto():
    return autogen.UserProxyAgent(
        name="User_Proxy_Auto",
        human_input_mode="NEVER",
        is_termination_msg=lambda x: (
            x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE")
        ),
        code_execution_config={
            "last_n_messages": 3,
            "work_dir": OUTPUTS_DIR,
            "use_docker": False,
        },
    )
