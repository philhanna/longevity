package main

import (
	"os"
	"path/filepath"
	"testing"
)

func TestResponseParser(t *testing.T) {
	testdata := "testdata"
	testfile := filepath.Join(testdata, "keith_richards.html")
	contentBytes, err := os.ReadFile(testfile)
	if err != nil {
		t.Error(err)
	}
	html := string(contentBytes)
	resp, err := ParseResponse(html)
	if err != nil {
		t.Error(err)
	}

	var have, want float64

	have = resp.CurrentAge
	want = 78.75
	if have != want {
		t.Errorf("Current age: have=%0.2f, want=%0.2f", have, want)
	}

	have = resp.AdditionalYears
	want = 9.5
	if have != want {
		t.Errorf("Additional years: have=%0.2f, want=%0.2f", have, want)
	}

	have = resp.TotalYears
	want = 88.3
	if have != want {
		t.Errorf("Total years: have=%0.2f, want=%0.2f", have, want)
	}

}

func TestParseCurrentAge(t *testing.T) {
	type args struct {
		currentAgeString string
	}
	tests := []struct {
		name string
		args args
		want float64
	}{
		{"Integer years", args{"68"}, 68},
		{"and some months", args{"68 and 3 months"}, 68.25},
		{"and 1 month", args{"68 and 1 month"}, 68.083333333333},
		{"bogus", args{"bogus"}, 0},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			input := tt.args.currentAgeString
			want := tt.want
			have := ParseCurrentAge(input)
			if !AlmostEqual(have, want) {
				t.Errorf("ParseCurrentAge() = %v, want %v", have, tt.want)
			}
		})
	}
}

func TestParseFloat(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  float64
	}{
		{"simple", "29.95", float64(29.95)},
		{"integer", "13", float64(13)},
		{"empty", "", float64(-1)},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			input := tt.input
			have := ParseFloat(input)
			want := tt.want
			if !AlmostEqual(have, want) {
				t.Errorf("ParseFloat() = %v, want %v", have, want)
			}
		})
	}
}
