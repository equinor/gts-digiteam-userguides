from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPS_DIR = ROOT / "apps"
OUTPUT_FILE = ROOT / "_site" / "index.html"


def read_frontmatter(markdown_file: Path) -> dict[str, str]:
    content = markdown_file.read_text(encoding="utf-8")

    match = re.match(
        r"^---\s*\n(.*?)\n---\s*(?:\n|$)",
        content,
        flags=re.DOTALL,
    )

    if not match:
        return {}

    metadata: dict[str, str] = {}

    for line in match.group(1).splitlines():
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("\"'")

    return metadata


def get_order(value: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 9999


def get_apps() -> list[dict[str, str]]:
    apps: list[dict[str, str]] = []

    if not APPS_DIR.exists():
        return apps

    for app_directory in APPS_DIR.iterdir():
        if not app_directory.is_dir():
            continue

        index_file = app_directory / "index.md"

        if not index_file.exists():
            continue

        metadata = read_frontmatter(index_file)

        if metadata.get("status", "Published").lower() != "published":
            continue

        app_id = app_directory.name

        apps.append(
            {
                "id": app_id,
                "title": metadata.get(
                    "title",
                    app_id.replace("-", " ").title(),
                ),
                "description": metadata.get(
                    "description",
                    "Brukerguide og dokumentasjon.",
                ),
                "language": metadata.get(
                    "language",
                    "Norsk og English",
                ),
                "order": str(
                    get_order(metadata.get("order", "9999"))
                ),
            }
        )

    return sorted(
        apps,
        key=lambda app: (
            int(app["order"]),
            app["title"].lower(),
        ),
    )


def render_cards(apps: list[dict[str, str]]) -> str:
    if not apps:
        return """
        <div class="empty-state">
          <h2>Ingen brukerguider er publisert ennå</h2>
          <p>
            Publiserte brukerguider vises automatisk her.
          </p>
        </div>
        """

    cards: list[str] = []

    for app in apps:
        title = html.escape(app["title"])
        description = html.escape(app["description"])
        language = html.escape(app["language"])
        url = f"apps/{html.escape(app['id'])}/"

        cards.append(
            f"""
            <article class="guide-card">
              <div class="guide-card__content">
                <div class="guide-card__meta">
                  <span class="guide-card__eyebrow">
                    Brukerguide
                  </span>

                  <span class="guide-card__language">
                    {language}
                  </span>
                </div>

                <h2 class="guide-card__title">
                  {title}
                </h2>

                <p class="guide-card__description">
                  {description}
                </p>
              </div>

              <a
                class="eds-button"
                href="{url}"
                aria-label="Åpne brukerguiden for {title}"
              >
                Åpne brukerguide
                <span aria-hidden="true">→</span>
              </a>
            </article>
            """
        )

    return "\n".join(cards)


def build_page(apps: list[dict[str, str]]) -> str:
    cards = render_cards(apps)
    guide_count = len(apps)

    return f"""<!doctype html>
<html lang="nb" data-color-scheme="light">
<head>
  <meta charset="utf-8">

  <meta
    name="viewport"
    content="width=device-width, initial-scale=1"
  >

  <meta
    name="description"
    content="Offentlige brukerguider for applikasjoner utviklet av GTS DigiTeam."
  >

  <title>GTS DigiTeam brukerguider</title>

  <link
    rel="stylesheet"
    href="styles/userguide.css"
  >
</head>

<body>
  <a class="skip-link" href="#main-content">
    Hopp til hovedinnhold
  </a>

  <header class="site-header">
    <div class="site-header__content">
      <a class="site-header__brand" href="./">
        <span class="site-header__brand-mark" aria-hidden="true"></span>

        <span>
          <strong>GTS DigiTeam</strong>
          <span class="site-header__subtitle">
            Brukerguider
          </span>
        </span>
      </a>
    </div>
  </header>

  <main id="main-content">
    <section class="hero" aria-labelledby="page-title">
      <div class="page-container hero__content">
        <p class="hero__eyebrow">
          Dokumentasjon
        </p>

        <h1 id="page-title">
          Brukerguider for våre applikasjoner
        </h1>

        <p class="hero__ingress">
          Finn hurtigguider og brukerdokumentasjon for applikasjoner
          utviklet og vedlikeholdt av GTS DigiTeam.
        </p>
      </div>
    </section>

    <section
      class="guide-section page-container"
      aria-labelledby="guide-heading"
    >
      <div class="section-heading">
        <div>
          <p class="section-heading__eyebrow">
            Applikasjoner
          </p>

          <h2 id="guide-heading">
            Tilgjengelige brukerguider
          </h2>
        </div>

        <p class="guide-count">
          {guide_count} publisert
        </p>
      </div>

      <div class="guide-grid">
        {cards}
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="page-container site-footer__content">
      <p>
        Dokumentasjonen vedlikeholdes av GTS DigiTeam.
      </p>

      <p>
        Innholdet oppdateres automatisk ved publisering.
      </p>
    </div>
  </footer>
</body>
</html>
"""


def main() -> None:
    apps = get_apps()

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_FILE.write_text(
        build_page(apps),
        encoding="utf-8",
    )

    print(
        f"Generated {OUTPUT_FILE} with {len(apps)} guide(s)."
    )


if __name__ == "__main__":
    main()