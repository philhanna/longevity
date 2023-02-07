package main

import (
	"testing"
	"time"
)

func TestGetDateFields(t *testing.T) {
	dob, _ := time.Parse(ISO_FORMAT, "2023-01-30")
	haveMonth, haveDay, haveYear := GetDateFields(dob)
	wantMonth, wantDay, wantYear := "0", "30", "2023"
	if haveMonth != wantMonth {
		t.Errorf("haveMonth=%q, wantMonth=%q", haveMonth, wantMonth)
	}
	if haveDay != wantDay {
		t.Errorf("wantDay=%q, wantDay=%q", haveDay, wantDay)
	}
	if haveYear != wantYear {
		t.Errorf("haveYear=%q, wantYear=%q", haveYear, wantYear)
	}
}

func TestFormatPostData(t *testing.T) {
	goodTime := func(s string) time.Time {
		dob, _ := time.Parse(ISO_FORMAT, s)
		return dob
	}
	type args struct {
		sex string
		dob time.Time
	}
	tests := []struct {
		name string
		args args
		want string
	}{
		{
			name: "today",
			args: args{
				sex: "m",
				dob: goodTime("2023-01-30"),
			},
			want: "sex=m&monthofbirth=0&dayofbirth=30&yearofbirth=2023",
		},
		{
			name: "Keith Richards",
			args: args{
				sex: "m",
				dob: goodTime("1943-12-18"),
			},
			want: "sex=m&monthofbirth=11&dayofbirth=18&yearofbirth=1943",
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := FormatPostData(tt.args.sex, tt.args.dob); got != tt.want {
				t.Errorf("FormatPostData() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestRequesterWithKeithRichards(t *testing.T) {
	sex := "m"
	dob, _ := time.Parse(ISO_FORMAT, "1943-12-18")
	requester, err := Get(sex, dob)
	if err != nil {
		t.Error(err)
	}
	want := 79 + 1.0/12.0
	have := requester.CurrentAge
	if !AlmostEqual(want, have) {
		t.Errorf("CurrentAge: want=%f, have=%f", want, have)
	}
}
