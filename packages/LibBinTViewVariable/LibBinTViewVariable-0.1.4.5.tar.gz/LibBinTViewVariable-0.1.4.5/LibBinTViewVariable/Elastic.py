import time
import traceback

from elasticsearch import Elasticsearch


#
class ElasticSearchClient:
    def __init__(self, name: str, host: str, port: int):
        self.__es_client = Elasticsearch([{'host': host, 'port': port}])
        self.Name = name
        if self.__es_client.ping():
            self.__es_client.index(index="start-" + self.Name, body=dict(msg="Connect",
                                                                         time=time.strftime(
                                                                             "%Y-%m-%d %H:%M:%S")))
        else:
            raise Exception('It could not connect!')

    def store_record(self, index_name: str, doc_type: str, record: dict):
        try:
            self.__es_client.index(index=index_name, doc_type=doc_type, body=record)
        except Exception as ex:
            self.__es_client.index(index="error-" + self.Name, body=dict(traceback=traceback.format_exc(),
                                                                         msg=ex,
                                                                         time=time.strftime("%Y-%m-%d %H:%M:%S")))

    def store_warnings(self, msg: str):
        try:
            self.__es_client.index(index="warning-" + self.Name, body=dict(msg=msg,
                                                                           time=time.strftime("%Y-%m-%d %H:%M:%S")))
        except Exception as ex:
            self.__es_client.index(index="error-" + self.Name, body=dict(traceback=traceback.format_exc(),
                                                                         msg=ex,
                                                                         time=time.strftime("%Y-%m-%d %H:%M:%S")))

    def store_error(self, trace: str, msg: Exception):
        self.__es_client.index(index="error-" + self.Name, body=dict(traceback=trace,
                                                                     msg=str(msg),
                                                                     time=time.strftime("%Y-%m-%d %H:%M:%S")))
