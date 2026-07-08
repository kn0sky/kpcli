from .build import build_exp
from .session import cd_remote_tmp
from .upload import upload


def prepare_target(io):
    build_exp()
    uploaded = upload(io)
    if uploaded:
        cd_remote_tmp(io)
