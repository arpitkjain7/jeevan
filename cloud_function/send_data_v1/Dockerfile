FROM debian:bookworm
RUN apt-get update && apt-get upgrade -y
RUN apt-get install gcc -y \
    python3 \
    python3-pip \
    python3-venv -y \
    && apt-get clean
RUN apt-get install -y openjdk-17-jdk
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip3 install -r requirements.txt
COPY . ${LAMBDA_TASK_ROOT}
WORKDIR ${LAMBDA_TASK_ROOT}
ENTRYPOINT [ "python3", "-m", "awslambdaric" ]
CMD ["main.handler"]