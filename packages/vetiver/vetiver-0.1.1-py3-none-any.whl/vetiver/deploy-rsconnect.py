from rsconnect import api, actions


def connect(url, api_key):
    connect_server = api.RSConnectServer(url=url, api_key=api_key)
    return connect_server


# WIP
# def vetiver_deploy_rsconnect(connect_server):

#     actions.deploy_python_fastapi(connect_server, directory = ".", \
#     extra_files = None, excludes = None, entry_point = "app.py", \
#     title="vetiver app", python=None, \
#     conda_mode=False, force_generate=True, log_callback=None)
