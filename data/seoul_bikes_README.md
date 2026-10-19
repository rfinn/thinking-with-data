# Seoul bike-sharing course snapshot

Source: [Seoul Bike Sharing Demand](https://doi.org/10.24432/C5F62R) (2020).
UCI Machine Learning Repository. Retrieved October 14, 2026.
License: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/).

`seoul_bikes.csv` retains all 8,760 observations and 14 columns from the UCI
archive member `SeoulBikeData.csv`. The course preparation decodes the source
file and gives columns simpler names. No observations are removed, no values
are imputed, and recorded zeros are preserved. Dates remain day/month/year text.

One row is one recorded system-wide hour, from December 1, 2017 through
November 30, 2018. The file contains hourly rentals, weather measurements,
season, holiday status, and whether the service was operating. These data
describe recorded use, rather than unmet demand or individual riders.

Columns are `date`, `rentals`, `hour`, `temperature_c`, `humidity_pct`,
`wind_speed_ms`, `visibility_10m`, `dew_point_c`, `solar_radiation_mjm2`,
`rainfall_mm`, `snowfall_cm`, `season`, `holiday`, and `operating`.

Temperature and dew point are degrees Celsius; humidity is percent; wind speed
is m/s; visibility is tens of metres; solar radiation is MJ/m²; rainfall is mm;
snowfall is cm. The source's category values are retained.

Prepared CSV SHA-256:
`fb0b5405e37779e0b690e1b6990f99997101ea3eed2abcf62d561731db29cda1`
