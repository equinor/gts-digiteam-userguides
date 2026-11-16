# Looking for the userguides?

Go to https://equinor.github.io/gts-digiteam-userguides

---

# Publishing user guides to the GTS DigiTeam User Guide Portal

This guide describes how application developers publish documentation to the GTS DigiTeam User Guide Portal.

Application teams maintain their user guides together with their application source code. A GitHub Actions workflow publishes the documentation to the central User Guides repository, where it is converted from Markdown to HTML and published through GitHub Pages.

> [!IMPORTANT]
> The User Guide Portal is public. Everything published to the portal must be considered publicly accessible.

---

## How publishing works

The publishing flow is:

```text
Application repository
        │
        │ Markdown + images
        ▼
GitHub Actions
        │
        ▼
equinor/gts-digiteam-userguides
        │
        ├── Markdown → HTML
        ├── Generate portal
        └── Deploy
        │
        ▼
GitHub Pages
        │
        ▼
Public User Guide Portal
```

Application teams are responsible for:

- maintaining their user guide
- maintaining screenshots and other assets
- defining application metadata
- keeping the documentation up to date
- publishing the documentation from their application repository

The User Guide Portal is responsible for:

- common presentation and styling
- application navigation
- application cards
- language selection
- Markdown-to-HTML conversion
- GitHub Pages deployment

Application repositories should publish documentation content and assets only. Styling and portal functionality are maintained centrally.

---

# Preparing your application repository

## 1. Create the documentation structure

The recommended structure in the application repository is:

```text
docs/
├── userguide.md
└── images/
    └── userguide/
        ├── overview.png
        ├── create-item.png
        ├── edit-item.png
        └── delete-item.png
```

Existing applications may use different names.

For example:

```text
docs/
├── hurtigguider.md
└── images/
    └── hurtigguider/
        ├── opprett.png
        └── rediger.png
```

The publishing workflow maps the application's own structure to the structure expected by the User Guide Portal.

---

# Structuring the user guide

## 2. Add application metadata

Every user guide must start with a metadata block.

Example:

```yaml
---
title_nb: Elektroautorisasjonssystem
title_en: Electro Authorization System
description_nb: Hurtigguider og brukerdokumentasjon for Elektroautorisasjonssystem.
description_en: Quick guides and user documentation for Electro Authorization System.
languages: nb,en
status: Published
order: 10
initials: EA
---
```

The metadata must be the first content in the Markdown file.

Do not place a heading or other content before the opening:

```text
---
```

## Metadata fields

| Field | Required | Description |
|---|---|---|
| `title_nb` | Yes | Norwegian application name displayed in the portal |
| `title_en` | Yes | English application name displayed in the portal |
| `description_nb` | Yes | Norwegian description displayed on the application card |
| `description_en` | Yes | English description displayed on the application card |
| `languages` | Yes | Available languages, for example `nb,en` |
| `status` | Yes | Use `Published` to make the guide visible in the portal |
| `order` | No | Controls ordering. Lower values appear first |
| `initials` | No | Short identifier displayed on the application card |

For example:

```yaml
languages: nb,en
```

indicates that the application documentation is available in Norwegian and English.

---

## 3. Choose an application ID

Each application needs a stable technical application ID.

For example:

```text
electroauthorizationsystem
```

The application ID becomes the directory name in the User Guides repository:

```text
apps/electroauthorizationsystem/
```

The application ID should:

- use lowercase characters
- contain no spaces
- be URL-friendly
- remain stable after publication
- not depend on the Norwegian or English application name

Example:

```text
Application ID:
electroauthorizationsystem

Norwegian display name:
Elektroautorisasjonssystem

English display name:
Electro Authorization System
```

The application ID and display names are deliberately separate.

The Norwegian or English application name can therefore change without changing the application's published location.

Avoid changing the application ID after publication because existing links may stop working.

---

# Writing the user guide

## 4. Use normal Markdown

After the metadata block, write the documentation using standard Markdown.

Example:

```markdown
# Hurtigguider

Denne siden inneholder hurtigguider for applikasjonen.

## Opprette et nytt element

1. Åpne applikasjonen.
2. Velg Nytt element.
3. Fyll ut de obligatoriske feltene.
4. Velg Lagre.

## Redigere et element

1. Finn elementet.
2. Velg Rediger.
3. Gjør nødvendige endringer.
4. Velg Lagre.
```

You can use normal Markdown features such as:

- headings
- numbered lists
- bullet lists
- links
- images
- tables
- code blocks
- emphasis

The portal converts the Markdown to HTML automatically.

---

## 5. Use a logical heading hierarchy

Use headings to structure the guide.

Recommended:

```markdown
# Hurtigguider

## Opprette autorisasjon

### Obligatorisk informasjon

### Godkjenne autorisasjonen

## Endre autorisasjon

## Avslutte autorisasjon
```

Avoid unnecessarily skipping heading levels.

For example, avoid going directly from:

```markdown
# Heading
```

to:

```markdown
### Heading
```

---

## 6. Write procedures as numbered steps

For procedures, numbered lists are usually easiest to follow.

Example:

```markdown
## Opprette en autorisasjon

1. Åpne applikasjonen.
2. Velg Ny.
3. Fyll ut nødvendig informasjon.
4. Kontroller opplysningene.
5. Velg Lagre.
```

Keep each step focused on one user action where possible.

---

# Images and screenshots

## 7. Store images with the documentation

Recommended structure:

```text
docs/
├── userguide.md
└── images/
    └── userguide/
        ├── home.png
        ├── create.png
        └── edit.png
```

Reference the image using a relative path:

```markdown
images/userguide/home.png
```

Do not use local filesystem paths such as:

```text
C:\Users\developer\Pictures\home.png
```

Do not reference images using URLs that require authentication.

Relative paths allow the publishing workflow to move the documentation without breaking its image references.

---

## 8. Add meaningful alternative text

Images should have useful alternative text.

Recommended:

```markdown
images/userguide/create.png
```

Avoid generic descriptions:

```markdown
images/userguide/create.png
```

Alternative text should briefly describe the information that the screenshot contributes to the instruction.

---

## 9. Keep screenshots focused

Use screenshots when they help explain:

- where an action is located
- navigation
- a complex form
- an unfamiliar interface
- an important state or result

Avoid screenshots when a short text instruction communicates the same thing clearly.

Crop screenshots where appropriate so the relevant part of the interface is easy to identify.

---

# Published structure

## 10. Structure expected by the portal

The publishing workflow must write documentation under:

```text
apps/<application-id>/
```

For example:

```text
apps/
└── electroauthorizationsystem/
    ├── index.md
    └── images/
        └── hurtigguider/
            ├── opprett.png
            ├── rediger.png
            └── slett.png
```

The main Markdown file must be published as:

```text
index.md
```

The source file in the application repository does not need to be named `index.md`.

For example:

```text
Application repository

docs/hurtigguider.md

        ↓

User Guides repository

apps/electroauthorizationsystem/index.md
```

The build process discovers published applications from:

```text
apps/*/index.md
```

---

# Publishing from the application repository

## 11. Create a GitHub Actions workflow

Create the following file in the application repository:

```text
.github/workflows/publish-userguide.yml
```

Example:

```yaml
name: Publish user guide

on:
  push:
    branches:
      - main
    paths:
      - "docs/userguide.md"
      - "docs/images/userguide/**"

  workflow_dispatch:

jobs:
  publish:
    name: Publish user guide
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
        run: |
          rm -rf userguides/apps/my-application

          mkdir -p \
            userguides/apps/my-application/images/userguide

          cp \
            docs/userguide.md \
            userguides/apps/my-application/index.md

          cp -r \
            docs/images/userguide/. \
            userguides/apps/my-application/images/userguide/

      - name: Commit and publish
        working-directory: userguides
        run: |
          git config user.name "github-actions[bot]"

          git config user.email \
            "41898282+github-actions[bot]@users.noreply.github.com"

          git add apps/my-application

          if git diff --cached --quiet; then
            echo "No user guide changes to publish."
            exit 0
          fi

          git commit \
            -m "Update my-application user guide"

          git push
```

Replace:

```text
my-application
```

with the application's technical application ID.

Also adjust:

```text
docs/userguide.md
docs/images/userguide/
```

if the application repository uses different paths.

---

# Authentication

## 12. Configure access to the User Guides repository

The publishing workflow needs permission to write to:

```text
equinor/gts-digiteam-userguides
```

The example workflow expects a GitHub Actions secret named:

```text
USERGUIDES_REPO_TOKEN
```

The credential should only have the permissions required to publish documentation to the User Guides repository.

Never place a token directly in:

```text
publish-userguide.yml
```

Never place credentials or secrets in the Markdown documentation.

Use GitHub Actions secrets or the authentication mechanism approved for the organization.

---

# What happens after publishing?

When the application workflow pushes content to the User Guides repository, the portal's deployment workflow runs automatically.

The process is:

```text
apps/<application-id>/index.md
        │
        ▼
      Pandoc
        │
        ▼
      HTML
        │
        ├── User guide
        └── Portal metadata
        │
        ▼
Portal generation
        │
        ▼
GitHub Pages
```

The portal automatically discovers applications under:

```text
apps/
```

and uses the metadata from each `index.md` to generate:

- application cards
- Norwegian application names
- English application names
- descriptions
- language information
- navigation
- ordering

Application teams do not need to modify the portal itself.

---

# Updating documentation

## 13. Publish documentation changes through the application repository

Update the Markdown or images in the application repository as part of the normal development process.

For example:

```text
docs/userguide.md
```

or:

```text
docs/images/userguide/**
```

After the changes reach `main`, the publication workflow runs automatically.

The application team does not need to deploy GitHub Pages directly.

---

## 14. Removing obsolete content

The recommended workflow replaces the application's complete published directory before copying the current documentation:

```bash
rm -rf userguides/apps/my-application
```

This is intentional.

If an obsolete screenshot is removed from the application repository, it will therefore also disappear from the public documentation during the next publication.

The workflow must only remove its own application directory.

Correct:

```bash
rm -rf userguides/apps/electroauthorizationsystem
```

Do not use:

```bash
rm -rf userguides/apps
```

The latter would remove documentation belonging to every application.

---

# Example: Electro Authorization System

Source repository:

```text
equinor/electroauthorizationsystem
```

Source documentation:

```text
docs/
├── hurtigguider.md
└── images/
    └── hurtigguider/
```

Application ID:

```text
electroauthorizationsystem
```

Metadata:

```yaml
---
title_nb: Elektroautorisasjonssystem
title_en: Electro Authorization System
description_nb: Hurtigguider og brukerdokumentasjon for Elektroautorisasjonssystem.
description_en: Quick guides and user documentation for Electro Authorization System.
languages: nb,en
status: Published
order: 10
initials: EA
---
```

Publishing mapping:

```text
docs/hurtigguider.md
        ↓
apps/electroauthorizationsystem/index.md
```

Images:

```text
docs/images/hurtigguider/
        ↓
apps/electroauthorizationsystem/images/hurtigguider/
```

This application can be used as a reference implementation when onboarding another application.

---

# Before publishing

Verify the following:

- [ ] `title_nb` contains the correct Norwegian application name.
- [ ] `title_en` contains the correct English application name.
- [ ] `description_nb` contains the correct Norwegian description.
- [ ] `description_en` contains the correct English description.
- [ ] `languages` reflects the documentation actually available.
- [ ] `status` is set to `Published`.
- [ ] The application ID is correct and stable.
- [ ] Markdown headings have a logical hierarchy.
- [ ] Images use relative paths.
- [ ] All referenced images exist.
- [ ] Images have meaningful alternative text.
- [ ] Links work.
- [ ] Norwegian characters such as `æ`, `ø` and `å` are displayed correctly.
- [ ] No secrets or credentials are present.
- [ ] Screenshots have been reviewed for sensitive information.

---

# Security and public content

> [!CAUTION]
> The GTS DigiTeam User Guide Portal is publicly accessible.

Everything published through this mechanism must be suitable for public distribution.

Do not publish:

- passwords
- Personal Access Tokens
- API keys
- client secrets
- connection strings
- authentication cookies
- credentials
- confidential information
- personal information
- production data
- sensitive source code
- sensitive system architecture
- information that exposes security controls

Pay particular attention to screenshots.

Before publishing a screenshot, check for:

- names
- email addresses
- user IDs
- environment names
- internal URLs
- tenant information
- record IDs
- production data
- browser tabs
- notifications
- tokens or credentials

If there is any doubt about whether information is suitable for public distribution, do not publish it until it has been reviewed.

---

# Responsibilities

## Application team

The application team owns:

- user guide content
- Norwegian and English application metadata
- screenshots and images
- keeping documentation aligned with application functionality
- the GitHub Actions publishing workflow
- reviewing content before public publication

## User Guide Portal

`equinor/gts-digiteam-userguides` owns:

- portal layout
- common styling
- navigation
- application cards
- language selection
- Markdown-to-HTML conversion
- GitHub Pages deployment

Application repositories should not contain copies of the portal layout, CSS or HTML.

Publish documentation content and assets only. The portal controls how the documentation is presented.
