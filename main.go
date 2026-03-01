package main

import (
	"github.com/sfmunoz/github-playground/internal/github"
	"github.com/sfmunoz/logit"
)

var log = logit.Logit().WithLevel(logit.LevelInfo)

func main() {
	log.Info("github-playground")
	if err := github.Run(); err != nil {
		log.Fatal("github.Run() failed", "err", err)
	}
}
