#!/usr/bin/env python

import requests
import sys
import json

# These containers have one tag (latest) across architectures
containers = [
    "ghcr.io/buildsi/spack-ubuntu-18.04",
    "ghcr.io/buildsi/spack-ubuntu-20.04",
    "ghcr.io/buildsi/spack-centos-7",
    "ghcr.io/buildsi/spack-centos-8",
    "ghcr.io/buildsi/spack-fedora",
    # These have tags corresponding to gcc version and only amd64
    "ghcr.io/buildsi/ubuntu:gcc-8.1.0",
    "ghcr.io/buildsi/ubuntu:gcc-7.3.0",
    "ghcr.io/buildsi/ubuntu:gcc-9.4.0",
    "ghcr.io/buildsi/ubuntu:gcc-11.2.0",
    "ghcr.io/buildsi/ubuntu:gcc-4.9.4",
    "ghcr.io/buildsi/ubuntu:gcc-10.3.0",
]


def main(pkg):

    # Get versions of package
    versions = requests.get("https://raw.githubusercontent.com/spack/packages/main/data/packages/%s.json" % pkg)
    if versions.status_code != 200:
        sys.exit("Failed to get package versions")
    versions = versions.json()
    versions = list(set([x['name'] for x in versions['versions']]))
 
    # We will build up a matrix of containers and compilers
    matrix = []
    for container in containers:
        print(container)
        response = requests.get("https://crane.ggcr.dev/config/%s" % container)
        if response.status_code != 200:
            sys.exit(
                "Issue retrieving image config for % container: %s"
                % (container, response.reason)
            )
        config = response.json()
        labels = config["config"].get("Labels", {}).get("org.spack.compilers")
        if not labels:
            labels = ["all"]
        else:
            labels = [x for x in labels.strip(",").split(",") if x]
        # programatically get labels or default to "all compilers in the image"
        for label in labels:
            name = container.split('/')[-1].replace('spack', '').replace(':', '-').strip('-')
            if "gcc" not in name and "clang" not in name:
                name = name + "-" + label.replace("@", '-')
            for version in versions:
                container_name = name + "-" + version
                matrix.append([container, label, container_name, version])
    print(matrix)
    print("::set-output name=containers::%s\n" % json.dumps(matrix))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Please provide the package name as an argument!")
    main(sys.argv[1])
