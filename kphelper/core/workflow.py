from .build import build_exp
from .session import cd_remote_tmp, managed_session
from .upload import upload


def build_only():
    return build_exp()


def upload_and_cd(io):
    uploaded = upload(io)
    if uploaded:
        cd_remote_tmp(io)
    return uploaded


def build_start_upload_and_interact(build_action, target_action, interactive_action):
    build_action()
    with managed_session(target_action) as io:
        upload_and_cd(io)
        interactive_action(io)
