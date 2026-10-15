# Auto MPG course snapshot

Source: Quinlan, R. (1993). [Auto MPG](https://doi.org/10.24432/C5859H).
UCI Machine Learning Repository. Retrieved October 14, 2026.
License: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/).

`auto_mpg.csv` retains all 398 observations and nine columns from the UCI archive
member `auto-mpg.data`. The preparation converts the source's `?` markers to
blank missing values and expands model-year codes by adding 1900. No observations
are removed and no missing measurements are filled. The UCI modified source
itself already excludes eight observations with unknown MPG.

Columns are `mpg`, `cylinders`, `displacement`, `horsepower`, `weight`,
`acceleration`, `model_year`, `origin`, and `car_name`.

- MPG is city-cycle fuel economy in miles per gallon.
- Horsepower has six missing values. All other columns are complete.
- Weight is pounds; displacement is cubic inches; acceleration is seconds to
  reach 60 mph. See the [variable documentation](https://search.r-project.org/CRAN/refmans/ISLR2/html/Auto.html)
  for units and origin labels; that package's reduced copy has different row counts.
- Origin codes are 1 = American, 2 = European, 3 = Japanese, following the source.
- Model years span 1970–1982. These recorded observations do not establish
  market shares or represent all current cars. Vehicle names are not unique IDs.

Prepared CSV SHA-256:
`f459c757f377f4f7f6405999d7478715a4484b85c725d455d307c39024f0223a`
