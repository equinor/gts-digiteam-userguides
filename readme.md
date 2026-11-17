# GTS DigiTeam User Guide Portal

Find published guides at <https://equinor.github.io/gts-digiteam-userguides>.

# Publish a user guide

Application teams keep guide content and images in their application repository. A GitHub Actions workflow copies them to `equinor/gts-digiteam-userguides`. The portal repository then builds and deploys the public site.

> [!IMPORTANT]
> The portal is public. Do not publish confidential information, personal data, credentials, or screenshots containing sensitive information.

## 1. Set up the application repository

Keep the source files together in the application repository. For example:

```text
docs/
└── guides/
    ├── nb/
    │   └── hurtigguide.md
    ├── en/
    │   └── quickguide.md
    └── images/
        ├── overview.png
        └── create-item.png
.github/
└── workflows/
    └── publish-userguide.yml
```

Include only the language directories you maintain. In each guide, use normal Markdown, meaningful heading levels, and numbered steps for procedures. Reference images with descriptive alternative text and a relative path, such as:

```markdown
![The new item form](../images/create-item.png)
```

The path works both in the source structure and after publishing. Keep screenshots focused and use synthetic or anonymised data.

### Add portal metadata

Start each guide with a front matter block. Keep the same metadata in both language files; the portal reads it from `nb/index.md`, or from `en/index.md` when no Norwegian guide exists.

```yaml
---
title_nb: Elektroautorisasjonssystem
title_en: Electro Authorization System
description_nb: Hurtigguider og brukerdokumentasjon for Elektroautorisasjonssystem.
description_en: Quick guides and user documentation for Electro Authorization System.
status: Published
order: 10
initials: EA
---
```

`title_*` and `description_*` provide the translated application-card text. Set `status: Published` to show the application. `order` is optional (lower numbers appear first), as is `initials` (the portal can generate these).

Choose a stable, lowercase application ID without spaces, such as `electroauthorizationsystem`. It is the application’s directory name in the portal, not its displayed title. Avoid changing it after publication because it determines the guide URL.

### Allow the workflow to publish

The application repository needs a fine-grained GitHub Personal Access Token (PAT) that can write to the portal repository:

1. Create a fine-grained token with resource owner `equinor`.
2. Limit repository access to `gts-digiteam-userguides`.
3. Grant the repository permission **Contents: Read and write**. Obtain Equinor organization approval if required.
4. In the application repository, open **Settings → Secrets and variables → Actions** and create a repository secret named `USERGUIDES_REPO_TOKEN`.

Never put the token in source code, workflow YAML, or logs. Keep it in the Actions secret only.

### Add the publishing workflow

Create `.github/workflows/publish-userguide.yml`. Update `APP_ID` if needed. The example publishes either or both language guides and copies the shared images:

```yaml
name: Publish user guide

on:
  push:
    branches:
      - main
    paths:
      - "docs/guides/**"
      - ".github/workflows/publish-userguide.yml"
  workflow_dispatch:

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout application repository
        uses: actions/checkout@v6

      - name: Checkout User Guides repository
        uses: actions/checkout@v6
        with:
          repository: equinor/gts-digiteam-userguides
          token: ${{ secrets.USERGUIDES_REPO_TOKEN }}
          path: userguides

      - name: Prepare user guide
        shell: bash
        run: |
          APP_ID="electroauthorizationsystem"
          SOURCE_DIR="docs/guides"
          TARGET_DIR="userguides/apps/$APP_ID"
          found_guide=false

          for language in nb en; do
            if [ "$language" = nb ]; then
              source="$SOURCE_DIR/$language/hurtigguide.md"
            else
              source="$SOURCE_DIR/$language/quickguide.md"
            fi
            if [ -f "$source" ]; then
              mkdir -p "$TARGET_DIR/$language"
              cp "$source" "$TARGET_DIR/$language/index.md"
              found_guide=true
            fi
          done

          if [ "$found_guide" != true ]; then
            echo "::error::No nb/index.md or en/index.md guide was found."
            exit 1
          fi

          if [ -d "$SOURCE_DIR/images" ]; then
            mkdir -p "$TARGET_DIR/images"
            cp -R "$SOURCE_DIR/images/." "$TARGET_DIR/images/"
          fi

      - name: Commit and publish
        working-directory: userguides
        run: |
          APP_ID="electroauthorizationsystem"

          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add "apps/$APP_ID"

          if git diff --cached --quiet; then
            echo "No user guide changes to publish."
            exit 0
          fi

          git commit -m "Update $APP_ID user guide"
          git push
```

Run it once manually from the application repository’s **Actions** tab using **Publish user guide → Run workflow**. Confirm that both the checkout and publish steps succeed. Subsequent changes to `docs/guides/**` on `main` publish automatically.

## 2. How the portal receives and publishes guides

The application workflow writes this structure to the User Guides repository:

```text
apps/
└── <application-id>/
    ├── nb/
    │   └── index.md
    ├── en/
    │   └── index.md
    └── images/
        └── ...
```

The portal discovers an application when it finds `nb/index.md` or `en/index.md`. The language folders determine which languages are available; the stable application ID determines the application’s portal path. Image references remain relative to each guide.

When changes arrive in the User Guides repository, its own GitHub Actions workflow:

1. Reads application metadata and builds the portal’s application cards and navigation.
2. Converts each language’s `index.md` to an HTML guide and copies shared images and assets.
3. Deploys the generated site to GitHub Pages.

The application workflow only transfers guide files; deployment of the public portal is handled by the User Guides repository.

## Responsibilities

- **Application team:** owns guide content, translations, images, metadata, and the publishing workflow. Review all content and screenshots before publishing.
- **User Guide Portal:** owns the shared design, navigation, Markdown-to-HTML build, and GitHub Pages deployment. Application repositories should publish content and assets only, not portal styling or HTML.

## Troubleshooting

- **Portal repository not found:** verify the token’s resource owner is `equinor`, repository access includes `gts-digiteam-userguides`, and any required organization approval is complete.
- **Push is denied:** verify the token has **Contents: Read and write** access to the portal repository.
- **Secret not found:** check that the application repository has a secret named exactly `USERGUIDES_REPO_TOKEN` and the workflow references `${{ secrets.USERGUIDES_REPO_TOKEN }}`.
- **Guide does not appear:** verify that at least one `apps/<application-id>/nb/index.md` or `en/index.md` reached the portal repository and that its front matter has `status: Published`.
