from abc import ABC, abstractmethod
from sqlalchemy import text


'''
Abstract base class for all data quality checks
'''
class DataQualityCheck(ABC):
    '''
    Method to initialize data quality check
    qc_name    [=] used to identify quality checks
    db_engine  [=] SQLAlchemy engine
    params     [=] params like table, columns, etc.
    '''
    def __init__(self, qc_name, conn, params):
        self.qc_name = qc_name
        self.conn = conn
        self.params = params

    
    '''
    Method to execute data quality check
    Returns dict with status, qc_name, and details
    '''
    @abstractmethod
    def run(self):
        pass