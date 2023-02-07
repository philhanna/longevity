package main

import (
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"
)

// Get issues a POST request to the website, parses the response, and returns the results.
//
// Parameters:
// - sex: either "m" or "f"
// - dob: date of birth
//
// Returns:
// - The response
func Get(sex string, dob time.Time) (Response, error) {

	// Create a string that will be sent to the server containing sex and date of birth
	postData := FormatPostData(sex, dob)

	// Post the request to the server
	html, err := PostRequest(postData)
	if err != nil {
		return Response{}, err
	}

	// Parse the response and return the whole structure
	resp, err := ParseResponse(html)
	if err != nil {
		return Response{}, err
	}

	return resp, nil
}

// GetDateFields extracts date fields and formats them in the way the
// cgi program expects them.
//
// Output fields:
//   - monthofbirth is the month field minus 1 (0-11)
//   - dayofbirth is the day field with leading zero if less than 10
//   - yearofbirth is a 4-digit year field
//     These fields are returned as tuple of 3 strings
func GetDateFields(dob time.Time) (monthOfBirth, dayOfBirth, yearOfBirth string) {
	monthOfBirth = fmt.Sprintf("%d", dob.Month()-1)
	dayOfBirth = fmt.Sprintf("%0d", dob.Day())
	yearOfBirth = fmt.Sprintf("%4d", dob.Year())
	return
}

// FormatPostData creates a dictionary of the data that will be used in the POST method
func FormatPostData(sex string, dob time.Time) string {
	mm, dd, yyyy := GetDateFields(dob)
	s := fmt.Sprintf("sex=%s&monthofbirth=%s&dayofbirth=%s&yearofbirth=%s", sex, mm, dd, yyyy)
	return s
}

// PostRequest posts the request and gets the response.
//
// Parameters postdata: a string containing the parameters, e.g., for Keith Richards:
//   - "sex" : "m",
//   - "monthofbirth": "11",   # Note: website expects actual month - 1
//   - "dayofbirth": "18",
//   - "yearofbirth": "1943",
//
// Returns: a string containing the returned HTML
//
// Separated from the mainline so that this function can be mocked
// and test data used instead of a live call to the URL.
func PostRequest(postData string) (string, error) {
	const SSA_URL = "https://www.ssa.gov/cgi-bin/longevity.cgi"
	const contentType = "application/x-www-form-urlencoded"

	// Send the request
	body := strings.NewReader(postData)
	resp, err := http.Post(SSA_URL, contentType, body)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	// Get the contents of the response, which will be an array of bytes
	content, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	// And then convert it to a string
	html := string(content)

	return html, nil
}
