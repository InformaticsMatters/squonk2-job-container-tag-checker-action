#!/usr/bin/env python
"""A GitHub docker-based Action to check the image tags in job-definition files.
The Action can also be used as a pre-commit hook.
"""

import glob
import os
import re
import sys
from typing import List

from munch import DefaultMunch  # type: ignore
import yaml

from decoder import decoder  # type: ignore

# The repository we're run in is mounted into the container under /github/workspace,
# which is the image WORKDIR value - so '.' is the root of the repository to check.
# When run as a pre-commit hook, the repository is mounted under /src
# but the pre-commit logic also sets WORKDIR accordingly, so "." is still the root.
GITHUB_WORKSPACE: str = "."
# The Data Manager directory (manifests)
DM_DIR: str = f"{GITHUB_WORKSPACE}/data-manager"
# FIle globs for manifests and Nextflow files
MANIFEST_FILE_GLOB: str = f"{DM_DIR}/manifest-*.yaml"
NEXTFLOW_FILE_GLOB: str = f"{GITHUB_WORKSPACE}/**/*.nf"

# Production tags are 2 or 3-number version strings, i.e. 2024.3 or 1.0.2
VALID_IMAGE_TAG_PATTERN: re.Pattern = re.compile(r"^[0-9]+\.[0-9]+(\.[0-9]+)?$")
# What does a nextflow container declaration look like?
#   container 'informaticsmatters/vs-moldb:latest'
NEXTFLOW_CONTAINER_PATTERN: re.Pattern = re.compile(
    r"^\s+container '((?P<iname>\S+)(:(?P<itag>\S+)))?'\s*$"
)

# Collected errors
ERRORS: List[str] = []


def error(msg: str) -> None:
    """Prints and collects an error message"""
    print(f"ERROR: {msg}")
    ERRORS.append(msg)


def check() -> None:
    """Runs the built-in tag checks for job-definition files
    and nextflow files."""
    # Look for Job manifests
    jd_files: List[str] = []
    manifest_files: List[str] = glob.glob(MANIFEST_FILE_GLOB)
    for manifest_file in manifest_files:
        with open(manifest_file, encoding="utf-8") as f_manifest:
            manifest = yaml.safe_load(f_manifest)
            if "job-definition-files" not in manifest:
                print(f"Missing job-definition-files in {manifest_file}")
                sys.exit(1)
            jd_files += manifest["job-definition-files"]
    # Process Job definition files (declared in manifests)
    if not jd_files:
        error("No job definition files found")
    for jd_file in jd_files:
        jd_path: str = os.path.join(DM_DIR, jd_file)
        with open(jd_path, encoding="utf-8") as f_jd:
            jd = yaml.safe_load(f_jd)
            jd_munch: DefaultMunch = DefaultMunch.fromDict(jd)
            for jd_name in jd_munch.jobs:
                _, image_tag = decoder.get_image(jd_munch.jobs[jd_name])
                tag_match = VALID_IMAGE_TAG_PATTERN.match(image_tag)
                if not tag_match:
                    msg: str = (
                        f"Invalid image tag '{image_tag}' for job '{jd_name}' in {jd_path}"
                    )
                    error(msg)

    # Process Nextflow files
    nf_files: List[str] = glob.glob(NEXTFLOW_FILE_GLOB, recursive=True)
    for nf_file in nf_files:
        with open(nf_file, encoding="utf-8") as file:
            for line_no, line in enumerate(file, start=1):
                if container_match := NEXTFLOW_CONTAINER_PATTERN.match(line):
                    if itag := container_match.group("itag"):
                        tag_match = VALID_IMAGE_TAG_PATTERN.match(itag)
                        if not tag_match:
                            error(
                                f"Invalid container tag '{itag}' in {nf_file}:{line_no}"
                            )
                    else:
                        error(f"Missing container tag in {nf_file}:{line_no}")


if __name__ == "__main__":

    check()
    if ERRORS:
        print("------")
        if len(ERRORS) == 1:
            print("FAILED - there is 1 invalid tag")
        else:
            print(f"FAILED - there are {len(ERRORS)} invalid tags")
        sys.exit(1)
