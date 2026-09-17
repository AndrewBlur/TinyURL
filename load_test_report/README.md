
## Version 1

Your app did not handle 10,000 simultaneous users successfully. The test found its breaking point.

| Result | What it means |
|---|---|
| 10,000 users | You simulated 10,000 people at once |
| 842,949 total requests | The app received a lot of traffic during the hour |
| ~211 requests/second | Actual completed throughput |
| 48,924 failed requests | About **5.8%** of requests failed |
| Typical response | Around **3 seconds** |
| 95% response time | Around **251 seconds** — over 4 minutes |
| Worst response | Around **1,503 seconds** — about 25 minutes |

The important conclusion: the app became overloaded. It kept accepting work, but requests piled up faster than it could finish them. That is why some users waited minutes, then some requests failed.


> “At 10,000 simulated concurrent users, the current local setup processed roughly 211 requests per second, but latency became unacceptable and about 5.8% of requests failed.”

The meaningful capacity is lower than 10,000 users. We should next test gradually—500, 1,000, 2,000, then 5,000 users—and identify the level where failures remain at 0 and the 95% response time stays reasonable. Then we can improve the specific bottlenecks.