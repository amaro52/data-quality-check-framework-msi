from config_loader import load_config
from db_connector import create_db_engine
from check_loader import get_quality_check_instance
from reporter import save_results_xlsx, print_result


def main():
    config = load_config("config.json") # load config file

    # map of all the connection types to the connection strings
    connections = {}
    for db, conn_str in config["ConnectionStrings"].items():
        engine = create_db_engine(connection_string=conn_str) # connect to databse with conn_str
        conn = engine.connect()

        connections[db] = conn


    qc_results = {}
    # loop through table names (Law, CAD, etc.)
    for table, quality_checks in config["DataQualityChecks"].items():
        check_results = [] # quality checks results for the specific table

        # loop through quality checks within table
        for qc in quality_checks:
            if qc.get("Active") != "0":
                check = get_quality_check_instance(qc_info=qc, connection_map=connections) # get type of quality check
                result = check.run() # run quality check

                check_results.append(result)
        
        qc_results[table] = check_results

    save_results_xlsx(results=qc_results) # save results to a file


if __name__ == "__main__":
    main()