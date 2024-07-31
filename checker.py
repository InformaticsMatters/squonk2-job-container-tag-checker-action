#!/usr/bin/env python

import glob
import os
import re
import sys
from typing import List

from munch import DefaultMunch
import yaml

from decoder import decoder

# The repository we're run in is mounted into the container under /github/workspace.
GITHUB_WORKSPACE: str = "/github/workspace"
DM_DIR: str = f"{GITHUB_WORKSPACE}/data-manager"
MANIFEST_FILE_GLOB: str = f"{DM_DIR}/manifest-*.yaml"

# Production tags are 2 or 3-number version strings
# i.e. 2024.3 or 1.0.2
VALID_IMAGE_TAG_PATTERN: re.Pattern = re.compile(r"^[0-9]+\.[0-9]+(\.[0-9]+)?$")

# Collected errors
ERRORS: List[str] = []


def error(msg: str) -> None:
    """Prints and collects an error message"""
    ERRORS.append(msg)
    print(f" ERROR: {msg}")


def check() -> None:
    """Runs the check."""
    jd_files: List[str] = []
    manifest_files: List[str] = glob.glob(MANIFEST_FILE_GLOB)
    for manifest_file in manifest_files:
        with open(manifest_file, "r", encoding="utf-8") as f_manifest:
            manifest = yaml.safe_load(f_manifest)
            if "job-definition-files" not in manifest:
                print(f"Missing job-definition-files in {manifest_file}")
                sys.exit(1)
            jd_files += manifest["job-definition-files"]

    if not jd_files:
        error("No job definition files found in manifest files")

    for jd_file in jd_files:
        print(f"Checking Job Manifest '{jd_file}'...")
        jd_path: str = os.path.join(DM_DIR, jd_file)
        with open(jd_path, "r", encoding="utf-8") as f_jd:
            jd = yaml.safe_load(f_jd)
            jd_munch: DefaultMunch = DefaultMunch.fromDict(jd)
            for jd_name in jd_munch.jobs:
                _, image_tag = decoder.get_image(jd_munch.jobs[jd_name])
                tag_match: re.Match = VALID_IMAGE_TAG_PATTERN.match(image_tag)
                if not tag_match:
                    msg: str = f"Invalid image tag '{image_tag}' for job '{jd_name}'"
                    error(msg)


check()
if not ERRORS:
    print("--")
    print("OK")
else:
    print("------")
    print("FAILED - there were invalid tags")
    sys.exit(1)
