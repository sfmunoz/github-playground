package github

import (
	_ "embed"
	"fmt"
	"os/exec"
	"strings"

	"github.com/sfmunoz/github-playground/internal/cmdutil"
	"github.com/sfmunoz/logit"
)

var log = logit.Logit().WithLevel(logit.LevelInfo)

//go:embed static/github.sh
var githubSh string

type GH struct {
	Metadata *Metadata
}

func newGH() (*GH, error) {
	metadata, err := NewMetadata()
	if err != nil {
		return nil, err
	}
	log.Info("metadata loaded", "metadata", metadata)
	return &GH{Metadata: metadata}, nil
}

func (g *GH) releaseView() error {
	cmd := exec.Command("gh", "release", "view", g.Metadata.Tag)
	bo, be, err := cmdutil.RunSimple(cmd)
	if err != nil {
		return fmt.Errorf("'gh release view %s' failed': %s (stdout=%s, stderr=%s)", g.Metadata.Tag, err, bo.String(), be.String())
	}
	lines := strings.SplitSeq(strings.TrimSpace(bo.String()), "\n")
	for line := range lines {
		log.Info("gh-release-view>", "line", line)
	}
	return nil
}

func (g *GH) githubSh() error {
	cmd := exec.Command("bash", "-c", githubSh)
	bo, be, err := cmdutil.RunSimple(cmd)
	if err != nil {
		return fmt.Errorf("github script execution failed: %s (stdout=%s, stderr=%s)", err, bo.String(), be.String())
	}
	lines := strings.SplitSeq(strings.TrimSpace(bo.String()), "\n")
	for line := range lines {
		log.Info("github-sh>", "line", line)
	}
	return nil
}

func (g *GH) run() error {
	log.Info("GH.run()")
	if err := g.releaseView(); err != nil {
		return err
	}
	if err := g.githubSh(); err != nil {
		return err
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
