package longevity

import (
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strings"
	"time"
)

const (
	SSA_URL = "https://www.ssa.gov/cgi-bin/longevity.cgi"
	TIMEOUT = 15
)

// An HTTP client that times out after 15 seconds
var client = &http.Client{
	Timeout: TIMEOUT * time.Second,
}

// DoRequest accepts the two required parameters (sex and date of birth)
// and issues a POST request to the SSA website.  It then parses the
// HTML returned and creates a Response object with what it parses.
func DoRequest(sex string, dob time.Time) (string, error) {

	// Extract the month, day, and year as strings in the format the SSA website is expecting
	monthofbirth := fmt.Sprintf("%d", dob.Month()-1)
	dayofbirth := fmt.Sprintf("%0d", dob.Day())
	yearofbirth := fmt.Sprintf("%4d", dob.Year())

	// Format the post data
	values := url.Values{
		"sex":          {sex},
		"monthofbirth": {monthofbirth},
		"dayofbirth":   {dayofbirth},
		"yearofbirth":  {yearofbirth},
	}

	// Create the body parameter that client.Do requires
	body := strings.NewReader(values.Encode())

	// Create a POST request that the http client can use
	req, err := http.NewRequest(
		http.MethodPost,
		SSA_URL,
		body,
	)
	if err != nil {
		return "", err
	}

	// Pretend to be a browser
	req.Header.Set("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")
	req.Header.Set("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
	req.Header.Set("Accept-Language", "en-US,en;q=0.9")

	// Issue the request
	resp, err := client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	// Read the HTML returned
	htmlBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	return string(htmlBytes), nil

}
