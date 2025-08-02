from sqlalchemy import text
from .base import DataQualityCheck
import re


'''
Validate data against a regular expression pattern (e.g., phone, SSN, email format).
'''
class PatternMatchingCheck(DataQualityCheck):
    def run(self):
        try:
            table   = self.params["Table"]
            column  = self.params.get("Column", None)
            pattern = self.params.get("Pattern", None)

            regex = re.compile(pattern=pattern) # compile regex

            # error check for no column or pattern provided
            if not column:
                raise ValueError("No column provided for pattern check.")
            elif not pattern:
                raise ValueError("No pattern provided for pattern check.")

            query = f"SELECT {column} FROM {table} WHERE {column} IS NOT NULL"

            result = self.conn.execute(text(query)).fetchall()

            # record rows where the column does not follow the pattern
            non_matching_rows = [] # list of rows that do not follow the pattern format
            for row in result:
                value = str(row[0]).strip()
                if not regex.match(value):
                    non_matching_rows.append(value)

            pattern_check_result = {
                "Violating Rows Count": len(non_matching_rows),
                "Violating Rows": non_matching_rows
            }

            status = "PASS" if len(non_matching_rows) == 0 else "FAIL" # set PASS/FAIL status


            return {
                "qc_name": self.qc_name,        # str
                "status": status,               # str
                "details": pattern_check_result # dict
            }

        except Exception as e:
            return {
                "qc_name": self.qc_name,
                "status": "ERROR",
                "details": str(e)
            }