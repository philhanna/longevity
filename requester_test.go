package longevity

import (
	"github.com/stretchr/testify/assert"
	"testing"
	"time"
)

func TestRequesterWithKeithRichards(t *testing.T) {
	sex := "m"
	dob, _ := time.Parse(ISO_FORMAT, "1943-12-18")
	html, err := DoRequest(sex, dob)
	if err != nil {
		t.Error(err)
	}
	resp, err := ParseResponse(html)
	if err != nil {
		t.Error(err)
	}
	assert.GreaterOrEqual(t, resp.CurrentAge, 80.0)
}
