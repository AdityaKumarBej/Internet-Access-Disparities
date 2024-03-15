SELECT  FORMAT_DATE('%Y', counties.date)     year,
        counties.GEOID                       geoid,
        counties.state_fips_code             state,
        counties.county_name                 county,
        avg(counties.download_MIN)           download_min,
        avg(counties.upload_MIN)             upload_min,
        avg(counties.download_AVG)           download_avg,
        avg(counties.upload_AVG)             upload_avg,
        avg(counties.download_MAX)           download_max,
        avg(counties.upload_MAX)             upload_max,
        avg(counties.dl_minRTT_LOG_AVG_rnd1) download_minRTT_r1,
        avg(counties.dl_minRTT_LOG_AVG_rnd2) download_minRTT_r2,
        avg(counties.ul_minRTT_LOG_AVG_rnd1) upload_minRTT_r1,
        avg(counties.ul_minRTT_LOG_AVG_rnd2) upload_minRTT_r2,
        count(*)                             number_of_measurements
FROM    `statistics.v0_us_counties`          counties
WHERE   counties.country_code             = "US"
-- AND     counties.state                 = "US-AL"
-- AND     counties.county_name           = "Autauga"
AND     counties.date BETWEEN '2020-01-01' AND '2024-12-31'
GROUP BY  year,
          geoid,
          state,
          county
ORDER BY  year,
          geoid,
          state,
          county
