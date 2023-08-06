# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
from plumbum.cmd import docker
from .docker_runner import DockerRunner
from .git_helper import GitHelper


logger = logging.getLogger(__name__)


def quoted_output(container, cmd: str) -> str:
    return "\n".join(
        [
            "```",
            DockerRunner.run_simple_command(container, cmd, print_result=False),
            "```",
        ]
    )


class ManifestHeader:
    """ManifestHeader doesn't fall under common interface and we run it separately"""

    @staticmethod
    def create_header(short_image_name: str, owner: str, build_timestamp: str) -> str:
        commit_hash = GitHelper.commit_hash()
        commit_hash_tag = GitHelper.commit_hash_tag()
        commit_message = GitHelper.commit_message()

        image_size = docker[
            "images", f"{owner}/{short_image_name}:latest", "--format", "{{.Size}}"
        ]().rstrip()

        return "\n".join(
            [
                f"# Build manifest for image: {short_image_name}:{commit_hash_tag}",
                "",
                "## Build Info",
                "",
                f"* Build datetime: {build_timestamp}",
                f"* Docker image: {owner}/{short_image_name}:{commit_hash_tag}",
                f"* Docker image size: {image_size}",
                f"* Git commit SHA: [{commit_hash}](https://github.com/jupyter/docker-stacks/commit/{commit_hash})",
                "* Git commit message:",
                "```",
                f"{commit_message}",
                "```",
            ]
        )


class ManifestInterface:
    """Common interface for all manifests"""

    @staticmethod
    def markdown_piece(container) -> str:
        raise NotImplementedError


class AptPackagesManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container) -> str:
        return "\n".join(
            [
                "## Apt Packages",
                "",
                quoted_output(container, "apt list --installed"),
            ]
        )


class ApkPackagesManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container) -> str:
        return "\n".join(
            [
                "## Apk Packages",
                "",
                quoted_output(container, "apk list --installed"),
            ]
        )


class CondaEnvironmentManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container) -> str:
        return "\n".join(
            [
                "## Python Packages",
                "",
                quoted_output(container, "python --version"),
                "",
                quoted_output(container, "mamba info"),
                "",
                quoted_output(container, "mamba list"),
            ]
        )


class PipEnvironmentManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container) -> str:
        return "\n".join(
            [
                "## Python Packages",
                "",
                quoted_output(container, "python --version"),
                "",
                quoted_output(container, "pip list --disable-pip-version-check"),
                "",
                quoted_output(container, "pip list --outdated --disable-pip-version-check"),
            ]
        )
