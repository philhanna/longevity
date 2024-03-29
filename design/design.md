# Design

## Processing overview:

### Collect the parameters
The parameters are the names and values of the input fields.

#### `sex`
This is either "m" or "f" (lower case)

#### `monthofbirth`
Integer values from 0 to 11, corresponding to JAN to DEC

#### `dayofbirth`
Integer values from 1 to 31
(but only those valid for that particular
month and year)

#### `yearofbirth`
Four digit year from 1904 to 2022

> **Note**: A Python `date` object can be constructed from a string
> in the format "yyyy-mm-dd" (two-digit month and day values!)
> using the `date.fromisoformat()` method.  You need to import this
> with `from datetime import date`

### Send a POST request to the URL
Use the Python `requests` module to send
the request and receive the response.

The URL for the cgi program at the Social Security Administration that
actually does the calculation is
[https://www.ssa.gov/cgi-bin/longevity.cgi](https://www.ssa.gov/cgi-bin/longevity.cgi)

### Handle the response HTML
Parse the response HTML to get the desired output.
The section of interest is this:
- Inside `<table ... summary="life expectancy table"` after the first `<tr>...</tr>`
...
```html
<tr><td style="text-align:left">68 and 6 months<sup>a</sup></td>
<td>16.5</td>
<td>85.0</td></tr>
...
Estimate as of Tuesday June 7, 2022 20:53:51 EDT.
```
You can use a [**finite state machine**](https://en.wikipedia.org/wiki/Finite-state_machine)
to parse this.
Could also use the Python [*Beautiful Soup*](https://www.crummy.com/software/BeautifulSoup/)
package


#### Current age
Current age, in decimal years.

#### Expected number of additional years
Decimal years, e.g., 13.5

#### Estimated total years
The projected age at death, also in decimal years.

