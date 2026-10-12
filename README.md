# UK Regional Labour Dynamics ETL Pipeline

An automated batch ETL (Extract, Transform, Load) data engineering pipeline built in Python to ingest, parse, and harmonise complex administrative data catalogues from the UK Office for National Statistics (ONS).

## Live Interactive Visualisation
The production-ready output of this data engine is hosted as a client-ready executive dashboard on Tableau Public:
(https://public.tableau.com/app/profile/milan.gorasia/viz/UKRegionalEarningsLabourMarketDynamics/UKRegionalEarningsLabourMarketDynamics)

## The Business Problem
UK municipal economic reports are highly fragmented across hundreds of individual worksheets. If an enterprise wants to evaluate regional cost boundaries or labour efficiency vectors, gathering data manually is error-prone. This pipeline provides an automated, scalable data schema comparing **Average Weekly Income vs. Productive Working Hours** across all macro UK administrative territories.

## Technical Architecture & Pipeline Strategy
* **Automated Batch Processing:** Loops dynamically through dozens of unformatted `.xlsx` and `.csv` system logs simultaneously.
* **Self-Healing Row Mapping:** Deploys a scanning mechanism to dynamically locate shifting data headers across changing government layouts, bypassing blank cells and text footnotes on the fly.
* **Data Harmonisation:** Leverages `pandas` to standardise naming metrics, scrub text anomalies, drop numerical null properties, and isolate the core macro-regional workforce cohorts.

## Tech Stack & Libraries Used
* **Backend Pipeline Engine:** Python 3
* **Data Wrangling & Manipulation:** Pandas
* **File Directory I/O Systems:** Glob, OS
* **Enterprise Reporting Layer:** Tableau Public

## Output Framework
The pipeline consolidates over 14,000 messy, fragmented records into a single, structured database schema:
* `Description`: The targeted geographic UK macro-region.
* `Code`: Standard ONS municipal administrative code.
* `Median / Mean`: Standardised financial and productivity metrics.
* `Source_File`: Dynamically injected file-origin label.
* `Age_Group`: Disaggregated demographic marker extracted from sheet tab indexes.
