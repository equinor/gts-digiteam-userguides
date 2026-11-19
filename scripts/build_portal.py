from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path
from typing import TypedDict

ROOT = Path(__file__).resolve().parents[1]
APPS_DIR = ROOT / "apps"
OUTPUT_FILE = ROOT / "_site" / "index.html"
STYLESHEET_FILE = ROOT / "styles" / "userguide.css"


class AppMetadata(TypedDict):
    app_id: str
    title_nb: str
    title_en: str
    description_nb: str
    description_en: str
    languages: list[str]
    order: int
    initials: str


def read_frontmatter(markdown_file: Path) -> dict[str, str]:
    content = markdown_file.read_text(encoding="utf-8")
    match = re.match(
        r"^\ufeff?---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)",
        content,
        flags=re.DOTALL,
    )
    if not match:
        return {}

    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("\"'")
    return metadata


def parse_order(value: str | None) -> int:
    try:
        return int(value) if value is not None else 9999
    except ValueError:
        return 9999


def make_initials(title: str) -> str:
    ignored = {"and", "for", "of", "the", "og", "av"}
    words = [
        word
        for word in re.findall(r"[A-Za-zÆØÅæøå0-9]+", title)
        if word.lower() not in ignored
    ]
    if not words:
        return "APP"
    if len(words) == 1:
        return words[0][:2].upper()
    return "".join(word[0] for word in words[:2]).upper()


def get_apps() -> list[AppMetadata]:
    apps: list[AppMetadata] = []
    if not APPS_DIR.exists():
        print(f"Applications directory does not exist: {APPS_DIR}")
        return apps

    for app_directory in sorted(APPS_DIR.iterdir()):
        if not app_directory.is_dir():
            continue

        app_id = app_directory.name
        nb_index = app_directory / "nb" / "index.md"
        en_index = app_directory / "en" / "index.md"
        languages = [
            language
            for language, path in (("nb", nb_index), ("en", en_index))
            if path.exists()
        ]

        if not languages:
            print(f"Skipping {app_id}: no nb/index.md or en/index.md found.")
            continue

        nb_metadata = read_frontmatter(nb_index) if nb_index.exists() else {}
        en_metadata = read_frontmatter(en_index) if en_index.exists() else {}
        metadata = {**en_metadata, **nb_metadata}

        status = metadata.get("status", "Published").strip()
        if status.lower() != "published":
            print(f"Skipping {app_id}: status is {status!r}.")
            continue

        default_title = app_id.replace("-", " ").replace("_", " ").title()
        legacy_title = metadata.get("title")
        title_nb = metadata.get("title_nb") or legacy_title or default_title
        title_en = metadata.get("title_en") or legacy_title or default_title

        if "title_nb" not in metadata:
            print(f"WARNING: {app_id} has no title_nb; using {title_nb!r}.")
        if "title_en" not in metadata:
            print(f"WARNING: {app_id} has no title_en; using {title_en!r}.")

        apps.append(
            {
                "app_id": app_id,
                "title_nb": title_nb,
                "title_en": title_en,
                "description_nb": metadata.get(
                    "description_nb",
                    "Brukerguide og dokumentasjon for applikasjonen.",
                ),
                "description_en": metadata.get(
                    "description_en",
                    "User guide and documentation for the application.",
                ),
                "languages": languages,
                "order": parse_order(metadata.get("order")),
                "initials": metadata.get("initials", make_initials(title_en)),
            }
        )

    return sorted(apps, key=lambda app: (app["order"], app["title_nb"].casefold()))


def app_data_attributes(app: AppMetadata) -> str:
    return (
        f'data-guide-app="{html.escape(app["app_id"], quote=True)}" '
        f'data-title-nb="{html.escape(app["title_nb"], quote=True)}" '
        f'data-title-en="{html.escape(app["title_en"], quote=True)}" '
        f'data-has-nb="{str("nb" in app["languages"]).lower()}" '
        f'data-has-en="{str("en" in app["languages"]).lower()}"'
    )


def render_language_tags(languages: list[str]) -> str:
    labels = {"nb": "NO", "en": "EN"}
    return "\n".join(
        f'<span class="language-tag">{labels.get(language, language.upper())}</span>'
        for language in languages
    )


def render_sidebar_apps(apps: list[AppMetadata]) -> str:
    if not apps:
        return '<p class="portal-nav__empty" data-i18n="noPublishedGuides">Ingen publiserte brukerguider</p>'

    items: list[str] = []
    for app in apps:
        title_nb = html.escape(app["title_nb"], quote=True)
        title_en = html.escape(app["title_en"], quote=True)
        initials = html.escape(
            (app["initials"].strip() or make_initials(app["title_en"]))[:3]
        )
        default_language = "nb" if "nb" in app["languages"] else "en"
        href = f'apps/{html.escape(app["app_id"], quote=True)}/{default_language}/'
        items.append(
            f'''<a class="portal-nav__item portal-app-link" href="{href}" {app_data_attributes(app)}>
  <span class="portal-nav__app-indicator" aria-hidden="true"><span class="portal-nav__app-initials">{initials}</span></span>
  <span class="portal-nav__label" data-nb="{title_nb}" data-en="{title_en}">{title_nb}</span>
</a>'''
        )
    return "\n".join(items)


def render_app_cards(apps: list[AppMetadata]) -> str:
    if not apps:
        return '''<div class="portal-empty-state">
  <h3 data-i18n="noPublishedGuides">Ingen publiserte brukerguider</h3>
  <p data-i18n="guidesAppearAutomatically">Publiserte brukerguider vises automatisk her.</p>
</div>'''

    cards: list[str] = []
    for app in apps:
        app_id = html.escape(app["app_id"], quote=True)
        title_nb = html.escape(app["title_nb"], quote=True)
        title_en = html.escape(app["title_en"], quote=True)
        description_nb = html.escape(app["description_nb"], quote=True)
        description_en = html.escape(app["description_en"], quote=True)
        initials = html.escape(app["initials"])
        default_language = "nb" if "nb" in app["languages"] else "en"
        href = f"apps/{app_id}/{default_language}/"
        cards.append(
            f'''<article class="app-card">
  <div class="app-card__header">
    <div class="app-card__icon" aria-hidden="true">{initials}</div>
    <span class="app-card__status" data-i18n="publishedStatus">Publisert</span>
  </div>
  <div class="app-card__content">
    <p class="app-card__eyebrow" data-i18n="userGuide">Brukerguide</p>
    <h3 class="app-card__title" data-nb="{title_nb}" data-en="{title_en}">{title_nb}</h3>
    <p class="app-card__description" data-nb="{description_nb}" data-en="{description_en}">{description_nb}</p>
  </div>
  <div class="app-card__footer">
    <div class="app-card__languages" aria-label="Tilgjengelige språk">
      {render_language_tags(app["languages"])}
    </div>
    <a class="eds-button portal-app-link" href="{href}" {app_data_attributes(app)}
       data-aria-label-nb="Åpne brukerguiden for {title_nb}"
       data-aria-label-en="Open the user guide for {title_en}"
       aria-label="Åpne brukerguiden for {title_nb}">
      <span data-i18n="openGuide">Åpne brukerguide</span>
      <span aria-hidden="true">→</span>
    </a>
  </div>
</article>'''
        )
    return "\n".join(cards)


def build_translations() -> str:
    translations = {
        "nb": {
            "pageTitle": "GTS DigiTeam | Brukerguider",
            "skipLink": "Hopp til hovedinnhold",
            "brandSubtitle": "Brukerguider",
            "language": "Språk",
            "menu": "Meny",
            "collapseMenu": "Komprimer meny",
            "expandMenu": "Utvid meny",
            "collapseMenuShort": "Komprimer",
            "expandMenuShort": "Utvid",
            "allGuides": "Alle brukerguider",
            "applications": "Applikasjoner",
            "maintainedBy": "Vedlikeholdes av GTS DigiTeam",
            "documentation": "Dokumentasjon",
            "title": "Brukerguider",
            "ingress": "Finn hurtigguider og brukerdokumentasjon for applikasjoner utviklet og vedlikeholdt av GTS DigiTeam.",
            "availableGuides": "Tilgjengelige brukerguider",
            "published": "publisert",
            "publishedPlural": "publiserte",
            "publishedStatus": "Publisert",
            "userGuide": "Brukerguide",
            "openGuide": "Åpne brukerguide",
            "openInNewTab": "Åpne i ny fane",
            "footerText": "Dokumentasjonen vedlikeholdes av GTS DigiTeam.",
            "footerUpdated": "Innholdet oppdateres automatisk ved publisering.",
            "noPublishedGuides": "Ingen publiserte brukerguider",
            "guidesAppearAutomatically": "Publiserte brukerguider vises automatisk her.",
        },
        "en": {
            "pageTitle": "GTS DigiTeam | User guides",
            "skipLink": "Skip to main content",
            "brandSubtitle": "User guides",
            "language": "Language",
            "menu": "Menu",
            "collapseMenu": "Collapse menu",
            "expandMenu": "Expand menu",
            "collapseMenuShort": "Collapse",
            "expandMenuShort": "Expand",
            "allGuides": "All user guides",
            "applications": "Applications",
            "maintainedBy": "Maintained by GTS DigiTeam",
            "documentation": "Documentation",
            "title": "User guides",
            "ingress": "Find quick guides and user documentation for applications developed and maintained by GTS DigiTeam.",
            "availableGuides": "Available user guides",
            "published": "published",
            "publishedPlural": "published",
            "publishedStatus": "Published",
            "userGuide": "User guide",
            "openGuide": "Open user guide",
            "openInNewTab": "Open in new tab",
            "footerText": "Documentation is maintained by GTS DigiTeam.",
            "footerUpdated": "Content is automatically updated when published.",
            "noPublishedGuides": "No user guides have been published",
            "guidesAppearAutomatically": "Published user guides will appear here automatically.",
        },
    }
    return json.dumps(translations, ensure_ascii=False)


def build_page(apps: list[AppMetadata]) -> str:
    guide_count = len(apps)
    published_key = "published" if guide_count == 1 else "publishedPlural"
    stylesheet_version = hashlib.sha256(STYLESHEET_FILE.read_bytes()).hexdigest()
    template = '''<!doctype html>
<html lang="nb" data-color-scheme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Brukerguider for applikasjoner utviklet av GTS DigiTeam.">
  <title>GTS DigiTeam | Brukerguider</title>
  <link rel="stylesheet" href="styles/userguide.css?v=__STYLESHEET_VERSION__">
</head>
<body class="portal-page">
  <a class="skip-link" href="#main-content" data-i18n="skipLink">Hopp til hovedinnhold</a>

  <header class="portal-header">
    <a class="portal-brand" href="./">
      <span class="portal-brand__mark" aria-hidden="true"></span>
      <span class="portal-brand__text">
        <strong>GTS DigiTeam</strong>
        <span class="portal-brand__subtitle" data-i18n="brandSubtitle">Brukerguider</span>
      </span>
    </a>
    <div class="language-selector">
      <span class="language-selector__label" data-i18n="language">Språk</span>
      <div class="language-selector__buttons" role="group" aria-label="Velg språk">
        <button type="button" class="language-button is-active" data-language="nb" aria-pressed="true">NO</button>
        <button type="button" class="language-button" data-language="en" aria-pressed="false">EN</button>
      </div>
    </div>
  </header>

  <div class="portal-layout">
    <aside class="portal-sidebar">
      <div class="portal-sidebar__header">
        <p class="portal-nav__heading" data-i18n="menu">Meny</p>
        <button id="portal-menu-toggle" class="portal-menu-toggle" type="button"
                aria-controls="portal-sidebar-nav" aria-expanded="true"
                aria-label="Komprimer meny" title="Komprimer meny" hidden>
          <svg class="portal-menu-toggle__icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
            <rect x="3" y="4" width="18" height="16" rx="2"></rect>
            <path d="M9 4v16"></path>
            <path id="portal-menu-toggle-arrow" d="m16 9-3 3 3 3"></path>
          </svg>
          <span id="portal-menu-toggle-text">Komprimer</span>
        </button>
      </div>
      <nav id="portal-sidebar-nav" class="portal-nav" aria-label="Hovedmeny">
        <a id="portal-home-link" class="portal-nav__item is-active" href="./" aria-current="page">
          <span class="portal-nav__home-icon" aria-hidden="true">
            <span class="portal-nav__home-roof"></span>
            <span class="portal-nav__home-body"></span>
          </span>
          <span class="portal-nav__label" data-i18n="allGuides">Alle brukerguider</span>
        </a>
        <p class="portal-nav__heading portal-nav__heading--apps" data-i18n="applications">Applikasjoner</p>
        __SIDEBAR_APPS__
      </nav>
      <div class="portal-sidebar__footer">
        <p data-i18n="maintainedBy">Vedlikeholdes av GTS DigiTeam</p>
      </div>
    </aside>

    <main id="main-content" class="portal-main">
      <section id="portal-hero" class="portal-hero" aria-labelledby="page-title">
        <p class="portal-eyebrow" data-i18n="documentation">Dokumentasjon</p>
        <h1 id="page-title" data-i18n="title">Brukerguider</h1>
        <p class="portal-ingress" data-i18n="ingress">Finn hurtigguider og brukerdokumentasjon for applikasjoner utviklet og vedlikeholdt av GTS DigiTeam.</p>
      </section>

      <section id="portal-home" class="portal-guides" aria-labelledby="guide-heading">
        <div class="portal-section-header">
          <div>
            <p class="portal-eyebrow" data-i18n="applications">Applikasjoner</p>
            <h2 id="guide-heading" data-i18n="availableGuides">Tilgjengelige brukerguider</h2>
          </div>
          <span class="portal-guide-count"><strong>__GUIDE_COUNT__</strong> <span data-i18n="__PUBLISHED_KEY__">publisert</span></span>
        </div>
        <div class="portal-card-grid">__APP_CARDS__</div>
      </section>

      <section id="guide-viewer" class="guide-viewer" aria-labelledby="guide-viewer-title" hidden>
        <div class="guide-viewer__header">
          <div>
            <p class="portal-eyebrow" data-i18n="userGuide">Brukerguide</p>
            <h1 id="guide-viewer-title" class="guide-viewer__title">Brukerguide</h1>
          </div>
          <a id="guide-direct-link" class="guide-viewer__direct-link" href="#" target="_blank" rel="noopener" data-i18n="openInNewTab">Åpne i ny fane</a>
        </div>
        <iframe id="guide-frame" class="guide-viewer__frame" title="Brukerguide" loading="eager"></iframe>
      </section>
    </main>
  </div>

  <footer class="portal-footer">
    <p data-i18n="footerText">Dokumentasjonen vedlikeholdes av GTS DigiTeam.</p>
    <p data-i18n="footerUpdated">Innholdet oppdateres automatisk ved publisering.</p>
  </footer>

  <script>
    (() => {
      "use strict";

      const translations = __TRANSLATIONS__;
      const languageButtons = document.querySelectorAll(".language-button");
      const appLinks = document.querySelectorAll(".portal-app-link");
      const navLinks = document.querySelectorAll(".portal-nav__item");
      const portalLayout = document.querySelector(".portal-layout");
      const menuToggle = document.getElementById("portal-menu-toggle");
      const menuToggleText = document.getElementById("portal-menu-toggle-text");
      const menuToggleArrow = document.getElementById("portal-menu-toggle-arrow");
      const homeLink = document.getElementById("portal-home-link");
      const portalHero = document.getElementById("portal-hero");
      const portalHome = document.getElementById("portal-home");
      const guideViewer = document.getElementById("guide-viewer");
      const guideFrame = document.getElementById("guide-frame");
      const guideTitle = document.getElementById("guide-viewer-title");
      const directLink = document.getElementById("guide-direct-link");
      const mobileLayout = window.matchMedia("(max-width: 720px)");

      let currentLanguage = "nb";
      let currentApp = null;
      let sidebarCollapsed = false;

      function updateSidebar() {
        const collapsed = sidebarCollapsed && !mobileLayout.matches;
        const text = translations[currentLanguage];
        const label = text[collapsed ? "expandMenu" : "collapseMenu"];
        portalLayout.classList.toggle("is-sidebar-collapsed", collapsed);
        menuToggle.setAttribute("aria-expanded", collapsed ? "false" : "true");
        menuToggle.setAttribute("aria-label", label);
        menuToggle.title = label;
        menuToggleText.textContent = text[collapsed ? "expandMenuShort" : "collapseMenuShort"];
        menuToggleArrow.setAttribute("d", collapsed ? "m13 9 3 3-3 3" : "m16 9-3 3 3 3");
      }

      function findAppLink(appId) {
        return Array.from(appLinks).find(
          (link) => link.dataset.guideApp === appId
        );
      }

      function targetLanguage(link, requestedLanguage) {
        const hasNb = link.dataset.hasNb === "true";
        const hasEn = link.dataset.hasEn === "true";
        if (requestedLanguage === "nb" && hasNb) return "nb";
        if (requestedLanguage === "en" && hasEn) return "en";
        if (hasNb) return "nb";
        if (hasEn) return "en";
        return null;
      }

      function appTitle(link, language) {
        return language === "en" ? link.dataset.titleEn : link.dataset.titleNb;
      }

      function setActiveNavigation(appId) {
        navLinks.forEach((item) => {
          const active = appId
            ? item.dataset.guideApp === appId
            : item.id === "portal-home-link";
          item.classList.toggle("is-active", active);
          if (active) item.setAttribute("aria-current", "page");
          else item.removeAttribute("aria-current");
        });
      }

      function replaceUrl(appId) {
        const url = new URL(window.location.href);
        if (appId) url.searchParams.set("app", appId);
        else url.searchParams.delete("app");
        url.searchParams.set("lang", currentLanguage);
        history.replaceState({ app: appId, lang: currentLanguage }, "", url);
      }

      function pushUrl(appId) {
        const url = new URL(window.location.href);
        if (appId) url.searchParams.set("app", appId);
        else url.searchParams.delete("app");
        url.searchParams.set("lang", currentLanguage);
        history.pushState({ app: appId, lang: currentLanguage }, "", url);
      }

      function showHome(updateHistory = true) {
        currentApp = null;
        guideFrame.removeAttribute("src");
        portalHero.hidden = false;
        portalHome.hidden = false;
        guideViewer.hidden = true;
        setActiveNavigation(null);
        if (updateHistory) pushUrl(null);
      }

      function openGuide(appId, updateHistory = true) {
        const link = findAppLink(appId);
        if (!link) {
          showHome(updateHistory);
          return;
        }

        const language = targetLanguage(link, currentLanguage);
        if (!language) {
          showHome(updateHistory);
          return;
        }

        currentApp = appId;
        const guideUrl = `apps/${appId}/${language}/`;
        const title = appTitle(link, currentLanguage);

        guideTitle.textContent = title;
        guideFrame.title = currentLanguage === "en"
          ? `User guide for ${title}`
          : `Brukerguide for ${title}`;
        guideFrame.src = guideUrl;
        directLink.href = guideUrl;

        portalHero.hidden = true;
        portalHome.hidden = true;
        guideViewer.hidden = false;
        setActiveNavigation(appId);

        if (updateHistory) pushUrl(appId);
        window.scrollTo({ top: 0, behavior: "smooth" });
      }

      function setLanguage(language, updateUrl = true) {
        const text = translations[language];
        if (!text) return;

        currentLanguage = language;
        document.documentElement.lang = language;
        document.title = text.pageTitle;

        document.querySelectorAll("[data-i18n]").forEach((element) => {
          const key = element.dataset.i18n;
          if (Object.prototype.hasOwnProperty.call(text, key)) {
            element.textContent = text[key];
          }
        });

        document.querySelectorAll("[data-nb][data-en]").forEach((element) => {
          element.textContent = language === "en"
            ? element.dataset.en
            : element.dataset.nb;
        });

        document.querySelectorAll("[data-aria-label-nb][data-aria-label-en]").forEach((element) => {
          element.setAttribute(
            "aria-label",
            language === "en"
              ? element.dataset.ariaLabelEn
              : element.dataset.ariaLabelNb
          );
        });

        languageButtons.forEach((button) => {
          const active = button.dataset.language === language;
          button.classList.toggle("is-active", active);
          button.setAttribute("aria-pressed", active ? "true" : "false");
        });

        updateSidebar();
        if (currentApp) openGuide(currentApp, false);
        if (updateUrl) replaceUrl(currentApp);
      }

      menuToggle.addEventListener("click", () => {
        sidebarCollapsed = !sidebarCollapsed;
        updateSidebar();
      });
      mobileLayout.addEventListener("change", updateSidebar);
      menuToggle.hidden = false;

      navLinks.forEach((link) => {
        const resetTooltip = () => link.classList.remove("is-tooltip-dismissed");
        link.addEventListener("pointerenter", resetTooltip);
        link.addEventListener("focus", resetTooltip);
      });
      document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
          navLinks.forEach((link) => link.classList.add("is-tooltip-dismissed"));
        }
      });

      appLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
          event.preventDefault();
          openGuide(link.dataset.guideApp);
        });
      });

      homeLink.addEventListener("click", (event) => {
        event.preventDefault();
        showHome();
      });

      languageButtons.forEach((button) => {
        button.addEventListener("click", () => {
          setLanguage(button.dataset.language);
        });
      });

      window.addEventListener("popstate", () => {
        const parameters = new URLSearchParams(window.location.search);
        const language = parameters.get("lang") === "en" ? "en" : "nb";
        const appId = parameters.get("app");
        setLanguage(language, false);
        if (appId) openGuide(appId, false);
        else showHome(false);
      });

      const parameters = new URLSearchParams(window.location.search);
      const initialLanguage = parameters.get("lang") === "en" ? "en" : "nb";
      const initialApp = parameters.get("app");
      setLanguage(initialLanguage, false);
      if (initialApp) openGuide(initialApp, false);
      else showHome(false);
      replaceUrl(currentApp);
    })();
  </script>
</body>
</html>
'''

    return (
        template
        .replace("__SIDEBAR_APPS__", render_sidebar_apps(apps))
        .replace("__APP_CARDS__", render_app_cards(apps))
        .replace("__GUIDE_COUNT__", str(guide_count))
        .replace("__PUBLISHED_KEY__", published_key)
        .replace("__STYLESHEET_VERSION__", stylesheet_version)
        .replace("__TRANSLATIONS__", build_translations())
    )


def main() -> None:
    apps = get_apps()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(build_page(apps), encoding="utf-8")
    print(f"Generated {OUTPUT_FILE} with {len(apps)} published guide(s).")
    for app in apps:
        print(
            f"  - {app['title_nb']} / {app['title_en']} "
            f"({', '.join(app['languages'])})"
        )


if __name__ == "__main__":
    main()
