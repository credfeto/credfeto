# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
Please ADD ALL Changes to the UNRELASED SECTION and not a specific release
-->

## [Unreleased]
### Security
- Pinned GitHub Actions used in build.yml (actions/checkout, actions/setup-python, actions/cache) to immutable commit SHAs instead of mutable version tags, preventing a repointed or compromised tag from silently running different code
### Added
### Fixed
- Fixed YAML linting errors in build.yml: added document start marker, corrected indentation, removed extra whitespace, quoted python-version, reordered step fields, added shell: bash to all run steps, and updated action versions to specific release tags
### Changed
### Deprecated
### Removed
### Deployment Changes
<!--
Releases that have at least been deployed to staging, BUT NOT necessarily released to live.  Changes should be moved from [Unreleased] into here as they are merged into the appropriate release branch
-->
## [0.0.0] - Project created