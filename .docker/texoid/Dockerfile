FROM python:3.11.1-bullseye

RUN apt-get update && \
    apt-get install -y \
        texlive-binaries texlive-fonts-recommended texlive-xetex \
        texlive-latex-base texlive-latex-extra texlive-latex-recommended \
        texlive-pictures imagemagick git && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/DMOJ/texoid/
WORKDIR /texoid/
RUN pip3 install -e .

EXPOSE 8888
ENTRYPOINT texoid --address=texoid --port=8888
