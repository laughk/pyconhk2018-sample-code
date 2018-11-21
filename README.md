# pyconhk2018-sample-code

this repository source code is a sample for [Collaboration hack with slackbot - PyCon Hong Kong](http://pycon.hk/sessions-2018/collaboration-hack-with-slackbot/).

# Usage

1. install requirements libraries.

    ```console
    $ python -m venv venv       # if you needs :-)
    $ source venv/bin/activate  # if you needs :-)
    (venv) $ pip install -r requirements.txt
    ```

1. copy and update for your environment.

    ```console
    (venv) $ cp slackbot_settings.py.example slackbot_settings.py
    ```

1. (optional) if you would like to use github\_plugin, you need update a dictionary `reviewers` included by `github_plugin.py`
1. run

    ```console
    (venv) $ python run.py
    ```
