from agents import (
    create_legal_reviewer, create_textalignment_reviewer, 
    create_consistency_reviewer, create_completion_reviewer, 
    create_meta_reviewer
)

def setup_review_chats():
    legal_reviewer = create_legal_reviewer()
    textalignment_reviewer = create_textalignment_reviewer()
    consistency_reviewer = create_consistency_reviewer()
    completion_reviewer = create_completion_reviewer()
    meta_reviewer = create_meta_reviewer()

    review_chats = [
        {
        "recipient": legal_reviewer, "message": reflection_message, 
         "summary_method": "reflection_with_llm",
         "summary_args": {"summary_prompt" : 
            "Return review into a JSON object only:"
            "{'Reviewer': '', 'Review': ''}.",},
         "max_turns": 1},
        {"recipient": textalignment_reviewer, "message": reflection_message, 
         "summary_method": "reflection_with_llm",
         "summary_args": {"summary_prompt" : 
            "Return review into a JSON object only:"
            "{'reviewer': '', 'review': ''}",},
         "max_turns": 1},
        {"recipient": consistency_reviewer, "message": reflection_message, 
         "summary_method": "reflection_with_llm",
         "summary_args": {"summary_prompt" : 
            "Return review into a JSON object only:"
            "{'reviewer': '', 'review': ''}",},
         "max_turns": 1},
        {"recipient": completion_reviewer, "message": reflection_message, 
         "summary_method": "reflection_with_llm",
         "summary_args": {"summary_prompt" : 
            "Return review into a JSON object only:"
            "{'reviewer': '', 'review': ''}",},
         "max_turns": 1},
         {"recipient": meta_reviewer, 
          "message": "Aggregrate feedback from all reviewers and give final suggestions on the writing.", 
         "max_turns": 1},
    ]

    return review_chats