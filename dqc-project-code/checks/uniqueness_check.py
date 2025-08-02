from sqlalchemy import text
from .base import DataQualityCheck


'''
Verify that values in a given column (or combination of columns) are unique.
'''
class UniquenessCheck(DataQualityCheck):
    def run(self):
        try:
            table   = self.params["Table"]
            columns = self.params.get("Columns", None)

            # error check for no columns provided
            if not columns:
                raise ValueError("No columns provided for uniquness check.")
            
            # build query
            columns_str = (", ").join(columns)
            group_by_clause = f"GROUP BY {columns_str} HAVING COUNT(*) > 1"
            query = f"SELECT {columns_str} FROM {table} {group_by_clause}"

            result = self.conn.execute(text(query)).fetchall() # run query
            cleaned_result = [str(row[0]).strip() for row in result] # remove whitespace and clean up result
            unique_check_result = {
                    "Violating Rows Count": len(cleaned_result),
                    "Violating Rows": cleaned_result
            }

            status = "PASS" if len(result) == 0 else "FAIL" # set PASS/FAIL status


            return {
                "qc_name": self.qc_name,       # str
                "status": status,              # str
                "details": unique_check_result # dict
            }
        
        except Exception as e:
            return {
                "qc_name": self.qc_name,
                "status": "ERROR",
                "details": str(e)
            }