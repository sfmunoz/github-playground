package github

import (
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
	return nil
}

func Run() error {
	g, err := newGH()
	if err != nil {
		return err
	}
	return g.run()
}
