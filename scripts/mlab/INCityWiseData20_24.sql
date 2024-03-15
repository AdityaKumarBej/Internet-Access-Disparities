select  FORMAT_DATE('%Y', cities.date)     year,
        cities.country_code                country,
        cities.ISO3166_2region1            state,
        cities.city                        city,
        avg(cities.download_MIN)           download_min,
        avg(cities.upload_MIN)             upload_min,
        avg(cities.download_AVG)           download_avg,
        avg(cities.upload_AVG)             upload_avg,
        avg(cities.download_MAX)           download_max,
        avg(cities.upload_MAX)             upload_max,
        avg(cities.dl_minRTT_LOG_AVG_rnd1) download_minRTT_r1,
        avg(cities.dl_minRTT_LOG_AVG_rnd2) download_minRTT_r2,
        avg(cities.ul_minRTT_LOG_AVG_rnd1) upload_minRTT_r1,
        avg(cities.ul_minRTT_LOG_AVG_rnd2) upload_minRTT_r2,
        count(*)                           num_of_measurements_daily_sampled
FROM    `statistics.v0_cities`             cities
WHERE   cities.country_code                = 'IN'
AND     ISO3166_2region1 IN ('IN-AP', 'IN-AR', 'IN-AS', 'IN-BR', 'IN-CG','IN-GA', 'IN-GJ', 'IN-HR', 'IN-HP',  'IN-JH', 'IN-KA', 'IN-KL', 'IN-MP', 'IN-MH', 'IN-MN', 'IN-ML', 'IN-MZ', 'IN-NL', 'IN-OD', 'IN-PB', 'IN-RJ', 'IN-SK', 'IN-TN', 'IN-TS', 'IN-TR', 'IN-UP', 'IN-UK', 'IN-WB', 'IN-AN', 'IN-CH', 'IN-DH', 'IN-DL',   'IN-JK',  'IN-LA', 'IN-LD', 'IN-PY'
)
AND     cities.date BETWEEN '2020-01-01' AND '2024-12-31'
GROUP BY  year,
          country,
          state,
          city
ORDER BY  year,
          country,
          state,
          city
