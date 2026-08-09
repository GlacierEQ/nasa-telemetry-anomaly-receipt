package tlm

type Severity string

const (
	Nominal Severity = "NOMINAL"
	Warn    Severity = "WARN"
	Hard    Severity = "HARD"
)

type Limit struct {
	Channel string
	Warn, Hard float64
}

type Receipt struct {
	Channel  string
	Value    float64
	Severity Severity
	Residual float64
}

type Monitor struct {
	limits map[string]Limit
}

func New(limits []Limit) *Monitor {
	m := map[string]Limit{}
	for _, l := range limits {
		m[l.Channel] = l
	}
	return &Monitor{limits: m}
}

func (m *Monitor) Observe(ch string, v float64) Receipt {
	lim, ok := m.limits[ch]
	if !ok {
		return Receipt{ch, v, Hard, 0}
	}
	if v >= lim.Hard {
		return Receipt{ch, v, Hard, v - lim.Hard}
	}
	if v >= lim.Warn {
		return Receipt{ch, v, Warn, v - lim.Warn}
	}
	return Receipt{ch, v, Nominal, 0}
}
