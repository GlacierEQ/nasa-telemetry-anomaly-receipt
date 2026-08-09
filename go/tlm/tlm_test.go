package tlm

import "testing"

func TestHard(t *testing.T) {
	m := New([]Limit{{"temp", 50, 80}})
	r := m.Observe("temp", 90)
	if r.Severity != Hard {
		t.Fatal(r.Severity)
	}
}
