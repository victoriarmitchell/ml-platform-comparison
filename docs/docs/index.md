# ml_platform_comparison documentation!

## Description

Evaluate the UX of different ML platforms by building the same models across them. The study will focus on ease of use, feature comprehensiveness, and developer experience.

## Commands

The Makefile contains the central entry points for common tasks related to this project.

### Syncing data to cloud storage

* `make sync_data_up` will use `gsutil rsync` to recursively sync files in `data/` up to `gs://ml-platform-comparison-gcs/data/`.
* `make sync_data_down` will use `gsutil rsync` to recursively sync files in `gs://ml-platform-comparison-gcs/data/` to `data/`.


