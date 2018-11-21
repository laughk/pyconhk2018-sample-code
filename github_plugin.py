import re

from github import Github
from slackbot import settings
from slackbot.bot import respond_to


def get_pr_info_from_repo_link(url):

    res = re.match(
        r'<https://github.com/([^/]+)/([^/]+)/pull/([0-9]+)/?>$', url,
    )
    if not res:
        return None

    return {
        'org': res.group(1),
        'repository': f'{res.group(1)}/{res.group(2)}',
        'full_url': url,
        'number': int(res.group(3)),
    }


@respond_to(r'^gh\s+set\s+reviewer\s+(\S+)\s+(\S+)')
def set_issue_assigne(message, reviewers_type, pull_request_link):

    pullrequest_info = get_pr_info_from_repo_link(pull_request_link)
    if not pullrequest_info:
        message.send('Please Pull Request URL！')
        return

    reviewers = {
        # set member id for your team
        # ex.
        # 'frontend': ['massa142'],
        # 'developer': ['checkpoint', 'masakos'],
        # 'sre': ['laughk'],
    }
    reviewers['all'] = \
        reviewers['frontend'] \
        + reviewers['developer'] \
        + reviewers['sre'] \

    if reviewers_type not in reviewers.keys():
        message.send(
            'Could you choose one of that'
            'is `frontend` or `developer` or `sre`?',
        )
        return

    g = Github(settings.GITHUB_TOKEN)
    repo = g.get_repo(pullrequest_info['repository'])
    pull = repo.get_pull(pullrequest_info['number'])
    pull_author = pull.user.login

    request_reviewers = reviewers[reviewers_type]
    if pull_author in request_reviewers:
        request_reviewers.remove(pull_author)

    pull.create_review_request(request_reviewers)

    message.send('I asked for a review.')
