# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.15]
### Added
- Slug field `label` added. Added ability to filter over `label` field.
- Division name prefixes. They also used in address formatter now.
- New dumping script. It creates updatable dump.
### Changed
- Changed the way geometry data stored. Separate geometry model is there still, but it's deprecated.
- Changed polygon field to be MultiPolygon instead on Polygon.

## [0.1.14]
### Fixed
- Fixed tree lookups.
### Added
- DAL admin extends the default one with fields and filters for division.

## [0.1.13]
### Fixed
- Fixed setup.

## [0.1.12]
### Added
- DAL contrib module.
- Small changes to a search mechanics.

## [0.1.11]
### Fixed
- Fixed address formatter usage with translations.

  If there is none - fallbacks to an original entity data.

  Make at least 1, at most 2 queries, no matter the amount of address definitions passed.

## [0.1.10]
### Fixed
- Translations mechanics added. No changes to an external API. Now it just works as expected.

## [0.1.9]
### Fixed
- Search fix. Added indexes to improve search performance. Some additional tests added.
### Changed
- Search API extended: now you can add a `min_rank`(minimal matching rank 0..1) parameter info a `search_query` to limit matches amount.

## [0.1.8]
### Added
- Search mechanics implemented. Old API was a little bit changed: language parameter is not required not. Example in README.

## [0.1.6]
### Fixed
- Tree structure is now optimal.

## [0.1.5]
### Changed
- Data structure changes.

## [0.1.2]
Initial version.
