# GTS DigiTeam User Guide Portal

Find published guides at <https://equinor.github.io/gts-digiteam-userguides>.

On screens wider than 720 px, use the labeled sidebar button to switch between full navigation and a compact rail with Home and application initials. All guides remain accessible; hover over or focus a compact link to see its full name. At 720 px or narrower, navigation remains at the top.

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

The compact sidebar displays up to the first three characters of `initials`; shorter values are kept as given.

Choose a stable, lowercase application ID without spaces, such as `electroauthorizationsystem`. It is the application’s directory name in the portal, not its displayed title. Avoid changing it after publication because it determines the guide URL.

### Allow the workflow to publish

The workflow uses its normal `GITHUB_TOKEN` to check out the application repository, but needs a separate fine-grained personal access token (PAT) to push to `equinor/gts-digiteam-userguides`. The built-in token is scoped to the application repository; a PAT-authenticated push can also trigger the portal's deployment workflow.

Before creating the token:

- Use a GitHub account with a verified email address, membership in the `equinor` organization, and existing write access to `equinor/gts-digiteam-userguides`. A token cannot grant its owner more access than the account already has.
- Make sure you can create an Actions repository secret in the **application repository**. Ask its maintainers for help if you cannot access its settings.
- The token owner must be allowed to push to the portal's `main` branch under its branch protection rules or rulesets. If direct pushes are blocked, contact the portal maintainers; a PAT does not bypass those rules.

#### Create a fine-grained token

1. On GitHub, open your profile menu and select **Settings → Developer settings → Personal access tokens → Fine-grained tokens**. You can also open [fine-grained token settings](https://github.com/settings/personal-access-tokens) directly.
2. Select **Generate new token**. Give it a descriptive **Token name**, such as `userguide-publisher`, and choose an **Expiration** that complies with your organization's policy. Record a reminder to rotate it before it expires.
3. Under **Resource owner**, select `equinor`. If an approval justification is requested, describe that the token publishes an application guide. Complete any organization SSO prompt during creation.
4. Under **Repository access**, choose **Only select repositories**, then select `gts-digiteam-userguides`. The PAT does not need access to the application repository.
5. Under **Permissions → Repository permissions**, set **Contents** to **Read and write**. GitHub also includes read-only **Metadata** access; leave other permissions unselected. Contents write access applies to the whole selected repository, not just one application's directory.
6. Select **Generate token** and copy the token value immediately; GitHub shows it only once. If organization approval is required, ask an organization owner to approve the request. While approval is pending, the token can only read public resources, so a successful checkout does not prove that it can push.

If `equinor` or the portal repository is unavailable in the selection lists, check your membership and repository access with an organization administrator; organization policy may also restrict fine-grained tokens. See GitHub's [fine-grained token instructions](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token) for more details.

#### Store the token as an Actions secret

The secret name must match the workflow's `secrets.<name>` reference exactly. The example below uses `USERGUIDES_REPO_TOKEN`. The existing Electrical Authorization System workflow uses `GTS_DIGITEAM_USERGUIDES`, so use that name for it instead.

1. Open the **application repository**, not the user guide portal repository, on GitHub.
2. Go to **Settings → Secrets and variables → Actions**, select the **Secrets** tab, and choose **New repository secret**.
3. Enter the matching secret **Name**, paste the token into **Secret**, and select **Add secret**.

Treat the token like a password. Never put it in source code, workflow YAML, logs, screenshots, issues, or pull requests. The token belongs to its creator and stops working if it expires, is revoked, or the account loses access. Before expiration, create and approve a replacement, update the same application repository secret, verify publishing, and revoke the old token. Revoke an exposed token immediately.

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

### Verify publishing

1. Use a reviewed, non-sensitive guide change that is not already in the portal. Push it to `main` to trigger the workflow automatically, or run **Actions → Publish user guide → Run workflow** in the application repository for the branch containing that change. The workflow file must exist on the application's default branch for the manual option to appear.
2. Open the application repository's workflow run and confirm that the portal checkout and commit-and-push steps succeed.
3. In `equinor/gts-digiteam-userguides`, confirm that a new commit on `main` contains the expected changes under `apps/<application-id>/`.
4. In that repository's **Actions** tab, confirm that **Build and deploy user guides** succeeds, including the GitHub Pages deployment. Open the [portal](https://equinor.github.io/gts-digiteam-userguides) and check the updated guide.

If the run reports `No user guide changes to publish`, it did not push a commit or trigger a new portal deployment. A successful no-change run does not verify write permission; test again when there is a genuine, reviewed change. Subsequent changes to `docs/guides/**` on `main` publish automatically.

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

- **Portal repository or `equinor` is unavailable:** verify organization membership, the token's resource owner and selected repository, and the account's existing access. Ask an organization administrator about fine-grained token policies and approval.
- **Checkout succeeds but push is denied:** check that approval is complete, the token is not expired or revoked, it has **Contents: Read and write**, and its owner can write to the repository. Ask the portal maintainers about branch protection or rulesets if access is otherwise correct.
- **Secret not found:** check that the secret is in the application repository and its name exactly matches the workflow's `secrets.<name>` reference. The example uses `USERGUIDES_REPO_TOKEN`; an existing workflow may use a different name.
- **No portal deployment starts:** check that a commit was actually pushed to the portal's `main` branch with changes under `apps/**`, using the PAT rather than the application repository's `GITHUB_TOKEN`. A no-change run does not push or trigger a deployment.
- **Guide does not appear:** verify that at least one `apps/<application-id>/nb/index.md` or `en/index.md` reached the portal repository and that its front matter has `status: Published`.
