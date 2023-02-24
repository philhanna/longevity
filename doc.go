// A web scraper for the Social Security Administration's life expectancy calculation.
//
// Given a gender code ("m" or "f") and a date of birth in YYYY-MM-DD format,
// it will do a POST request to the Social Security Administrations website
// using the format defined by its [Life Expectancy Calculator], parse the response,
// and return the result.
package longevity
