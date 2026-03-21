# longevity

Calculates life expectancy according to the Social Security Administration website.

## References

- [Github repository](https://github.com/philhanna/life_expectancy)
- [Social Security Administration website for calculator](https://www.ssa.gov/oact/population/longevity.html)

## Gists

## Architecture

The project follows a hexagonal (ports and adapters) architecture.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          DRIVING SIDE (Inbound)                            ║
║                                                                            ║
║   ┌─────────────────────────────────────────────────────────────────────┐  ║
║   │  cli.py  ·  main()                                                  │  ║
║   │  Parses argv → calls get_life_expectancy() → prints result          │  ║
║   └──────────────────────────────┬──────────────────────────────────────┘  ║
╚══════════════════════════════════│═════════════════════════════════════════╝
                                   │
╔══════════════════════════════════▼═════════════════════════════════════════╗
║                        APPLICATION LAYER                                   ║
║                                                                            ║
║   ┌──────────────────────────────────────────────────────────────────────┐ ║
║   │  use_cases.py  ·  get_life_expectancy(sex, dob, *, fetcher,          │ ║
║   │                                       parser, clock)                 │ ║
║   │                                                                      │ ║
║   │  1. _validate_inputs()                                               │ ║
║   │  2. fetcher.fetch()   ──► LongevityHtmlFetcher port                  │ ║
║   │  3. parser.parse()    ──► LongevityHtmlParser  port                  │ ║
║   │  4. clock.now()       ──► Clock               port                  │ ║
║   │  5. builds LifeExpectancy and returns it                             │ ║
║   └──────────────────────────────────────────────────────────────────────┘ ║
║                                                                            ║
║   ports.py  (Protocols = interfaces)                                       ║
║   ┌─────────────────────┐  ┌──────────────────────┐  ┌─────────────────┐  ║
║   │ LongevityHtmlFetcher│  │ LongevityHtmlParser  │  │     Clock       │  ║
║   │ fetch(sex,dob)->str │  │ parse(html)->        │  │ now()->datetime │  ║
║   │                     │  │  (float,float,float) │  │                 │  ║
║   └─────────┬───────────┘  └──────────┬───────────┘  └────────┬────────┘  ║
╚═════════════│══════════════════════════│════════════════════════│══════════╝
              │                          │                        │
╔═════════════▼══════════════════════════▼════════════════════════▼══════════╗
║                        DRIVEN SIDE (Outbound Adapters)                     ║
║                                                                            ║
║   ┌─────────────────────┐  ┌──────────────────────┐  ┌─────────────────┐  ║
║   │RequestsLongevity    │  │  Bs4LongevityParser  │  │  SystemClock    │  ║
║   │Fetcher              │  │                      │  │                 │  ║
║   │                     │  │  parse_current_age() │  │  now() →        │  ║
║   │ HTTP POST to        │  │  BeautifulSoup HTML  │  │  datetime.now() │  ║
║   │ ssa.gov CGI         │  │  table scraper       │  │                 │  ║
║   └─────────────────────┘  └──────────────────────┘  └─────────────────┘  ║
╚═══════════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════════╗
║                          DOMAIN LAYER                                     ║
║                                                                           ║
║   models.py                          services.py                          ║
║   ┌───────────────────────────┐      ┌────────────────────────────────┐   ║
║   │ LifeExpectancy (frozen    │      │ parse_float(text) -> float     │   ║
║   │   dataclass)              │      │ almost_equal(a, b) -> bool     │   ║
║   │                           │      │                                │   ║
║   │  current_age:    float    │      │ (pure functions, no I/O)       │   ║
║   │  additional_years: float  │      └────────────────────────────────┘   ║
║   │  total_years:    float    │                                           ║
║   │  estimated_death_date:    │                                           ║
║   │    datetime               │                                           ║
║   └───────────────────────────┘                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

Data flow:
  argv ──► cli ──► get_life_expectancy ──► fetcher ──► ssa.gov (HTTP POST)
                         │                                    │
                         │◄──────── raw HTML ◄────────────────┘
                         │
                         ├──► parser ──► LifeExpectancy (domain model)
                         │
                         └──► clock ──► estimated_death_date
```

`get_life_expectancy` never imports concrete adapters at the type level — it depends
only on the `Protocol` ports defined in `ports.py`. The concrete
`RequestsLongevityFetcher`, `Bs4LongevityParser`, and `SystemClock` are injected
as defaults but can be swapped out freely (e.g. with fakes in tests).
