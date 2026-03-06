# github-playground

Playground to test/validate some GitHub behaviours (e.g. actions)

> [!IMPORTANT]
> [Releases](https://github.com/sfmunoz/github-playground/releases) of this project contain useful information about how releases work... so they can be used as a reference

## gh release

Git log:
```
git log $(git describe --tags --abbrev=0)..HEAD --pretty=format:"%h %s"
```
gh release:
```
$ gh release create -h
(...)
  # Use automatically generated via GitHub Release Notes API release notes
  $ gh release create v1.2.3 --generate-notes
(...)
```

## Tools

- **[https://goreleaser.com/](https://goreleaser.com/) + [https://github.com/goreleaser/goreleaser](https://github.com/goreleaser/goreleaser)**: release engineering, simplified. **Go**
- [https://docs.github.com/en/rest/releases/releases](https://docs.github.com/en/rest/releases/releases): REST API endpoints for releases. Use the REST API to create, modify, and delete releases. **cURL/JavaScript/GitHub CLI**
- [https://dagger.io/](https://dagger.io/): A better way to ship. Build, test and deploy any codebase, repeatably and at scale. Runs locally, in your CI server, or directly in the cloud. **Go**
- [https://github.com/caarlos0/svu](https://github.com/caarlos0/svu): semantic version utility (svu) is a small helper for release scripts and workflows. It provides utility commands and functions to increase specific portions of the version. It can also figure the next version out automatically by looking through the git history. **Go**
- [https://github.com/semantic-release/semantic-release](https://github.com/semantic-release/semantic-release): fully automated version management and package publishing. **JavaScript**
- [https://github.com/release-it/release-it](https://github.com/release-it/release-it): automate versioning and package publishing. **JavaScript**
- [https://github.com/googleapis/release-please](https://github.com/googleapis/release-please): generate release PRs based on the [conventionalcommits.org](https://www.conventionalcommits.org/) spec. **TypeScript/JavaScript**

**gh release upload** example from [https://github.com/googleapis/release-please-action](https://github.com/googleapis/release-please-action):

```yaml
on:
  push:
    branches:
      - main
name: release-please
jobs:
  release-please:
    runs-on: ubuntu-latest
    steps:
      - uses: googleapis/release-please-action@v4
        id: release
        with:
          release-type: node
      - name: Upload Release Artifact
        if: ${{ steps.release.outputs.release_created }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: gh release upload ${{ steps.release.outputs.tag_name }} ./artifact/some-build-artifact.zip
```
