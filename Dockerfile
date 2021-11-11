ARG base
FROM ${base}

ARG compiler
ARG package
ARG version
ENV compiler=${compiler}
ENV package=${package}
ENV version=${version}

LABEL org.spack.package.name ${package}
LABEL org.spack.package.version ${version}
LABEL org.spack.compilers ${compiler}
LABEL org.opencontainers.image.description "A base image ${base} with spack package ${package}@${version} %{compiler}"

COPY . /code
RUN /code/install.sh ${package} ${version} ${compiler}
ENTRYPOINT ["/bin/bash"]
