from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import TypedDict


ROOT = Path(__file__).resolve().parents[1]
APPS_DIR = ROOT / "apps"
OUTPUT_FILE = ROOT / "_site" / "index.html"


class AppMetadata(TypedDict):
    app_id: str
    title_nb: str
    title_en: str
    description_nb: str
    description_en: str
    languages: list[str]
    status: str
    order: int
    initials: str
    url: str


def read_frontmatter(markdown_file: Path) -> dict[str, str]:
    """
    Read simple YAML-style frontmatter from a Markdown file.

    Example:

    ---
    title_nb: Norsk apptittel
    title_en: English apptitle
    description_nb: Norsk beskrivelse
    description_en: English description
    languages: nb,en
    status: Published
    order: 10
    initials: EA
    ---
    """

    content = markdown_file.read_text(encoding="utf-8")

    match = re.match(
        r"^\ufeff?---[ \t]*\r?\n"
        r"(.*?)"
        r"\r?\n---[ \t]*(?:\r?\n|$)",
        content,
        flags=re.DOTALL,
    )

    if not match:
        return {}

    metadata: dict[str, str] = {}

    for line in match.group(1).splitlines():
        stripped_line = line.strip()

        if not stripped_line:
            continue

        if stripped_line.startswith("#"):
            continue

        if ":" not in stripped_line:
            continue

        key, value = stripped_line.split(":", 1)

        clean_key = key.strip()
        clean_value = value.strip().strip("\"'")

        metadata[clean_key] = clean_value

    return metadata


def parse_order(value: str | None) -> int:
    """Convert order metadata to an integer."""

    if value is None:
        return 9999

    try:
        return int(value)
    except ValueError:
        return 9999


def parse_languages(value: str | None) -> list[str]:
    """
    Convert language metadata to normalized language codes.

    Examples:

    languages: nb,en
    languages: nb
    languages: no,en
    """

    if not value:
        return ["nb"]

    language_aliases = {
        "nb": "nb",
        "no": "nb",
        "norwegian": "nb",
        "norsk": "nb",
        "en": "en",
        "english": "en",
        "engelsk": "en",
    }

    languages: list[str] = []

    for item in value.split(","):
        normalized = item.strip().lower()
        language = language_aliases.get(normalized)

        if language and language not in languages:
            languages.append(language)

    return languages or ["nb"]


def make_initials(title: str) -> str:
    """
    Create short initials for the application card.

    Examples:
    Electro Authorization System -> EA
    Crane Inspection -> CI
    """

    ignored_words = {
        "and",
        "for",
        "of",
        "the",
        "og",
        "av",
    }

    words = [
        word
        for word in re.findall(
            r"[A-Za-zÆØÅæøå0-9]+",
            title,
        )
        if word.lower() not in ignored_words
    ]

    if not words:
        return "APP"

    if len(words) == 1:
        return words[0][:2].upper()

    return "".join(
        word[0]
        for word in words[:2]
    ).upper()


def get_apps() -> list[AppMetadata]:
    """
    Discover published applications under apps/*/index.md.
    """

    apps: list[AppMetadata] = []

    if not APPS_DIR.exists():
        print(
            f"Applications directory does not exist: "
            f"{APPS_DIR}"
        )
        return apps

    for app_directory in sorted(
        APPS_DIR.iterdir()
    ):
        if not app_directory.is_dir():
            continue

        index_file = app_directory / "index.md"

        if not index_file.exists():
            print(
                f"Skipping {app_directory.name}: "
                "apps/<app>/index.md was not found."
            )
            continue

        metadata = read_frontmatter(
            index_file
        )

        status = metadata.get(
            "status",
            "Published",
        ).strip()

        if status.lower() != "published":
            print(
                f"Skipping {app_directory.name}: "
                f"status is {status!r}."
            )
            continue

        app_id = app_directory.name

        default_title = (
            app_id
            .replace("-", " ")
            .replace("_", " ")
            .title()
        )

        # Support legacy "title" as fallback.
        title_nb = metadata.get(
            "title_nb",
            metadata.get(
                "title",
                default_title,
            ),
        )

        title_en = metadata.get(
            "title_en",
            metadata.get(
                "title",
                default_title,
            ),
        )

        description_nb = metadata.get(
            "description_nb",
            metadata.get(
                "description",
                (
                    "Brukerguide og dokumentasjon "
                    "for applikasjonen."
                ),
            ),
        )

        description_en = metadata.get(
            "description_en",
            metadata.get(
                "description",
                (
                    "User guide and documentation "
                    "for the application."
                ),
            ),
        )

        languages = parse_languages(
            metadata.get(
                "languages",
                metadata.get("language"),
            )
        )

        initials = metadata.get(
            "initials",
            make_initials(title_en),
        )

        apps.append(
            {
                "app_id": app_id,
                "title_nb": title_nb,
                "title_en": title_en,
                "description_nb": description_nb,
                "description_en": description_en,
                "languages": languages,
                "status": status,
                "order": parse_order(
                    metadata.get("order")
                ),
                "initials": initials,
                "url": f"apps/{app_id}/",
            }
        )

    return sorted(
        apps,
        key=lambda app: (
            app["order"],
            app["title_nb"].casefold(),
        ),
    )


def render_language_tags(
    languages: list[str],
) -> str:
    """Render available language tags."""

    labels = {
        "nb": "NO",
        "en": "EN",
    }

    tags: list[str] = []

    for language in languages:
        label = labels.get(
            language,
            language.upper(),
        )

        tags.append(
            f"""
            <span class="language-tag">
              {html.escape(label)}
            </span>
            """
        )

    return "\n".join(tags)


def render_sidebar_apps(
    apps: list[AppMetadata],
) -> str:
    """
    Render applications in the left navigation.
    """

    if not apps:
        return """
        <p
          class="portal-nav__empty"
          data-i18n="noPublishedGuides"
        >
          Ingen publiserte brukerguider
        </p>
        """

    items: list[str] = []

    for app in apps:
        title_nb = html.escape(
            app["title_nb"],
            quote=True,
        )

        title_en = html.escape(
            app["title_en"],
            quote=True,
        )

        url = html.escape(
            app["url"],
            quote=True,
        )

        items.append(
            f"""
            <a
              class="portal-nav__item"
              href="{url}"
            >
              <span
                class="portal-nav__app-indicator"
                aria-hidden="true"
              ></span>

              <span
                data-nb="{title_nb}"
                data-en="{title_en}"
              >
                {title_nb}
              </span>
            </a>
            """
        )

    return "\n".join(items)


def render_app_cards(
    apps: list[AppMetadata],
) -> str:
    """
    Render one card for each published application.
    """

    if not apps:
        return """
        <div class="portal-empty-state">
          <h3 data-i18n="noPublishedGuides">
            Ingen publiserte brukerguider
          </h3>

          <p data-i18n="guidesAppearAutomatically">
            Publiserte brukerguider vises
            automatisk her.
          </p>
        </div>
        """

    cards: list[str] = []

    for app in apps:
        title_nb = html.escape(
            app["title_nb"],
            quote=True,
        )

        title_en = html.escape(
            app["title_en"],
            quote=True,
        )

        description_nb = html.escape(
            app["description_nb"],
            quote=True,
        )

        description_en = html.escape(
            app["description_en"],
            quote=True,
        )

        initials = html.escape(
            app["initials"],
            quote=True,
        )

        url = html.escape(
            app["url"],
            quote=True,
        )

        language_tags = (
            render_language_tags(
                app["languages"]
            )
        )

        cards.append(
            f"""
            <article class="app-card">

              <div class="app-card__header">

                <div
                  class="app-card__icon"
                  aria-hidden="true"
                >
                  {initials}
                </div>

                <span
                  class="app-card__status"
                  data-i18n="publishedStatus"
                >
                  Publisert
                </span>

              </div>


              <div class="app-card__content">

                <p
                  class="app-card__eyebrow"
                  data-i18n="userGuide"
                >
                  Brukerguide
                </p>

                <h3
                  class="app-card__title"
                  data-nb="{title_nb}"
                  data-en="{title_en}"
                >
                  {title_nb}
                </h3>

                <p
                  class="app-card__description"
                  data-nb="{description_nb}"
                  data-en="{description_en}"
                >
                  {description_nb}
                </p>

              </div>


              <div class="app-card__footer">

                <div
                  class="app-card__languages"
                  aria-label="Tilgjengelige språk"
                >
                  {language_tags}
                </div>

                <a
                  class="eds-button"
                  href="{url}"
                  data-aria-label-nb=
                    "Åpne brukerguiden for {title_nb}"
                  data-aria-label-en=
                    "Open the user guide for {title_en}"
                  aria-label=
                    "Åpne brukerguiden for {title_nb}"
                >
                  <span data-i18n="openGuide">
                    Åpne brukerguide
                  </span>

                  <span aria-hidden="true">
                    →
                  </span>
                </a>

              </div>

            </article>
            """
        )

    return "\n".join(cards)


def build_translations() -> str:
    """
    Return translation data as JSON for JavaScript.
    """

    translations = {
        "nb": {
            "pageTitle": (
                "GTS DigiTeam | Brukerguider"
            ),
            "pageDescription": (
                "Brukerguider for applikasjoner "
                "utviklet av GTS DigiTeam."
            ),
            "skipLink": (
                "Hopp til hovedinnhold"
            ),
            "brandSubtitle": (
                "Brukerguider"
            ),
            "language": (
                "Språk"
            ),
            "languageSelectorLabel": (
                "Velg språk"
            ),
            "mainNavigation": (
                "Hovedmeny"
            ),
            "menu": (
                "Meny"
            ),
            "allGuides": (
                "Alle brukerguider"
            ),
            "applications": (
                "Applikasjoner"
            ),
            "maintainedBy": (
                "Vedlikeholdes av GTS DigiTeam"
            ),
            "documentation": (
                "Dokumentasjon"
            ),
            "title": (
                "Brukerguider"
            ),
            "ingress": (
                "Finn hurtigguider og "
                "brukerdokumentasjon for "
                "applikasjoner utviklet og "
                "vedlikeholdt av GTS DigiTeam."
            ),
            "availableGuides": (
                "Tilgjengelige brukerguider"
            ),
            "published": (
                "publisert"
            ),
            "publishedPlural": (
                "publiserte"
            ),
            "publishedStatus": (
                "Publisert"
            ),
            "userGuide": (
                "Brukerguide"
            ),
            "openGuide": (
                "Åpne brukerguide"
            ),
            "availableLanguages": (
                "Tilgjengelige språk"
            ),
            "footerText": (
                "Dokumentasjonen vedlikeholdes "
                "av GTS DigiTeam."
            ),
            "footerUpdated": (
                "Innholdet oppdateres automatisk "
                "ved publisering."
            ),
            "noPublishedGuides": (
                "Ingen publiserte brukerguider"
            ),
            "guidesAppearAutomatically": (
                "Publiserte brukerguider vises "
                "automatisk her."
            ),
        },
        "en": {
            "pageTitle": (
                "GTS DigiTeam | User guides"
            ),
            "pageDescription": (
                "User guides for applications "
                "developed by GTS DigiTeam."
            ),
            "skipLink": (
                "Skip to main content"
            ),
            "brandSubtitle": (
                "User guides"
            ),
            "language": (
                "Language"
            ),
            "languageSelectorLabel": (
                "Select language"
            ),
            "mainNavigation": (
                "Main menu"
            ),
            "menu": (
                "Menu"
            ),
            "allGuides": (
                "All user guides"
            ),
            "applications": (
                "Applications"
            ),
            "maintainedBy": (
                "Maintained by GTS DigiTeam"
            ),
            "documentation": (
                "Documentation"
            ),
            "title": (
                "User guides"
            ),
            "ingress": (
                "Find quick guides and user "
                "documentation for applications "
                "developed and maintained by "
                "GTS DigiTeam."
            ),
            "availableGuides": (
                "Available user guides"
            ),
            "published": (
                "published"
            ),
            "publishedPlural": (
                "published"
            ),
            "publishedStatus": (
                "Published"
            ),
            "userGuide": (
                "User guide"
            ),
            "openGuide": (
                "Open user guide"
            ),
            "availableLanguages": (
                "Available languages"
            ),
            "footerText": (
                "Documentation is maintained "
                "by GTS DigiTeam."
            ),
            "footerUpdated": (
                "Content is automatically updated "
                "when published."
            ),
            "noPublishedGuides": (
                "No user guides have been published"
            ),
            "guidesAppearAutomatically": (
                "Published user guides will appear "
                "here automatically."
            ),
        },
    }

    return json.dumps(
        translations,
        ensure_ascii=False,
        indent=2,
    )


def build_page(
    apps: list[AppMetadata],
) -> str:
    """Build the complete portal front page."""

    sidebar_apps = render_sidebar_apps(
        apps
    )

    app_cards = render_app_cards(
        apps
    )

    translations = build_translations()

    guide_count = len(apps)

    published_key = (
        "published"
        if guide_count == 1
        else "publishedPlural"
    )

    return f"""<!doctype html>
<html lang="nb" data-color-scheme="light">

<head>

  <meta charset="utf-8">

  <meta
    name="viewport"
    content="width=device-width, initial-scale=1"
  >

  <meta
    id="page-description"
    name="description"
    content="Brukerguider for applikasjoner utviklet av GTS DigiTeam."
  >

  <title>
    GTS DigiTeam | Brukerguider
  </title>

  <link
    rel="stylesheet"
    href="styles/userguide.css"
  >

</head>


<body class="portal-page">

  <a
    class="skip-link"
    href="#main-content"
    data-i18n="skipLink"
  >
    Hopp til hovedinnhold
  </a>


  <header class="portal-header">

    <a
      class="portal-brand"
      href="./"
    >

      <span
        class="portal-brand__mark"
        aria-hidden="true"
      ></span>

      <span class="portal-brand__text">

        <strong>
          GTS DigiTeam
        </strong>

        <span
          class="portal-brand__subtitle"
          data-i18n="brandSubtitle"
        >
          Brukerguider
        </span>

      </span>

    </a>


    <div class="language-selector">

      <span
        class="language-selector__label"
        data-i18n="language"
      >
        Språk
      </span>

      <div
        id="language-buttons"
        class="language-selector__buttons"
        role="group"
        aria-label="Velg språk"
      >

        <button
          type="button"
          class="language-button is-active"
          data-language="nb"
          aria-pressed="true"
        >
          NO
        </button>

        <button
          type="button"
          class="language-button"
          data-language="en"
          aria-pressed="false"
        >
          EN
        </button>

      </div>

    </div>

  </header>


  <div class="portal-layout">


    <aside class="portal-sidebar">

      <nav
        id="main-navigation"
        class="portal-nav"
        aria-label="Hovedmeny"
      >

        <p
          class="portal-nav__heading"
          data-i18n="menu"
        >
          Meny
        </p>


        <a
          class="portal-nav__item is-active"
          href="./"
          aria-current="page"
        >

          <span
            class="portal-nav__home-icon"
            aria-hidden="true"
          >
            <span
              class="portal-nav__home-roof"
            ></span>

            <span
              class="portal-nav__home-body"
            ></span>
          </span>

          <span data-i18n="allGuides">
            Alle brukerguider
          </span>

        </a>


        <p
          class="
            portal-nav__heading
            portal-nav__heading--apps
          "
          data-i18n="applications"
        >
          Applikasjoner
        </p>


        {sidebar_apps}

      </nav>


      <div class="portal-sidebar__footer">

        <p data-i18n="maintainedBy">
          Vedlikeholdes av GTS DigiTeam
        </p>

      </div>

    </aside>


    <main
      id="main-content"
      class="portal-main"
    >


      <section
        class="portal-hero"
        aria-labelledby="page-title"
      >

        <p
          class="portal-eyebrow"
          data-i18n="documentation"
        >
          Dokumentasjon
        </p>

        <h1
          id="page-title"
          data-i18n="title"
        >
          Brukerguider
        </h1>

        <p
          class="portal-ingress"
          data-i18n="ingress"
        >
          Finn hurtigguider og
          brukerdokumentasjon for
          applikasjoner utviklet og
          vedlikeholdt av GTS DigiTeam.
        </p>

      </section>


      <section
        class="portal-guides"
        aria-labelledby="guide-heading"
      >

        <div class="portal-section-header">

          <div>

            <p
              class="portal-eyebrow"
              data-i18n="applications"
            >
              Applikasjoner
            </p>

            <h2
              id="guide-heading"
              data-i18n="availableGuides"
            >
              Tilgjengelige brukerguider
            </h2>

          </div>


          <span class="portal-guide-count">

            <strong>
              {guide_count}
            </strong>

            <span
              data-i18n="{published_key}"
            >
              publisert
            </span>

          </span>

        </div>


        <div class="portal-card-grid">

          {app_cards}

        </div>

      </section>

    </main>

  </div>


  <footer class="portal-footer">

    <p data-i18n="footerText">
      Dokumentasjonen vedlikeholdes
      av GTS DigiTeam.
    </p>

    <p data-i18n="footerUpdated">
      Innholdet oppdateres automatisk
      ved publisering.
    </p>

  </footer>


  <script>
    (() => {{
      "use strict";

      const translations = {translations};

      const buttons = document.querySelectorAll(
        ".language-button"
      );

      function setLanguage(language) {{
        const text = translations[language];

        if (!text) {{
          return;
        }}

        document.documentElement.lang = language;

        document.querySelectorAll(
          "[data-i18n]"
        ).forEach((element) => {{
          const key = element.dataset.i18n;

          if (Object.prototype.hasOwnProperty.call(text, key)) {{
            element.textContent = text[key];
          }}
        }});

        document.querySelectorAll(
          "[data-nb][data-en]"
        ).forEach((element) => {{
          if (language === "en") {{
            element.textContent = element.dataset.en;
          }} else {{
            element.textContent = element.dataset.nb;
          }}
        }});

        document.querySelectorAll(
          "[data-aria-label-nb][data-aria-label-en]"
        ).forEach((element) => {{
          if (language === "en") {{
            element.setAttribute(
              "aria-label",
              element.dataset.ariaLabelEn
            );
          }} else {{
            element.setAttribute(
              "aria-label",
              element.dataset.ariaLabelNb
            );
          }}
        }});

        buttons.forEach((button) => {{
          const active =
            button.dataset.language === language;

          button.classList.toggle(
            "is-active",
            active
          );

          button.setAttribute(
            "aria-pressed",
            active ? "true" : "false"
          );
        }});

        document.title = text.pageTitle;
      }}

      buttons.forEach((button) => {{
        button.addEventListener("click", () => {{
          setLanguage(button.dataset.language);
        }});
      }});

      setLanguage("nb");
    }})();
  </script>

</body>

</html>
"""


def main() -> None:
    """Generate the portal front page."""

    apps = get_apps()

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output = build_page(
        apps
    )

    OUTPUT_FILE.write_text(
        output,
        encoding="utf-8",
    )

    print(
        f"Generated {OUTPUT_FILE} "
        f"with {len(apps)} published guide(s)."
    )

    for app in apps:
        print(
            f"  - "
            f"{app['title_nb']} / "
            f"{app['title_en']} "
            f"({', '.join(app['languages'])})"
        )


if __name__ == "__main__":
    main()
