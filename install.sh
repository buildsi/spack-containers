#!/bin/bash

if [ "$#" -eq 0 ]; then
    printf "Please provide a package filename and compiler as arguments.\n"
    exit 1
fi


pkg="${1}"
version="${2}"
compiler="${3:-all}"

printf "Installing ${pkg}@${version} across versions with ${compiler}\n"

# Setup spack
. /opt/spack/share/spack/setup-env.sh

# always build with debug!
export SPACK_ADD_DEBUG_FLAGS=true

# Just in case this was not run (but it should have been!)
spack compiler find

if [[ "${compiler}" == "all" ]]; then
    # Run a build for each pkg spec, all versions
    for compiler in $(spack compiler list --flat); do
        printf "spack install ${pkg}@${version} $compiler\n"
        spack install ${pkg}@${version} %$compiler
    done
else 
    # Assume just running for one compiler
    printf "spack install ${pkg}@${version} $compiler\n"
    spack install ${pkg}@${version} %$compiler
fi
