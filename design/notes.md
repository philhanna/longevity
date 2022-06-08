## SSI Longevity Calculator design notes

### Form URL
https://www.ssa.gov/cgi-bin/longevity.cgi

#### Fields:
- name: sex, values: "m", "f"
- name: monthofbirth, values: 0-11
- name: dayofbirth, values: 01-31
- name: yearofbirth, values: 1904-2022

### Demo with `curl`
```
curl -d "sex=m&monthofbirth=11&dayofbirth=04&yearofbirth=1953" -X POST https://www.ssa.gov/cgi-bin/longevity.cgi
```

### Parsing returned HTML:

Inside `<table ... summary="life expectancy table"` after the first `<tr>...</tr>`
...
```html
<tr><td style="text-align:left">68 and 6 months<sup>a</sup></td>
<td>16.5</td>
<td>85.0</td></tr>
...
Estimate as of Tuesday June 7, 2022 20:53:51 EDT.
```

### Documentation for the Python requests module
https://requests.readthedocs.io/en/latest/user/quickstart/

### Earlier test
```python
import requests

response = requests.post('https://www.ssa.gov/cgi-bin/longevity.cgi', data={
    'sex':'m',
    'monthofbirth':12,
    'dayofbirth':4,
    'yearofbirth':1953
})
text = response.text
print(text)
```

## Tasks

1. install requests module (DONE)
2. 

