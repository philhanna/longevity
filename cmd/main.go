package main

import (
	"flag"
	"fmt"
	"os"
	"time"
	"github.com/philhanna/longevity"
)

const (
	usage = `usage: Gets life expectancy from the Social Security Administration's website.

positional arguments:
  sex        "m" or "f"
  dob        Date of birth in YYYY-MM-DD format
`
)

var (
	sex string
	dob time.Time
)

func main() {

	// Override flag.Usage so that it prints this program's usage
	flag.Usage = func() {
		fmt.Fprint(os.Stderr, usage)
		flag.PrintDefaults()
	}

	// Parse the flags
	flag.Parse()
	switch flag.NArg() {
	case 0:
		fmt.Fprint(os.Stderr, "Missing sex and date of birth\n")
		return
	case 1:
		fmt.Fprint(os.Stderr, "Missing date of birth\n")
		return
	}

	// Verify that the arguments are valid
	sex = flag.Arg(0)
	if sex != "m" && sex != "f" {
		fmt.Fprintf(os.Stderr, "Sex must be %q or %q\n", "m", "f")
		return
	}

	// Verify that date of birth is valid
	dobString := flag.Arg(1)
	dob, err := time.Parse(longevity.ISO_FORMAT, dobString)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Date of birth must be in YYYY-MM-DD format, not %q\n", dobString)
		return
	}

	// Invoke the requester
	resp, err := longevity.Get(sex, dob)
	if err != nil {
		fmt.Fprintln(os.Stderr, err.Error())
		return
	}
	currentAge := resp.CurrentAge
	additionalYears := resp.AdditionalYears
	totalYears := resp.TotalYears
	deathDate := resp.DeathDate
	deathYear, deathMonth, deathDay := deathDate.Date()

	fmt.Printf("current age      = %.1f\n", currentAge)
	fmt.Printf("additional years = %.1f\n", additionalYears)
	fmt.Printf("total years      = %.1f\n", totalYears)
	fmt.Printf("expiration date  = %4d-%02d-%02d\n", deathYear, deathMonth, deathDay)

}
