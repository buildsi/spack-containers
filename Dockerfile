ARG base
FROM ${base}

ARG compiler
ARG package
ARG version
ENV compiler=${compiler}
ENV package=${package}
ENV version=${version}
COPY . /code
RUN /code/install.sh ${package} ${version} ${compiler}
ENTRYPOINT ["/bin/bash"]
