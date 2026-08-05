# Manual Review Answer

## Question

Why is manual investigation still required even when automated validation exists?

## Answer

Automated validation can identify whether two computed metrics differ beyond an acceptable threshold, but it cannot determine the underlying business reason for the difference.

Manual investigation is required to:

- Verify data quality issues.
- Identify missing or duplicate records.
- Check whether business rules changed.
- Confirm SQL and Python implementations follow the same logic.
- Determine whether discrepancies are expected or indicate real data problems.

Automated validation detects problems.

Manual review explains why the problems occurred.