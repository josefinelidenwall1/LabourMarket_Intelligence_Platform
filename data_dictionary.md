# Data Dictionary


Note

Source file SCB edu_region is encoded in `ISO-8859-1` (Latin-1), important to take this into consideration during ingestion in ADF setup:

* **Source Dataset:** Set to `ISO-889-1`.
* **Sink Dataset:** Set to `UTF-8`.



| Source         | **Raw field name**                            | **Business name** | **Data type** | **Notes**                          |
| -------------- | --------------------------------------------------- | ----------------------- | ------------------- | ---------------------------------------- |
| SCB edu_region | `kön`                                            | `gender`              | **String**    | Contains "män", "kvinnor", and "totalt" |
| SCB edu_region | `region där utbildningen bedrivs`                | `region_name`         | **String**    | Includes code and region name            |
| SCB edu_region | `år`                                             | `year`                | **Int**       |                                          |
| SCB edu_region | `tabellinnehåll`                                 | `measure_type`        | **String**    | Type of student - set as graduated?      |
| SCB edu_region | `Studerande och examinerade inom yrkeshögskolan` | `nr_graduated`        | **String**    | Need to transform to INT                 |
| SCB edu_topic  | `kön`                                            | `gender`              | String              |                                          |
| SCB edu_topic  | `utbildningens inriktning`                        | `education_subject`   | String              |                                          |
| SCB edu_topic  | `ålder`                                          | `age`                 | String              | Age spans                                |
| SCB edu_topic  | `år`                                             | `year`                | Int                 |                                          |
| SCB edu_topic  | `tabellinnehåll`                                 | `measure_type`        | String              | Type of student - set as graduated?      |
| SCB edu_topic  | `Studerande och examinerade inom yrkeshögskolan` | `nr_graduated`        | String              |                                          |
|                |                                                     |                         |                     |                                          |
|                |                                                     |                         |                     |                                          |
