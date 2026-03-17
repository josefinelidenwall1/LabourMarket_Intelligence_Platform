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

# Data Dictionary Swedish Labour Market Datasets

---

## Table of Contents

1. [aku_employment_stock](#1-aku_employment_stock)
2. [aku_population_region](#2-aku_population_region)
3. [aku_unemployed_age_sex](#3-aku_unemployed_age_sex)
4. [rams_employment](#4-rams_employment)
5. [wages_occupation_sector](#5-wages_occupation_sector)

---

## 1. aku_employment_stock

**Source:** SCB — Statistics Sweden, Labour Force Survey (AKU/LFS)

**Table ID:** `AM/AM0401/AM0401I/NAKUSysselYrke2012Ar`

**File:** `aku_employment_stock_occupation.csv`

**Coverage:** Employed persons aged 15–74

**Granularity:** Annual

**Years:** 2015–2025

**Unit:** Thousands of persons

### Columns

| Raw column              | Clean name           | Type         | Description                                          |
| ----------------------- | -------------------- | ------------ | ---------------------------------------------------- |
| `Anknytningsgrad`       | `attachment_code`    | string       | Raw code — degree of labour market attachment        |
| `Anknytningsgrad_label` | `attachment`         | string       | Human-readable attachment label                      |
| `Yrke`                  | `occupation_code`    | string       | SSYK 2012 occupation code                            |
| `Yrke_label`            | `occupation`         | string       | Occupation title                                     |
| `Kon`                   | `sex_code`           | string       | Sex code                                             |
| `Kon_label`             | `sex`                | string       | Sex label                                            |
| `Tid`                   | `year`               | int          | Year                                                 |
| `Tid_label`             | _(drop)_             | string       | Year display — duplicate of Tid, drop after renaming |
| `Employed persons`      | `employed_thousands` | float        | Estimated number of employed persons                 |
| `Margin of error ±`     | `margin_of_error`    | float / null | LFS sampling margin of error                         |
| `dataset`               | `source`             | string       | Source label added during fetch                      |

### Key Values

**Anknytningsgrad (attachment)**

| Code      | Label            |
| --------- | ---------------- |
| `ANSTTOT` | Employees, total |

> Run key printer on this table to retrieve all remaining attachment codes.

**Yrke (occupation — SSYK 2012)**

| Code   | Label                       |
| ------ | --------------------------- |
| `0000` | All occupations (aggregate) |

> ~120 three-digit SSYK 2012 codes. Full list available via metadata endpoint.

**Kon (sex)**

| Code | Label |
| ---- | ----- |
| `1`  | Men   |
| `2`  | Women |

### Notes

- `..` = suppressed estimate (unreliable due to small sample) — treat as null during cleaning
- `0000` in Yrke is the aggregate row — exclude when analysing per occupation
- Values are in **thousands** — multiply by 1,000 to get headcount

---

## 2. aku_population_region

**Source:** SCB — Statistics Sweden, Labour Force Survey (AKU/LFS)

**Table ID:** `AM/AM0401/AM0401N/NAKUBefolkningLAr`

**File:** `aku_population_region_labourstatus.csv`

**Coverage:** Population aged 15–74 by region and labour force status

**Granularity:** Annual

**Years:** 2005–2025

**Unit:** Thousands of persons / percent

### Columns

| Raw column                  | Clean name             | Type         | Description                                          |
| --------------------------- | ---------------------- | ------------ | ---------------------------------------------------- |
| `Region`                    | `region_code`          | string       | County code                                          |
| `Region_label`              | `region`               | string       | County name                                          |
| `Arbetskraftstillh`         | `labour_status_code`   | string       | Labour force status — raw code                       |
| `Arbetskraftstillh_label`   | `labour_status`        | string       | Labour force status label                            |
| `Kon`                       | `sex_code`             | string       | Sex code                                             |
| `Kon_label`                 | `sex`                  | string       | Sex label                                            |
| `Tid`                       | `year`                 | int          | Year                                                 |
| `Tid_label`                 | _(drop)_               | string       | Year display — duplicate of Tid, drop after renaming |
| `Thousands`                 | `population_thousands` | float        | Population count in thousands                        |
| `Margin of error ±, 1000s`  | `margin_thousands`     | float / null | Sampling error for thousands figure                  |
| `Percent`                   | `share_pct`            | float        | Share of labour force (%)                            |
| `Margin of error ± percent` | `margin_pct`           | float / null | Sampling error for percentage figure                 |
| `dataset`                   | `source`               | string       | Source label added during fetch                      |

### Key Values

**Region**

| Code | Label                  |
| ---- | ---------------------- |
| `00` | Sweden (all regions)   |
| `01` | Stockholm county       |
| `03` | Uppsala county         |
| `04` | Södermanland county    |
| `05` | Östergötland county    |
| `06` | Jönköping county       |
| `07` | Kronoberg county       |
| `08` | Kalmar county          |
| `09` | Gotland county         |
| `10` | Blekinge county        |
| `12` | Skåne county           |
| `13` | Halland county         |
| `14` | Västra Götaland county |
| `17` | Värmland county        |
| `18` | Örebro county          |
| `19` | Västmanland county     |
| `20` | Dalarna county         |
| `21` | Gävleborg county       |
| `22` | Västernorrland county  |
| `23` | Jämtland county        |
| `24` | Västerbotten county    |
| `25` | Norrbotten county      |

**Arbetskraftstillh (labour status)**

| Code     | Label                           |
| -------- | ------------------------------- |
| `TOTALT` | Total population (all statuses) |

> Run key printer to retrieve all status codes (employed / unemployed / outside labour force).

### Notes

- To isolate unemployed: filter `labour_status_label = "unemployed"` after cleaning
- `..` = suppressed — treat as null
- Values are in **thousands**

---

## 3. aku_unemployed_age_sex

**Source:** SCB — Statistics Sweden, Labour Force Survey (AKU/LFS)

**Table ID:** `AM/AM0401/AM0401L/NAKUArblheltidstudAr`

**File:** `aku_unemployed_age_sex.csv`

**Coverage:** Unemployed persons aged 15–74, national totals only

**Granularity:** Annual

**Years:** 2001–2025

**Unit:** Thousands of persons / percent

### Columns

| Raw column                  | Clean name              | Type         | Description                                          |
| --------------------------- | ----------------------- | ------------ | ---------------------------------------------------- |
| `Arbetskraftstillh`         | `labour_status_code`    | string       | Labour force status — raw code                       |
| `Arbetskraftstillh_label`   | `labour_status`         | string       | Labour force status label                            |
| `Kon`                       | `sex_code`              | string       | Sex code                                             |
| `Kon_label`                 | `sex`                   | string       | Sex label                                            |
| `Alder`                     | `age_group_code`        | string       | Age group code                                       |
| `Alder_label`               | `age_group`             | string       | Age group label                                      |
| `Tid`                       | `year`                  | int          | Year                                                 |
| `Tid_label`                 | _(drop)_                | string       | Year display — duplicate of Tid, drop after renaming |
| `1000s`                     | `unemployed_thousands`  | float        | Unemployed persons in thousands                      |
| `Margin of error ±, 1000s`  | `margin_thousands`      | float / null | Sampling error for thousands figure                  |
| `Percent`                   | `unemployment_rate_pct` | float        | Unemployment rate (%)                                |
| `Margin of error ± percent` | `margin_pct`            | float / null | Sampling error for rate                              |
| `dataset`                   | `source`                | string       | Source label added during fetch                      |

### Key Values

**Arbetskraftstillh (labour status)**

| Code   | Label      |
| ------ | ---------- |
| `ALÖS` | Unemployed |

**Alder (age group)**

| Code    | Label       |
| ------- | ----------- |
| `15-24` | 15–24 years |

> Run key printer to retrieve all age group codes.

### Notes

- No occupation or region dimension — **national totals only**
- Use alongside `aku_employment_stock` for occupation-level analysis
- `..` = suppressed — treat as null

---

## 4. rams_employment

**Source:** SCB — Statistics Sweden, Occupational Register (RAMS)

**Table IDs:**

| Period    | Table ID                      | File                 |
| --------- | ----------------------------- | -------------------- |
| 2016–2018 | `AM/AM0208/AM0208M/YREG60`    | `rams_2016_2018.csv` |
| 2019–2021 | `AM/AM0208/AM0208M/YREG60N`   | `rams_2019_2021.csv` |
| 2022–2024 | `AM/AM0208/AM0208M/YREG60BAS` | `rams_2022_2024.csv` |

**Coverage:** Employees aged 16–64, register-based

**Granularity:** Annual

**Years:** 2016–2024 (across three tables)

**Unit:** Number of persons (headcount)

### Columns

| Raw column       | Clean name        | Type   | Description                                          |
| ---------------- | ----------------- | ------ | ---------------------------------------------------- |
| `Region`         | `region_code`     | string | County code of workplace                             |
| `Region_label`   | `region`          | string | County name                                          |
| `Yrke2012`       | `occupation_code` | string | SSYK 2012 occupation code (4-digit)                  |
| `Yrke2012_label` | `occupation`      | string | Occupation title                                     |
| `Kon`            | `sex_code`        | string | Sex code                                             |
| `Kon_label`      | `sex`             | string | Sex label                                            |
| `Tid`            | `year`            | int    | Year                                                 |
| `Tid_label`      | _(drop)_          | string | Year display — duplicate of Tid, drop after renaming |
| `Number`         | `employed_count`  | int    | Number of employees (headcount)                      |
| `dataset`        | `source`          | string | Source label — indicates which table period          |

### Key Values

**Region** — same county codes as [aku_population_region](#2-aku_population_region) above.

**Yrke2012 (occupation — SSYK 2012, 4-digit)**

| Code   | Label                                  |
| ------ | -------------------------------------- |
| `0110` | Commissioned armed forces officers     |
| `0210` | Non-commissioned armed forces officers |
| `0310` | Armed forces occupation, other ranks   |
| `1111` | Legislators                            |
| `1112` | Senior government officials            |

> ~400 four-digit codes. Full list returned by metadata endpoint.

**Kon (sex)**

| Code | Label |
| ---- | ----- |
| `1`  | Men   |
| `2`  | Women |

### Notes

- SSYK 2012 coverage starts **2014** — do not compare with pre-2014 data
- Three separate table versions cover the full 2016–2024 range — stack CSVs after cleaning
- Unlike AKU, values are **headcounts** (not thousands)
- `00` in Region = all Sweden aggregate

---

## 5. wages_occupation_sector

**Source:** SCB — Statistics Sweden, Wage Structure Statistics

**Table IDs:**

| Period    | Table ID                                 | File                  |
| --------- | ---------------------------------------- | --------------------- |
| 2016–2022 | `AM/AM0110/AM0110A/LoneSpridSektorYrk4A` | `wages_2016_2022.csv` |
| 2023–2024 | `AM/AM0110/AM0110A/LoneSpridSektYrk4AN`  | `wages_2023_2024.csv` |

**Coverage:** All employees by sector and occupation

**Granularity:** Annual

**Years:** 2016–2024 (across two tables)

**Unit:** SEK per month

### Columns — 2016–2022

| Raw column        | Clean name        | Type   | Description                          |
| ----------------- | ----------------- | ------ | ------------------------------------ |
| `Sektor`          | `sector_code`     | string | Sector code                          |
| `Sektor_label`    | `sector`          | string | Sector name                          |
| `Yrke2012`        | `occupation_code` | string | SSYK 2012 occupation code            |
| `Yrke2012_label`  | `occupation`      | string | Occupation title                     |
| `Kon`             | `sex_code`        | string | Sex code                             |
| `Kon_label`       | `sex`             | string | Sex label                            |
| `Tid`             | `year`            | int    | Year                                 |
| `Tid_label`       | _(drop)_          | string | Year display — drop after renaming   |
| `Monthly salary`  | `wage_mean`       | int    | Average monthly salary (SEK)         |
| `Median`          | `wage_median`     | int    | Median monthly salary (SEK)          |
| `10th percentile` | `wage_p10`        | int    | 10th percentile monthly salary (SEK) |
| `25th percentile` | `wage_p25`        | int    | 25th percentile monthly salary (SEK) |
| `75th percentile` | `wage_p75`        | int    | 75th percentile monthly salary (SEK) |
| `90th percentile` | `wage_p90`        | int    | 90th percentile monthly salary (SEK) |
| `dataset`         | `source`          | string | Source label                         |

### Columns — 2023–2024 (extended — adds confidence intervals)

All columns from 2016–2022 are present, plus:

| Raw column                                                                | Clean name         | Type       | Description            |
| ------------------------------------------------------------------------- | ------------------ | ---------- | ---------------------- |
| `Monthly salary, 95 percent confidence interval`                          | `wage_mean_ci95`   | int / null | 95% CI for mean salary |
| `Median, 95 percent confidence interval`                                  | `wage_median_ci95` | int / null | 95% CI for median      |
| `Average monthly salary, 10th percentile, 95 percent confidence interval` | `wage_p10_ci95`    | int / null | 95% CI for p10         |
| `Average monthly salary, 25th percentile, 95 percent confidence interval` | `wage_p25_ci95`    | int / null | 95% CI for p25         |
| `Average monthly salary, 75th percentile, 95 percent confidence interval` | `wage_p75_ci95`    | int / null | 95% CI for p75         |
| `Average monthly salary, 90th percentile, 95 percent confidence interval` | `wage_p90_ci95`    | int / null | 95% CI for p90         |

### Key Values

**Sektor (sector)**

| Code | Label       |
| ---- | ----------- |
| `0`  | All sectors |

> Run key printer to retrieve all sector codes (e.g. state, municipality, private).

**Yrke2012 (occupation)**

| Code   | Label                       |
| ------ | --------------------------- |
| `0000` | All occupations (aggregate) |

> ~400 four-digit SSYK 2012 codes.

**Kon (sex)**

| Code | Label |
| ---- | ----- |
| `1`  | Men   |
| `2`  | Women |

### Notes

- Values are in **SEK per month**
- `..` = suppressed — treat as null
- `0000` in Yrke2012 = aggregate row — exclude when analysing per occupation
- Methodology break in **2018** due to AID code updates for municipalities — compare pre/post 2018 wage figures with caution
- 2023–2024 table includes confidence intervals not present in 2016–2022 — align column schema when stacking

---

## Cross-table Reference

| Shared key                   | Tables                                                         | Notes                                                                              |
| ---------------------------- | -------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `occupation_code`(SSYK 2012) | rams_employment, aku_employment_stock, wages_occupation_sector | Use for occupation-level joins.`0000`= aggregate in AKU/wages; not present in RAMS |
| `region_code`                | rams_employment, aku_population_region                         | County codes 00–25. RAMS uses workplace region; AKU uses residence region          |
| `sex_code`                   | all tables                                                     | 1 = men, 2 = women                                                                 |
| `year`                       | all tables                                                     | Annual. RAMS split across 3 table versions; wages split across 2                   |

## Known Limitations

| Limitation                                 | Affected tables                                                        |
| ------------------------------------------ | ---------------------------------------------------------------------- |
| No unemployment × occupation cross         | AKU — LFS sample too small for reliable estimates at that intersection |
| SSYK 2012 break at 2014                    | RAMS, wages, AKU — do not compare with pre-2014 occupation data        |
| AKU values in thousands, RAMS in headcount | Do not mix units without conversion                                    |
| Wage methodology break in 2018             | wages_occupation_sector                                                |
| `..`suppressed values throughout           | All AKU tables                                                         |
