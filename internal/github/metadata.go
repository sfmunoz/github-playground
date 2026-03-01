package github

import (
	"encoding/json"
	"os"
)

type Metadata struct {
	ProjectName string `json:"project_name"`
	Tag         string `json:"tag"`
	PreviousTag string `json:"previous_tag"`
	Version     string `json:"version"`
	Commit      string `json:"commit"`
	Date        string `json:"date"`
	Runtime     *struct {
		GoOs   string `json:"goos"`
		GoArch string `json:"goarch"`
	}
}

func NewMetadata() (*Metadata, error) {
	m := &Metadata{}
	buf, err := os.ReadFile("dist/metadata.json")
	if err != nil {
		return nil, err
	}
	if err := json.Unmarshal(buf, m); err != nil {
		return nil, err
	}
	return m, nil
}
