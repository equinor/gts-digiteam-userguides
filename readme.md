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

Before creating the publishing workflow, the application repository must be given a credential that allows GitHub Actions to write documentation to:

```text
equinor/gts-digiteam-userguides
```

The setup consists of two parts:

1. Create a token with access to the User Guides repository.
2. Store the token as a GitHub Actions secret in the application repository.
3. Create the publishing workflow that uses the secret.

---

## 1. Create a token for the User Guides repository

Create a fine-grained Personal Access Token (PAT) in GitHub.

Go to:

```text
GitHub
→ Settings
→ Developer settings
→ Personal access tokens
→ Fine-grained tokens
→ Generate new token
```

Configure the token so that it only has access to the User Guides repository.

### Resource owner

Select:

```text
equinor
```

as the resource owner.

This is important. If your personal account is selected as the resource owner, the token will not be able to select repositories owned by the Equinor organization.

### Repository access

Select:

```text
Only selected repositories
```

and select:

```text
equinor/gts-digiteam-userguides
```

The token should not be given access to additional repositories unless required for another purpose.

Fine-grained PATs allow repository access and permissions to be restricted to the resources required by the integration. 【1-507a77】【2-7754f8】

### Repository permissions

Under Repository permissions, configure:

```text
Contents: Read and write
```

The publishing workflow needs write access because it creates or updates files and pushes a commit to the User Guides repository.

Avoid granting unnecessary permissions.

### Organization approval

The Equinor GitHub organization may require approval of fine-grained Personal Access Tokens.

If approval is required, the token cannot access organization resources until an organization owner has approved the request. GitHub documents this approval flow for organizations that require approval of fine-grained PATs. 【3-2afd9c】

Do not continue with publication until the token has the required access.

---

## 2. Add the token to the application repository

Copy the token when GitHub displays it.

Do not add the token to source code, Markdown or the workflow YAML.

Instead, open the application repository and go to:

```text
Settings
→ Secrets and variables
→ Actions
→ New repository secret
```

Create a secret named:

```text
USERGUIDES_REPO_TOKEN
```

Paste the token as the secret value.

The application repository should now contain the Actions secret:

```text
USERGUIDES_REPO_TOKEN
```

The workflow will reference the secret as:

```yaml
${{ secrets.USERGUIDES_REPO_TOKEN }}
```

> [!IMPORTANT]
> Never commit the actual token to Git.

Correct:

```yaml
token: ${{ secrets.USERGUIDES_REPO_TOKEN }}
```

Incorrect:

```yaml
token: github_pat_xxxxxxxxxxxxxxxxx
```

---

## 3. Prepare the documentation

The application team may keep the documentation structure that makes sense for the application.

A recommended structure is:

```text
docs/
├── userguide.md
└── images/
    └── userguide/
        ├── overview.png
        ├── create.png
        └── edit.png
```

An existing application might instead use:

```text
docs/
├── hurtigguider.md
└── images/
    └── hurtigguider/
        ├── opprett.png
        └── rediger.png
```

Both are valid.

The publishing workflow is responsible for mapping the application's structure to the standard structure used by the User Guide Portal.

---

## 4. Add portal metadata to the Markdown file

The Markdown file must start with the portal metadata.

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

The portal uses these values to generate navigation and application cards.

The application ID is separate from the translated application names.

For example:

```text
Application ID:
electroauthorizationsystem

Norwegian name:
Elektroautorisasjonssystem

English name:
Electro Authorization System
```

This allows the displayed names to change without changing the application's URL.

---

## 5. Required published structure

Regardless of the structure in the application repository, the workflow must publish the documentation as:

```text
apps/
└── <application-id>/
    ├── index.md
    └── images/
        └── ...
```

For Electro Authorization System:

```text
apps/
└── electroauthorizationsystem/
    ├── index.md
    └── images/
        └── hurtigguider/
            ├── opprett.png
            └── rediger.png
```

The source Markdown file does not need to be named `index.md`.

For example:

```text
docs/hurtigguider.md
```

is published as:

```text
apps/electroauthorizationsystem/index.md
```

`index.md` is the contract between the application repository and the User Guide Portal.

---

## 6. Create the GitHub Actions workflow

Create:

```text
.github/workflows/publish-userguide.yml
```

in the application repository.

Example:

```yaml
name: Publish user guide

on:
  push:
    branches:
      - main
    paths:
      - "docs/hurtigguider.md"
      - "docs/images/hurtigguider/**"

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
          APP_ID="electroauthorizationsystem"
          SOURCE_MD="docs/hurtigguider.md"
          SOURCE_IMAGES="docs/images/hurtigguider"

          TARGET_DIR="userguides/apps/$APP_ID"

          rm -rf "$TARGET_DIR"

          mkdir -p \
            "$TARGET_DIR/images/hurtigguider"

          cp \
            "$SOURCE_MD" \
            "$TARGET_DIR/index.md"

          cp -r \
            "$SOURCE_IMAGES/." \
            "$TARGET_DIR/images/hurtigguider/"

      - name: Commit and publish
        working-directory: userguides
        run: |
          APP_ID="electroauthorizationsystem"

          git config \
            user.name \
            "github-actions[bot]"

          git config \
            user.email \
            "41898282+github-actions[bot]@users.noreply.github.com"

          git add \
            "apps/$APP_ID"

          if git diff --cached --quiet; then
            echo "No user guide changes to publish."
            exit 0
          fi

          git commit \
            -m "Update $APP_ID user guide"

          git push
```

The important authentication step is:

```yaml
token: ${{ secrets.USERGUIDES_REPO_TOKEN }}
```

This is the token stored in the application repository in step 2.

Without this credential, the workflow does not have permission to push documentation to the User Guides repository.

---

## 7. Adapt the workflow to your application

For another application, change:

```bash
APP_ID="electroauthorizationsystem"
SOURCE_MD="docs/hurtigguider.md"
SOURCE_IMAGES="docs/images/hurtigguider"
```

For example:

```bash
APP_ID="liftingequipment"
SOURCE_MD="docs/userguide.md"
SOURCE_IMAGES="docs/images/userguide"
```

Also update the workflow trigger:

```yaml
paths:
  - "docs/userguide.md"
  - "docs/images/userguide/**"
```

The destination contract remains:

```text
apps/<application-id>/index.md
```

---

## 8. Test access before relying on automatic publishing

The workflow contains:

```yaml
workflow_dispatch:
```

This allows it to be run manually.

After committing the workflow:

1. Open the application repository.
2. Select Actions.
3. Select Publish user guide.
4. Select Run workflow.
5. Run it against `main`.

The first important step to verify is:

```text
Checkout User Guides repository
```

If this succeeds, the workflow was able to authenticate against:

```text
equinor/gts-digiteam-userguides
```

Then verify that:

```text
Commit and publish
```

also succeeds.

A successful run should create or update:

```text
apps/<application-id>/
```

in the User Guides repository.

---

## Troubleshooting authentication

### Repository not found

If the workflow reports that:

```text
equinor/gts-digiteam-userguides
```

cannot be found, verify:

- the token uses `equinor` as its resource owner
- the token has access to `gts-digiteam-userguides`
- the token has not expired
- any required organization approval has been completed

Fine-grained PATs can be restricted to specific repositories, and organizations can require approval before such tokens can access organization resources. 【2-7754f8】【3-2afd9c】

### Write access not granted

If checkout succeeds but:

```text
git push
```

fails with a write-access error, verify that the token has:

```text
Repository permissions
→ Contents
→ Read and write
```

### Secret not found

Verify that the application repository contains a repository secret named exactly:

```text
USERGUIDES_REPO_TOKEN
```

and that the workflow references exactly:

```yaml
${{ secrets.USERGUIDES_REPO_TOKEN }}
```

Secret names are case-sensitive.

---

## Security

The token is a credential.

Do not:

- include it in Markdown
- print it in workflow logs
- commit it to the repository
- put it directly in workflow YAML
- share it in issues or pull requests

Store it only as a GitHub Actions secret.

The token should be limited to:

```text
equinor/gts-digiteam-userguides
```

with only the permissions required for publishing.

If the organization later provides a centrally managed GitHub App or equivalent publishing identity, that should be preferred over individually owned PATs for a long-lived team integration.

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
