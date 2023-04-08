FROM debian:bookworm
RUN apt-get update && apt-get upgrade -y
RUN apt-get install gcc -y \
    python3 \
    python3-pip \
    python3-venv -y \
    && apt-get clean
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
ENV PATH="/venv/bin:$PATH"
ENTRYPOINT [ "/bin/bash" ]
CMD ["run.sh"]