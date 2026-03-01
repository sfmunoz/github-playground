# github-playground

Playground to test/validate some GitHub behaviours (e.g. actions)

## Tools

- **[https://goreleaser.com/](https://goreleaser.com/) + [https://github.com/goreleaser/goreleaser](https://github.com/goreleaser/goreleaser)**: release engineering, simplified. **Go**
- [https://docs.github.com/en/rest/releases/releases](https://docs.github.com/en/rest/releases/releases): REST API endpoints for releases. Use the REST API to create, modify, and delete releases.
- [https://dagger.io/](https://dagger.io/): A better way to ship. Build, test and deploy any codebase, repeatably and at scale. Runs locally, in your CI server, or directly in the cloud. **Go**
- [https://github.com/caarlos0/svu](https://github.com/caarlos0/svu): semantic version utility (svu) is a small helper for release scripts and workflows. It provides utility commands and functions to increase specific portions of the version. It can also figure the next version out automatically by looking through the git history. **Go**
- [https://github.com/semantic-release/semantic-release](https://github.com/semantic-release/semantic-release): fully automated version management and package publishing. **JavaScript**
- [https://github.com/release-it/release-it](https://github.com/release-it/release-it): automate versioning and package publishing. **JavaScript**
- [https://github.com/googleapis/release-please](https://github.com/googleapis/release-please):  generate release PRs based on the [conventionalcommits.org](https://www.conventionalcommits.org/) spec

## GoReleaser

### Quick start

Ref: https://goreleaser.com/quick-start/

- **(1)** `go mod init github.com/sfmunoz/github-playground`
- **(2)** create simple **main.go**
- **(3)** `goreleaser init`
- **(4)** `goreleaser check`
- **(5)** `goreleaser release --snapshot --clean`

### Devel

Release local execution (no tags):
```
./goreleaser-local.sh --verbose release --clean --snapshot
```
Build local execution (no tags):
```
./goreleaser-local.sh --verbose build --clean --snapshot
```
