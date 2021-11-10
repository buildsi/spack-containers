ARG base
FROM ${base}

ARG compiler
ARG package
ENV compiler=${compiler}
ENV package=${package}
COPY . /code
RUN /code/install.sh ${package} ${compiler}
ENTRYPOINT ["/bin/bash"]
