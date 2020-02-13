FROM jupyter/minimal-notebook:latest

COPY requirements.txt /tmp/
RUN python3 -m pip install --trusted-host pypi.python.org --requirement /tmp/requirements.txt
COPY . /tmp/

EXPOSE 8888

CMD ["jupyter", "notebook"]
