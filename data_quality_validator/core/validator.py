import pandas as pd
import re

class DataValidator:
    def __init__(self, df: pd.DataFrame, rules: dict, logger):
        self.df = df.reset_index(drop=True)
        self.rules = rules
        self.logger = logger
        self.issues = []
        self.invalid_records = []

    def log_invalid(self, row_idx, col_name, reason, value):
        self.invalid_records.append({
            "row_no": row_idx + 2,  # +2 because pandas index starts at 0 + header row
            "column": col_name,
            "error": reason,
            "value": value
        })

    def validate(self):
        for col in self.rules["columns"]:
            name = col["name"]
            if name not in self.df.columns:
                self.issues.append(f"Missing column: {name}")
                continue

            series = self.df[name]

            # Required check
            if col.get("required"):
                for i, val in series[series.isna()].items():
                    self.log_invalid(i, name, "Missing required value", val)

            # Type check
            dtype = col.get("dtype")
            if dtype == "int":
                invalid = self.df[~self.df[name].apply(lambda x: isinstance(x, (int, float)))]
                for i, val in invalid[name].items():
                    self.log_invalid(i, name, "Invalid integer type", val)

            # Range check
            if "min" in col and "max" in col:
                invalid = self.df[(self.df[name] < col["min"]) | (self.df[name] > col["max"])]
                for i, val in invalid[name].items():
                    self.log_invalid(i, name, f"Out of range ({col['min']}-{col['max']})", val)

            # Pattern check
            if "pattern" in col:
                pattern = re.compile(col["pattern"])
                invalid = self.df[~self.df[name].astype(str).apply(lambda x: bool(pattern.match(x)))]
                for i, val in invalid[name].items():
                    self.log_invalid(i, name, "Invalid pattern", val)

        # Column-level issues summary
        self.issues = [f"{col['name']} → {sum(self.df[col['name']].isna())} nulls" 
                       for col in self.rules["columns"] if col["name"] in self.df.columns]
        return self.issues, pd.DataFrame(self.invalid_records)
