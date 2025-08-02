from sqlalchemy import text
from .base import DataQualityCheck


'''
Count the records in the source dataset and compare it to the count in the target 
dataset to see if they match.
'''
class RowCountValidationCheck(DataQualityCheck):
    def run(self):
        try:
            src_table = self.params["Source"]["Table"]
            tgt_table = self.params["Target"]["Table"]

            # query tables to get the row counts from source and target
            src_count = self.conn[0].execute(text(f"SELECT COUNT(*) FROM {src_table}")).scalar()
            tgt_count = self.conn[1].execute(text(f"SELECT COUNT(*) FROM {tgt_table}")).scalar()
            row_check_results = {
                "Row Count Difference": abs(src_count - tgt_count),
                f"{src_table} Count (Source)": src_count,
                f"{tgt_table} Count (Target)": tgt_count

            }

            status = "PASS" if src_count == tgt_count else "FAIL" # set PASS/FAIL status


            return {
                "qc_name": self.qc_name,     # str
                "status":  status,           # str
                "details": row_check_results # dict
            }

        except Exception as e:
            return {
                "qc_name": self.qc_name,
                "status": "ERROR",
                "details": str(e)
            }