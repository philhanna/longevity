# longevity

Calculates life expectancy according to the Social Security Administration website.

## Installation

### macOS / Linux

```bash
# Clone the repository
git clone https://github.com/philhanna/life_expectancy.git
cd life_expectancy

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the package and its dependencies
pip install .

# Symlink the CLIs into ~/.local/bin so they are available outside the venv.
# ~/.local/bin is on PATH by default on most Linux distros and macOS (via .profile).
mkdir -p ~/.local/bin
ln -sf "$(pwd)/venv/bin/longevity"       ~/.local/bin/longevity
ln -sf "$(pwd)/venv/bin/longevity-batch" ~/.local/bin/longevity-batch
```

If `~/.local/bin` is not yet on your PATH, add the following line to `~/.bashrc` or `~/.zshrc` and restart your shell:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Windows

Run the following commands in PowerShell:

```powershell
# Clone the repository
git clone https://github.com/philhanna/life_expectancy.git
cd life_expectancy

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\Activate.ps1

# Install the package and its dependencies
pip install .

# Add the venv's Scripts folder to your user PATH so the CLIs are
# available in any new shell without activating the venv first.
$scripts = "$PWD\venv\Scripts"
[Environment]::SetEnvironmentVariable(
    "PATH",
    "$([Environment]::GetEnvironmentVariable('PATH','User'));$scripts",
    "User"
)
```

Open a new PowerShell window after the PATH change for it to take effect.

## Usage

### Date formats

Both CLIs accept dates of birth in any of the following formats:

| Format           | Example              |
|------------------|----------------------|
| `YYYY-MM-DD`     | `1957-12-18`         |
| `MM/DD/YYYY`     | `12/18/1957`         |
| `DD/MM/YYYY`     | `18/12/1957`         |
| `Month DD, YYYY` | `December 18, 1957`  |
| `Mon DD, YYYY`   | `Dec 18, 1957`       |
| `DD Month YYYY`  | `18 December 1957`   |
| `DD Mon YYYY`    | `18 Dec 1957`        |
| `DD-Month-YYYY`  | `18-December-1942`   |
| `DD-Mon-YYYY`    | `18-Jun-1942`        |

Formats are tried in the order shown; the first match wins. To pin a specific
format in the batch CLI, use `--date-fmt` with a `strptime` format string
(e.g. `--date-fmt "%d/%m/%Y"`).

### Single record

```
longevity <sex> <dob>
```

`sex` is `m` or `f`. `dob` accepts many formats (`YYYY-MM-DD`, `MM/DD/YYYY`, `December 18, 1957`, etc.).

```bash
longevity m 1957-12-18
# current age      = 68.40
# additional years = 16.20
# total years      = 84.60
# estimated death  = 2042-06-19
```

### Batch CSV

```
longevity-batch <input.csv> <output.csv> [--sex-col COL] [--dob-col COL] [--date-fmt FMT]
```

Reads a CSV with at least a sex column and a date-of-birth column, calls the SSA
calculator for each row, and writes all original columns plus
`current_age`, `additional_years`, `total_years`, `estimated_death_date`, and `error`
to the output CSV.

```bash
longevity-batch people.csv results.csv --sex-col Sex --dob-col DOB
```

## References

- [Github repository](https://github.com/philhanna/life_expectancy)
- [Social Security Administration website for calculator](https://www.ssa.gov/oact/population/longevity.html)

## Architecture

The project follows a hexagonal (ports and adapters) architecture.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          DRIVING SIDE (Inbound)                            ║
║                                                                            ║
║   ┌─────────────────────────────────────────────────────────────────────┐  ║
║   │  cli.py  ·  main()                                                  │  ║
║   │  Parses argv → calls get_life_expectancy() → prints result          │  ║
║   │                                                                     │  ║
║   │  csv_cli.py  ·  main()                                              │  ║
║   │  Reads input CSV → calls get_life_expectancy() per row → writes CSV │  ║
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
║   longevity.ports package  (Protocols = interfaces)                        ║
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
only on the `Protocol` ports defined in the `longevity.ports` package. The concrete
`RequestsLongevityFetcher`, `Bs4LongevityParser`, and `SystemClock` are injected
as defaults but can be swapped out freely (e.g. with fakes in tests).
