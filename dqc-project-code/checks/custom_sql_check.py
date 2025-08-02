from sqlalchemy import text
from .base import DataQualityCheck


'''
Runs custom source and target queries and compares results
'''
class CustomSQLCheck(DataQualityCheck):
    def run(self):
        try:
            source_query = self.params["Source"]["Query"]
            target_query = self.params["Target"]["Query"]

            # run quality check queries
            qc_query_src = source_query + " EXCEPT " + target_query # comparing source against target
            qc_query_tgt = target_query + " EXCEPT " + source_query # comparing target against source

            # get rows from source table and target table
            source_qc_results = self.conn[0].execute(text(qc_query_src)).fetchall() # source table quality check
            target_qc_results = self.conn[1].execute(text(qc_query_tgt)).fetchall() # target table quality check

            # create map of labels to the rows (e.g. "Source")
            qc_result = {
                "Source": source_qc_results,
                "Target": target_qc_results
            }

            # set status
            status = "PASS"
            if len(qc_result["Source"]) != 0 and len(qc_result["Target"]) != 0:
                status = "FAIL"

            
            return {
                "qc_name": self.qc_name,  # str
                "status":  status,        # str
                "details": qc_result      # list
            }
        
        except Exception as e:
            return {
                "qc_name": self.qc_name,
                "status": "ERROR",
                "details": str(e)
            } 