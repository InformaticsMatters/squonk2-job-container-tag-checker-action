#!/usr/bin/env python

import glob
import os
import re
import sys
from typing import List

from munch import DefaultMunch
import yaml

from decoder import decoder

# The repository to check is mounted into the container under /github/workspace.

GITHUB_WORKSPACE: str = "/Users/alan/Code/InformaticsMatters/virtual-screening"
DM_DIR: str = f"{GITHUB_WORKSPACE}/data-manager"
MANIFEST_FILES: str = f"{DM_DIR}/manifest-*.yaml"

# Iterate through all the Data Manager manifests,
# collecting the names of the the Job definition files.

# Production tags are 2 or 3-number version strings
# i.e. 2024.3 or 1.0.2
VALID_IMAGE_TAG_PATTERN: re.Pattern = re.compile("^[0-9]+\.[0-9]+(\.[0-9]+)?$")

def check() -> None:
    """Runs the check."""
    jd_files: List[str] = []
    manifest_files: List[str] = glob.glob(MANIFEST_FILES)
    for manifest_file in manifest_files:
        with open(manifest_file, "r", encoding="utf-8") as f_manifest:
            manifest = yaml.safe_load(f_manifest)
            if "job-definition-files" not in manifest:
                print(f"Missing job-definition-files in {manifest_file}")
                sys.exit(1)
            jd_files += manifest["job-definition-files"]

    print(f"Checking {len(jd_files)} job definition files...")

    for jd_file in jd_files:
        print(f"Checking {jd_file}...")
        jd_path: str = os.path.join(DM_DIR, jd_file)
        with open(jd_path, "r", encoding="utf-8") as f_jd:
            jd = yaml.safe_load(f_jd)
            jd_munch: DefaultMunch = DefaultMunch.fromDict(jd)
            for jd_name in jd_munch.jobs:
                _, image_tag = decoder.get_image(jd_munch.jobs[jd_name])
                tag_match: re.Match = VALID_IMAGE_TAG_PATTERN.match(image_tag)
                if not tag_match:
                    print(f"ERROR: Invalid image tag '{image_tag}' for job '{jd_name}'")
                    sys.exit(1)

check()
