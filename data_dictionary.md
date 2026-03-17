# Data Dictionary


Note

Source file SCB edu_region is encoded in `ISO-8859-1` (Latin-1), important to take this into consideration during ingestion in ADF setup:

* **Source Dataset:** Set to `ISO-889-1`.
* **Sink Dataset:** Set to `UTF-8`.



| Data Source    | **Raw field name**                            | **Business name** | **Data type** | **Notes**                          |
| -------------- | --------------------------------------------------- | ----------------------- | ------------------- | ---------------------------------------- |
| SCB_yh_region  | `kön`                                            | `gender`              | **String**    | Contains "män", "kvinnor", and "totalt" |
| SCB_yh_region  | `region där utbildningen bedrivs`                | `region_name`         | **String**    | Includes code and region name            |
| SCB_yh_region  | `år`                                             | `year`                | **Int**       |                                          |
| SCB_yh_region  | `tabellinnehåll`                                 | `measure_type`        | **String**    | Type of student - set as graduated?      |
| SCB_yh_region  | `Studerande och examinerade inom yrkeshögskolan` | `nr_graduated`        | **String**    | Need to transform to INT                 |
| SCB_yh_topic   | `kön`                                            | `gender`              | String              |                                          |
| SCB_yh_topic   | `utbildningens inriktning`                        | `education_subject`   | String              |                                          |
| SCB_yh_topic   | `ålder`                                          | `age`                 | String              | Age spans                                |
| SCB_yh_topic   | `år`                                             | `year`                | Int                 |                                          |
| SCB_yh_topic   | `tabellinnehåll`                                 | `measure_type`        | String              | Type of student - set as graduated?      |
| SCB_yh_topic   | `Studerande och examinerade inom yrkeshögskolan` | `nr_graduated`        | String              |                                          |
| UKÄ_uni_topic | `Tidsperiod`                                      | `year`                | string              | Need transforming to INT                 |
| UKÄ_uni_topic | `Lärosäte`                                      | `n/a`                 |                     | Can remove                               |
| UKÄ_uni_topic | `Examen`                                          | `course_type`         | string              | Includes "Kandidat", "Master" etc.      |
| UKÄ_uni_topic | `Huvudinriktning`                                 | `education_topic`     | string              |                                          |
| UKÄ_uni_topic | `Huvudområdesgrupp`                              | `education_subject`   | string              |                                          |
| UKÄ_uni_topic | `Kön`                                            | `gender`              | string              |                                          |
| UKÄ_uni_topic | `Åldersgrupp`                                    | `n/a`                 | string              | Remove                                   |
| UKÄ_uni_topic | `Värde`                                          | `nr_graduated`        | string              | Transform to INT                         |
