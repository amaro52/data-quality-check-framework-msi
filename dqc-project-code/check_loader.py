from checks.custom_sql_check import CustomSQLCheck
from checks.null_check import NullCheck
from checks.uniqueness_check import UniquenessCheck
from checks.row_count_check import RowCountValidationCheck
from checks.pattern_check import PatternMatchingCheck

'''
Method to map the "Type" of a quality check to a class
'''
def get_quality_check_instance(qc_info, connection_map):
    try:
        qc_type = qc_info.get("Type", "CUSTOM").upper()

        if qc_type == "CUSTOM":
            # need to get both connections for custom quality checks
            src_connection_type = qc_info["Source"]["Connection"]
            tgt_connection_type = qc_info["Target"]["Connection"]
            
            src_connection = connection_map[src_connection_type]
            tgt_connection = connection_map[tgt_connection_type]
                

            return CustomSQLCheck(
                qc_name=qc_info["DisplayName"],
                conn=(src_connection, tgt_connection),
                params=qc_info
            )
        elif qc_type == "NULL_CHECK":
            connection_type = qc_info["Connection"]
            connection      = connection_map[connection_type]

            return NullCheck(
                qc_name=qc_info["DisplayName"],
                conn=connection,
                params=qc_info
            )
        elif qc_type == "UNIQUENESS":
            connection_type = qc_info["Connection"]
            connection      = connection_map[connection_type]

            return UniquenessCheck(
                qc_name=qc_info["DisplayName"],
                conn=connection,
                params=qc_info
            )
        elif qc_type == "PATTERN":
            connection_type = qc_info["Connection"]
            connection      = connection_map[connection_type]

            return PatternMatchingCheck(
                qc_name=qc_info["DisplayName"],
                conn=connection,
                params=qc_info
            )
        elif qc_type == "ROWS":
            # need to get both connections
            src_connection_type = qc_info["Source"]["Connection"]
            tgt_connection_type = qc_info["Target"]["Connection"]

            src_connection = connection_map[src_connection_type]
            tgt_connection = connection_map[tgt_connection_type]

            return RowCountValidationCheck(
                qc_name=qc_info["DisplayName"],
                conn=(src_connection, tgt_connection),
                params=qc_info
            )

        
        else:
            raise ValueError(f"Unknown check type: {qc_type}")
    except Exception as e:
        print(str(e))