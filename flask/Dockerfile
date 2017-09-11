#                            :2.2.0
FROM cgarciae/pyspark-notebook:2.1.1

RUN pip install pymongo
RUN pip install flask
RUN pip install Flask-PyMongo
RUN pip install click
RUN pip install odo
RUN pip install tabulate
RUN pip install tensorflow
RUN pip install h5py
RUN pip install pillow
RUN pip install keras
RUN pip install tensorflow
RUN pip install plotly
RUN pip install cytoolz

RUN echo 1
RUN pip install git+https://github.com/cgarciae/tfinterface.git@develop

WORKDIR /code

ENTRYPOINT []

CMD python main.py
