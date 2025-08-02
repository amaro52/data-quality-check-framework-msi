from sqlalchemy import text
from .base import DataQualityCheck


'''
Ensure a specified column (or set of columns) does not contain NULL values.
'''
class NullCheck(DataQualityCheck):
    def run(self):
        try:
            table   = self.params["Table"]
            columns = self.params.get("Columns", None) # list of columns

            # error check for no column provided
            if not columns:
                raise ValueError("No columns provided for null check.")

            # build query to filter columns
            filtered_columns = f"{columns[0]} IS NULL"
            for i in range(1, len(columns)):
                next_column_filter = f" OR {columns[i]} IS NULL"
                filtered_columns += next_column_filter
                
            query = f"SELECT * FROM {table} WHERE {filtered_columns}"

            result = self.conn.execute(text(query)).fetchall() # get rows with NULL values in specified columns
            null_check_result = {
                "Count": len(result),
                "Results": result
            }

            status = "PASS" if len(result) == 0 else "FAIL" # set PASS/FAIL status

            
            return {
                "qc_name": self.qc_name,     # str
                "status":  status,           # str
                "details": null_check_result # dict
            }
        
        except Exception as e:
            return {
                "qc_name": self.qc_name,
                "status": "ERROR",
                "details": str(e)
            }