package github

import (
	"fmt"
	"os/exec"
	"strings"

	"github.com/sfmunoz/github-playground/internal/cmdutil"
	"github.com/sfmunoz/logit"
)

var log = logit.Logit().WithLevel(logit.LevelInfo)

type GH struct {
}

func newGH() (*GH, error) {
	return &GH{}, nil
}

func (g *GH) run() error {
	log.Info("GH.run()")
	m, err := NewMetadata()
	if err != nil {
		return err
	}
	log.Info("metadata loaded", "m", m)
	cmd := exec.Command("gh", "release", "view", m.Tag)
	bo, be, err := cmdutil.RunSimple(cmd)
	if err != nil {
		return fmt.Errorf("'gh release view %s' failed': %s (stdout=%s, stderr=%s)", m.Tag, err, bo.String(), be.String())
	}
	lines := strings.SplitSeq(strings.TrimSpace(bo.String()), "\n")
	for line := range lines {
		log.Info("gh-release-view>", "line", line)
	}
	return nil
}

func Run() error {
	g, err := newGH()
	if err != nil {
		return err
	}
	return g.run()
}
