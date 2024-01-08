package longevity

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

func TestGetDateFields(t *testing.T) {
	dob, _ := time.Parse(ISO_FORMAT, "2023-01-30")
	haveMonth, haveDay, haveYear := GetDateFields(dob)
	wantMonth, wantDay, wantYear := "0", "30", "2023"
	assert.Equal(t, wantMonth, haveMonth)
	assert.Equal(t, wantDay, haveDay)
	assert.Equal(t, wantYear, haveYear)
}

func TestFormatPostData(t *testing.T) {
	goodTime := func(s string) time.Time {
		dob, _ := time.Parse(ISO_FORMAT, s)
		return dob
	}
	tests := []struct {
		name string
		sex  string
		dob  time.Time
		want string
	}{
		{
			name: "today",
			sex:  "m",
			dob:  goodTime("2023-01-30"),
			want: "sex=m&monthofbirth=0&dayofbirth=30&yearofbirth=2023",
		},
		{
			name: "Keith Richards",
			sex:  "m",
			dob:  goodTime("1943-12-18"),
			want: "sex=m&monthofbirth=11&dayofbirth=18&yearofbirth=1943",
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			assert.Equal(t, tt.want, FormatPostData(tt.sex, tt.dob))
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
	assert.GreaterOrEqual(t, requester.CurrentAge, 80.0)
}
