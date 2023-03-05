FROM baseapitest

WORKDIR /test/

COPY . .

RUN pip install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt

ENV PYTHONPATH "${PYTONPATH}:/test"

CMD ["/bin/bash"]
