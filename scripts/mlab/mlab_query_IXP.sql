-- SELECT  ndt.*
SELECT  ndt.client.Geo.CountryCode          client_country_code,
        ndt.client.Geo.Subdivision1ISOCode  client_subdivision,
        ndt.client.Geo.City                 client_city,
        ndt.client.Geo.Latitude             client_latitude,
        ndt.client.Geo.Longitude            client_longitude,
        ndt.client.Geo.AccuracyRadiusKm     client_accuracy_radius_km,
        ndt.client.Network.ASNumber         client_ASNumber,
        ndt.client.Network.ASName           client_ASName,
        --
        ndt.server.Geo.CountryCode          server_country_code,
        ndt.server.Geo.Subdivision1ISOCode  server_subdivision,
        ndt.server.Geo.City                 server_city,
        ndt.server.Geo.Latitude             server_latitude,
        ndt.server.Geo.Longitude            server_longitude,
        ndt.server.Geo.AccuracyRadiusKm     server_accuracy_radius_km,
        ndt.server.Network.ASNumber         server_ASNumber,
        ndt.server.Network.ASName           server_ASName,
        --
        -- ndt.date                            test_date,                   ,
        ndt.a.TestTime                      test_date_time,
        ndt.a.MeanThroughputMbps            test_mean_throughput_mbps,
        ndt.a.MinRTT                        test_minrtt

FROM    `ndt.unified_downloads` as ndt

WHERE   1 = 1
AND     ndt.date BETWEEN "2024-01-01" AND "2024-12-31"
AND     client.Geo.CountryCode          = 'US'
AND     client.Geo.Subdivision1ISOCode  = 'CA'