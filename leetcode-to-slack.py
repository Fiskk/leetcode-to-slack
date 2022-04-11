# from logging import _Level
import requests
import json
from slack import WebClient
from slack.errors import SlackApiError
from random import randrange


# JSON Form
# "stat": {
#         "question_id": 12,
#         "question__article__live": true,
#         "question__article__slug": "integer-to-roman",
#         "question__article__has_video_solution": false,
#         "question__title": "Integer to Roman",
#         "question__title_slug": "integer-to-roman",
#         "question__hide": false,
#         "total_acs": 667835,
#         "total_submitted": 1126162,
#         "frontend_question_id": 12,
#         "is_new_question": false
#       },
#       "status": null,
#       "difficulty": { "level": 2 },
#       "paid_only": false,
#       "is_favor": false,
#       "frequency": 0,
#       "progress": 0

def post_problem(all_problems, difficulty, type):

    slug = all_problems[randrange(len(all_problems))]  # choose random problem
    webhook_url = 'https://hooks.slack.com/services/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'
    output = { "text": "Today's " + difficulty + " " + type + " problem:" + "https://leetcode.com/problems/" + slug }
    # post
    slack_response = requests.post(
        webhook_url, data=json.dumps(output),
        headers={'Content-Type': 'application/json'}
    )
    if slack_response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (slack_response.status_code, slack_response.text)
        )

def get_algorithm_problems():
    # get data
    response = requests.get("https://leetcode.com/api/problems/algorithms/")
    data = json.loads(response.content)

    return data

def get_easy_algorithm_problems(problems):
    # filter-out premium, medium, and hard problems, get slugs


    all_easy_algorithm_problems = []
    for problem in range(len(problems["stat_status_pairs"])):
        difficulty_dict = json.loads(str(problems["stat_status_pairs"][problem]["difficulty"]).replace("'", "\"", 2))
        if (not problems["stat_status_pairs"][problem]["paid_only"]) and difficulty_dict['level'] == 1:
            #if data # look for easy questions
            single_problem = problems["stat_status_pairs"][problem]["stat"]["question__title_slug"]
            all_easy_algorithm_problems.append(single_problem)

    return all_easy_algorithm_problems

all_algorithm_problems = get_algorithm_problems()
post_problem(get_easy_algorithm_problems(all_algorithm_problems), 'easy', 'algorithm')
