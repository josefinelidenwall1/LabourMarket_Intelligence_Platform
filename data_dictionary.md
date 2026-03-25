# Data Dictionary

Note

Source file SCB edu_region is encoded in `ISO-8859-1` (Latin-1), important to take this into consideration during ingestion in ADF setup:

- **Source Dataset:** Set to `ISO-889-1`.
- **Sink Dataset:** Set to `UTF-8`.

| Data Source   | **Raw field name**                               | **Business name**   | **Data type** | **Notes**                               |
| ------------- | ------------------------------------------------ | ------------------- | ------------- | --------------------------------------- |
| SCB_yh_region | `kön`                                            | `gender`            | **String**    | Contains "män", "kvinnor", and "totalt" |
| SCB_yh_region | `region där utbildningen bedrivs`                | `region_name`       | **String**    | Includes code and region name           |
| SCB_yh_region | `år`                                             | `year`              | **Int**       |                                         |
| SCB_yh_region | `tabellinnehåll`                                 | `measure_type`      | **String**    | Type of student - set as graduated?     |
| SCB_yh_region | `Studerande och examinerade inom yrkeshögskolan` | `nr_graduated`      | **String**    | Need to transform to INT                |
| SCB_yh_topic  | `kön`                                            | `gender`            | String        |                                         |
| SCB_yh_topic  | `utbildningens inriktning`                       | `education_subject` | String        |                                         |
| SCB_yh_topic  | `ålder`                                          | `age`               | String        | Age spans                               |
| SCB_yh_topic  | `år`                                             | `year`              | Int           |                                         |
| SCB_yh_topic  | `tabellinnehåll`                                 | `measure_type`      | String        | Type of student - set as graduated?     |
| SCB_yh_topic  | `Studerande och examinerade inom yrkeshögskolan` | `nr_graduated`      | String        |                                         |
| UKÄ_uni_topic | `Tidsperiod`                                     | `year`              | string        | Need transforming to INT                |
| UKÄ_uni_topic | `Lärosäte`                                       | `n/a`               |               | Can remove                              |
| UKÄ_uni_topic | `Examen`                                         | `course_type`       | string        | Includes "Kandidat", "Master" etc.      |
| UKÄ_uni_topic | `Huvudinriktning`                                | `education_topic`   | string        |                                         |
| UKÄ_uni_topic | `Huvudområdesgrupp`                              | `education_subject` | string        |                                         |
| UKÄ_uni_topic | `Kön`                                            | `gender`            | string        |                                         |
| UKÄ_uni_topic | `Åldersgrupp`                                    | `n/a`               | string        | Remove                                  |
| UKÄ_uni_topic | `Värde`                                          | `nr_graduated`      | string        | Transform to INT                        |

---

# SCB Silver Layer: Data Dictionary & Quality Caveats

## Known Caveats & Data Quality Rules

1. **Privacy Suppression (`NULL` Handling):** To protect privacy in groups with very few individuals, SCB masks granular data using symbols like `..`, `...`, or `.`. In the Silver layer, all suppressed metric values are strictly cast to `NULL`.
2. **Pre-aggregated Totals (The `1+2` Rule):** SCB often provides pre-calculated totals (e.g., `sex = '1+2'`) alongside granular rows (`1` and `2`). **These are intentionally kept in the Silver layer.** Because SCB suppresses low-count granular rows, deleting the `1+2` row in Silver would cause permanent data loss for total market sizing. BI-level filtering of these totals must be handled in the Gold layer.
3. **Strict Data Typing:** All dimensional attributes (e.g., `region`, `sex`, `year`) are stored as `STRING` to preserve SCB's exact formatting and leading zeros (e.g., region `00`). All factual metrics are cast to `DOUBLE`.

---

## Data Dictionary (silver) SCB wages data set

### 1. `wages`

**Description:** Monthly salary distributions, percentiles, and confidence intervals broken down by sector, occupation, sex, and year.

| Column Name                  | Data Type | Description                                                  |
| :--------------------------- | :-------- | :----------------------------------------------------------- |
| `sector`                     | STRING    | The sector of the labor market (e.g., public, private).      |
| `occupation_code`            | STRING    | The SSYK 2012 classification code for the profession.        |
| `gender`                     | STRING    | Gender code (`1` = Men, `2` = Women, `1+2` = Total).         |
| `year`                       | STRING    | The reporting year.                                          |
| `monthly_salary_avg`         | DOUBLE    | The average (mean) monthly salary.                           |
| `salary_median`              | DOUBLE    | The median (50th percentile) monthly salary.                 |
| `salary_p10`                 | DOUBLE    | The 10th percentile salary (bottom 10% earn less than this). |
| `salary_p25`                 | DOUBLE    | The 25th percentile salary (lower quartile).                 |
| `salary_p75`                 | DOUBLE    | The 75th percentile salary (upper quartile).                 |
| `salary_p90`                 | DOUBLE    | The 90th percentile salary (top 10% earn more than this).    |
| `monthly_salary_avg_ci95`    | DOUBLE    | 95% confidence interval margin for the average salary.       |
| `monthly_salary_median_ci95` | DOUBLE    | 95% confidence interval margin for the median salary.        |
| `salary_p10_ci95`            | DOUBLE    | 95% confidence interval margin for the 10th percentile.      |
| `salary_p25_ci95`            | DOUBLE    | 95% confidence interval margin for the 25th percentile.      |
| `salary_p75_ci95`            | DOUBLE    | 95% confidence interval margin for the 75th percentile.      |
| `salary_p90_ci95`            | DOUBLE    | 95% confidence interval margin for the 90th percentile.      |

### 2. `aku_employment`

**Description:** The total stock of employed persons (measured in thousands) broken down by occupation and sex, sourced from the Labour Force Surveys (AKU).

| Column Name          | Data Type | Description                                                                   |
| :------------------- | :-------- | :---------------------------------------------------------------------------- |
| `attachment_code`    | STRING    | Degree of attachment to the labor market (e.g.,`ANSTTOT` for total employed). |
| `occupation_code`    | STRING    | The SSYK 2012 classification code for the profession.                         |
| `gender`             | STRING    | Gender code (`1` = Men, `2` = Women, `1+2` = Total).                          |
| `year`               | STRING    | The reporting year.                                                           |
| `employed_thousands` | DOUBLE    | Number of employed persons, measured in thousands.                            |
| `moe_thousands`      | DOUBLE    | Margin of error for the employed count (in thousands).                        |

### 3. `aku_population`

**Description:** High-level labor force and population statistics broken down by geographic region and labor status.

| Column Name          | Data Type | Description                                                                                 |
| :------------------- | :-------- | :------------------------------------------------------------------------------------------ |
| `region`             | STRING    | Geographic region code (`00` typically represents all of Sweden).                           |
| `labour_status_code` | STRING    | Status in the labor market (e.g.,`TOTALT` for total population, `DAIR` for in labor force). |
| `gender`             | STRING    | Gender code (`1` = Men, `2` = Women, `1+2` = Total).                                        |
| `year`               | STRING    | The reporting year.                                                                         |
| `pop_thousands`      | DOUBLE    | Population count for the given slice, measured in thousands.                                |
| `moe_thousands`      | DOUBLE    | Margin of error for the population count (in thousands).                                    |
| `pop_percent`        | DOUBLE    | The percentage of the broader population this group represents.                             |
| `moe_percent`        | DOUBLE    | Margin of error for the percentage metric.                                                  |

### 4. `aku_unemployment`

**Description:** Unemployment figures and rates broken down by age group and sex.

| Column Name          | Data Type | Description                                                     |
| :------------------- | :-------- | :-------------------------------------------------------------- |
| `labour_status_code` | STRING    | Status in the labor market (primarily `ALOS` for unemployed).   |
| `gender`             | STRING    | Gender code (`1` = Men, `2` = Women, `1+2` = Total).            |
| `age_group`          | STRING    | The age bracket for the demographic (e.g.,`15-24`, `tot15-74`). |
| `year`               | STRING    | The reporting year.                                             |
| `unemp_thousands`    | DOUBLE    | Number of unemployed persons, measured in thousands.            |
| `moe_thousands`      | DOUBLE    | Margin of error for the unemployed count (in thousands).        |
| `unemp_percent`      | DOUBLE    | The unemployment rate as a percentage of the labor force.       |
| `moe_percent`        | DOUBLE    | Margin of error for the unemployment rate percentage.           |
