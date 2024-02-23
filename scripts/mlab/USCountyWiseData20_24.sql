SELECT  FORMAT_DATE('%G', counties.date)     year,
        states.GEOID                         geoid,
        states.state_name                    state,
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
        avg(counties.ul_minRTT_LOG_AVG_rnd2) upload_minRTT_r2 
        
FROM    `statistics.v0_us_states`            states,
        `statistics.v0_us_counties`          counties

WHERE   states.GEOID  = counties.state_fips_code
AND     states.GEOID  BETWEEN '01' AND '56'  
AND     FORMAT_DATE('%G', counties.date) >= '2020'
AND     FORMAT_DATE('%G', counties.date) <= '2024'
AND     (
        FORMAT_DATE('%e', counties.date) = '01'
        OR
        FORMAT_DATE('%e', counties.date) = '15'
        OR
        FORMAT_DATE('%e', counties.date) = '30'
        )
GROUP BY  year,
          geoid,
          state,
          county
ORDER BY  year,
          geoid,
          state,
          county
