import pandas as pd
from pathlib import Path

class ReportGenerator:
    @staticmethod
    def generate_summary(issues, output_dir):
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        summary_df = pd.DataFrame({"issues": issues})
        summary_path = Path(output_dir) / "summary_report.csv"
        summary_df.to_csv(summary_path, index=False)
        return summary_path

    @staticmethod
    def generate_score(issues):
        errors = len(issues)
        score = max(0, 100 - errors * 2)
        return score
