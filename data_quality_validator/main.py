from data_quality_validator.core.config_loader import ConfigLoader
from data_quality_validator.core.validator import DataValidator
from data_quality_validator.core.report_generator import ReportGenerator
from data_quality_validator.core.logger import get_logger
from pathlib import Path
import pandas as pd

def validate_all_files():
    app_config = ConfigLoader.load_app_config()
    rules = ConfigLoader.load_rules()

    input_dir = Path(app_config["app"]["input_dir"])
    output_dir = Path(app_config["app"]["output_dir"])
    log_file = app_config["app"]["log_file"]

    logger = get_logger(log_file)
    logger.info("Starting multi-file validation with row-level tracking...")

    all_results = []

    for file in input_dir.glob("*.csv"):
        df = pd.read_csv(file)
        logger.info(f"Validating: {file.name}")

        validator = DataValidator(df, rules, logger)
        issues, invalid_rows = validator.validate()

        # Save invalid rows (row-level)
        invalid_path = output_dir / f"{file.stem}_invalid.csv"
        invalid_rows.to_csv(invalid_path, index=False)
        logger.info(f"Invalid record file saved: {invalid_path.name}")

        # NEW: Generate per-column issue summary
        if not invalid_rows.empty:
            column_summary = (
                invalid_rows.groupby("column")["error"]
                .count()
                .reset_index()
                .rename(columns={"error": "issue_count"})
            )
            summary_path = output_dir / f"{file.stem}_summary.csv"
            column_summary.to_csv(summary_path, index=False)
            logger.info(f"Column-level summary saved for {file.name}")
        else:
            pd.DataFrame(columns=["column", "issue_count"]).to_csv(
                output_dir / f"{file.stem}_summary.csv", index=False
            )
            logger.info(f"No issues found for {file.name} (summary created)")

        # Compute data quality score
        score = ReportGenerator.generate_score(issues)
        all_results.append({
            "file": file.name,
            "issues": len(issues),
            "invalid_rows": len(invalid_rows),
            "score": score
        })

        logger.info(f"{file.name} complete | Score: {score} | Invalid Rows: {len(invalid_rows)}")

    # Master summary (all files)
    master = pd.DataFrame(all_results)
    master.to_csv(output_dir / "master_summary.csv", index=False)
    logger.info("Master summary with row-level stats saved successfully.")

if __name__ == "__main__":
    validate_all_files()
