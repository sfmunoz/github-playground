# github-playground

Playground to test/validate some GitHub behaviours (e.g. actions)

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
