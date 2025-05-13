-- Description: This script queries the M-Lab dataset for county-wise measurement data from 2020 to 2024 throughout the US.
-- Run only on M-Lab's BigQuery dataset.

SELECT  FORMAT_DATE('%Y', counties.date)     year,
        counties.GEOID                       geoid,
        counties.state_fips_code             state,
        counties.county_name                 county,
        AVG(counties.download_MIN)           download_min,
        AVG(counties.upload_MIN)             upload_min,
        AVG(counties.download_AVG)           download_avg,
        AVG(counties.upload_AVG)             upload_avg,
        AVG(counties.download_MAX)           download_max,
        AVG(counties.upload_MAX)             upload_max,
        AVG(counties.dl_minRTT_LOG_AVG_rnd1) download_minRTT_r1,
        AVG(counties.dl_minRTT_LOG_AVG_rnd2) download_minRTT_r2,
        AVG(counties.ul_minRTT_LOG_AVG_rnd1) upload_minRTT_r1,
        AVG(counties.ul_minRTT_LOG_AVG_rnd2) upload_minRTT_r2,
        COUNT(*)                             num_of_measurements_daily_sampled
FROM    `statistics.v0_us_counties`          counties
WHERE   counties.country_code             = "US"
AND     counties.date BETWEEN '2020-01-01' AND '2024-12-31'
GROUP BY  year,
          geoid,
          state,
          county
ORDER BY  year,
          geoid,
          state,
          county
