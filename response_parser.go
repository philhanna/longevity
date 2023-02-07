package main

import (
	"errors"
	"fmt"
	"regexp"
	"strconv"
	"time"

	"github.com/anaskhan96/soup"
)

// Response is a structure that contains the results of parsing a response.
type Response struct {
	CurrentAge      float64
	AdditionalYears float64
	TotalYears      float64
	DeathDate       time.Time
}

// ParseResponse parses the response HTML to get the desired output.
// The section of interest is this:
//
// Inside <table ... summary="life expectancy table" after the first <tr>...</tr> ...
//
//	<tr><td style="text-align:left">68 and 6 months<sup>a</sup></td>
//	<td>16.5</td>
//	<td>85.0</td></tr>
func ParseResponse(html string) (Response, error) {

	// Parse the html string
	root := soup.HTMLParse(html)

	// Find the first <table>
	table := root.Find("table")

	// Get the list of table rows <tr> it contains, and skip the first
	trs := table.FindAll("tr")
	tr := trs[1]

	// Find all three table cells <td>
	tds := tr.FindAll("td")
	if len(tds) < 3 {
		errmsg := fmt.Sprintf("Not enough <td> tags. Only %d found", len(tds))
		return Response{}, errors.New(errmsg)
	}

	// Fill out the structure and return a pointer to it
	currentAge := ParseCurrentAge(tds[0].Text())
	additionalYears := ParseFloat(tds[1].Text())
	totalYears := ParseFloat(tds[2].Text())

	// Calculate the estimated date of death
	addHours := float64(additionalYears * 365.25 * 24)
	durString := fmt.Sprintf("%dh", int(addHours))
	dur, _ := time.ParseDuration(durString)
	deathDate := time.Now().Add(dur)

	r := Response{currentAge, additionalYears, totalYears, deathDate}
	return r, nil
}

// ParseCurrentAge finds an age value in a string.
// This can be a simple integer: "68" or a combination of years
// and month(s): ("68 and 3 months")
func ParseCurrentAge(currentAgeString string) float64 {
	age := float64(0)
	re := regexp.MustCompile(`(\d+)`)
	m := re.FindString(currentAgeString)
	if m != "" {
		age, _ = strconv.ParseFloat(m, 64)
	}
	re = regexp.MustCompile(` and (\d+) month`)
	groups := re.FindStringSubmatch(currentAgeString)
	if len(groups) != 0 {
		inner := groups[1]
		f, _ := strconv.ParseFloat(inner, 64)
		age += f / 12.0
	}
	return age
}

// ParseFloat converts a string to a float, ignoring any errors
func ParseFloat(s string) float64 {
	f, err := strconv.ParseFloat(s, 64)
	if err != nil {
		f = float64(-1)
	}
	return f
}
