#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from plumbum.cmd import git


class GitHelper:
    @staticmethod
    def commit_hash() -> str:
        return git["rev-parse", "HEAD"]().strip()

    @staticmethod
    def commit_hash_tag() -> str:
        return GitHelper.commit_hash()[:12]

    @staticmethod
    def commit_message() -> str:
        return git["log", -1, "--pretty=%B"]().strip()

    @staticmethod
    def commit_tag() -> str:
        return git["tag", "--contains"]().strip()

    @staticmethod
    def remote_url():
        url = git['config', 'remote.origin.url']().strip()
        return url.replace('ssh://', '') \
            .replace('git@', 'https://') \
            .replace('com:', 'com/') \
            .replace('.git', '')


if __name__ == "__main__":
    print("Git hash:", GitHelper.commit_hash())
    print("Git tag:", GitHelper.commit_tag())
    print("Git message:", GitHelper.commit_message())
    print("Git remote url:", GitHelper.remote_url())
