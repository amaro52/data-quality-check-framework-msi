# Data Quality Framework (Python)

Currently, we rely on a SQL Server-based package for performing data quality checks across various linked databases. This project's purporse is to migrate this functionality to a robust, Python-based solution that is entirely database-independent and supports customizable data validation logic via JSON configuration.

---

## Features

-Supports **custom SQL comparisons** (e.g., full value match, row counts)
- Built-in checks:  
  - Row Count Validation (`row_count_check.py`) 
  - Null Check (`null_check.py`)
  - Uniqueness Check (`uniqueness_check.py`) 
  - Pattern Matching Check (`pattern_check.py`) 
- Accepts configuration via `config.json`
- Works with **SQL Server**, and adaptable to PostgreSQL, MySQL, SQLite, etc.
- Outputs clear **console logs** and saves a full **JSON report**
- Modular & extensible design (plug in new checks with zero main loop changes)

---

## Folder Structure
```
dqf_python/
├── main.py                  # main file; entry point
├── config_loader.py         # loads and validates config.json
├── db_connector.py          # connects to database using SQLAlchemy
├── check_loader.py          # dispatches check type to correct class
├── reporter.py              # logs results and writes XLSX output
├── config.json              # configuration file for all checks and database info
├── requirements.txt         # python dependencies
└── checks/
    ├── base.py              # abstract base class for checks
    ├── custom_sql_check.py
    ├── row_count_check.py
    ├── null_check.py
    ├── uniqueness_check.py
    └── pattern_check.py
```

---

## Sample JSON Configuration

```json
{
  "ConnectionString": "mssql+pyodbc://sa:password@server/db?driver=ODBC+Driver+17+for+SQL+Server",
  "DataQualityChecks": [
    {
      "DisplayName": "Check Incident ID Uniqueness",
      "Type": "Uniqueness",
      "Table": "MSI_Internship.dbo.incidents",
      "Columns": ["incident_id"],
      "Connection": "SSMS",
      "Active": "1"
    },
    {
      "DisplayName": "Check Email Format",
      "Type": "Pattern",
      "Table": "FLEX_REMOTE_PRACTICE..admin.nmmain",
      "Column": "email",
      "Connection": "SSMS",
      "Pattern": "%@%.%",
      "Active": "1"
    }
  ]
}
```

## Setup & Run

Clone the repo and navigate into the project folder.

### Install dependencies:
```bash
pip install -r requirements.txt
```

Modify `config.json` with your connection string and quality checks.

### Run the framework:
```bash
python main.py
```

Check output in the console and in the `results/` folder:
```bash
results/dqf_results.xlsx
```

---

## Dependencies

- `sqlalchemy`
- `pyodbc`
- `pandas`

---

## Adding New Checks

To add a new check:

1. Create a new Python file in the `checks/` folder, subclassing `DataQualityCheck`.
2. Implement the `run(self, conn)` method.
3. Register the new check in `check_loader.py` under the appropriate `"Type"` key.

