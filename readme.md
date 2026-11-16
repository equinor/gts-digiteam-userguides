# Application User Guides | Brukerguider for applikasjoner

🇳🇴 #norsk | 🇬🇧 #english

---

# Norsk

## Om dette repoet

Dette repoet inneholder offentlig tilgjengelige brukerguider og dokumentasjon
for applikasjoner utviklet og vedlikeholdt av GTS Digiteam.

Formålet er å tilby ett felles sted for publisering av brukerdokumentasjon som
kan deles med brukere uten at de trenger en GitHub-konto.

## 📚 Tilgjengelige brukerguider

Brukerguidene organiseres etter applikasjon.

Hver applikasjon skal ha sin egen mappe:

```text
/
├── apps/
│   ├── app-name/
│   │   ├── index.html
│   │   └── assets/
│   │
│   └── another-app/
│       ├── index.html
│       └── assets/
│
└── README.md
```

Guidene publiseres som nettsider ved hjelp av GitHub Pages.

## 🌐 Publisering

Dokumentasjonen i dette repoet publiseres ved hjelp av GitHub Pages.

Brukerguider kan vedlikeholdes direkte i dette repoet eller publiseres
automatisk fra applikasjonens utviklingsrepo ved hjelp av GitHub Actions.

En typisk publiseringsflyt er:

```text
Applikasjonens private repo
            │
            │ GitHub Actions
            ▼
Dette offentlige repoet
            │
            │ GitHub Pages
            ▼
Offentlig brukerguide
```

Dette gjør at applikasjonens kildekode kan forbli privat, samtidig som
brukerdokumentasjonen kan gjøres offentlig tilgjengelig.

## ➕ Legge til en ny applikasjon

Opprett en egen mappe under `apps` for hver applikasjon.

Eksempel:

```text
/apps/safety-card/
/apps/installation-roles/
/apps/equipment-register/
```

Anbefalt startside for hver brukerguide er:

```text
index.html
```

Dette gir en ryddig URL:

```text
https://<organization>.github.io/<repository>/apps/installation-roles/
```

fremfor:

```text
https://<organization>.github.io/<repository>/apps/installation-roles/user-guide.html
```

## 🔄 Automatisk publisering

Når dokumentasjonen vedlikeholdes sammen med applikasjonens kildekode,
anbefales det å publisere brukerguiden automatisk ved hjelp av GitHub Actions.

Workflowen bør:

1. Kjøre når dokumentasjonen endres på applikasjonens `main`-branch.
2. Kopiere kun filer som er ment for offentlig publisering.
3. Publisere filene til applikasjonens mappe i dette repoet.
4. Committe endringene ved hjelp av GitHub Actions.
5. La GitHub Pages publisere den oppdaterte dokumentasjonen.

Dette holder den offentlige dokumentasjonen synkronisert med applikasjonen,
samtidig som det opprettholdes et tydelig skille mellom offentlig dokumentasjon
og privat kildekode.

## 🔒 Viktig: Dette er et offentlig repo

Alt som legges i dette repoet må betraktes som offentlig tilgjengelig.

**Ikke publiser:**

- passord eller credentials
- API-nøkler eller access tokens
- connection strings
- interne systemadresser
- personlig eller konfidensiell informasjon
- produksjonsdata
- sensitive skjermbilder
- kildekode som ikke er ment for offentlig distribusjon

Innhold skal gjennomgås før det publiseres.

## 🛠 Vedlikehold

GTS Digiteam er ansvarlige for å holde brukerguidene oppdatert når
funksjonalitet eller arbeidsprosesser i applikasjonene endres.

Der det er mulig bør oppdatering av dokumentasjonen være en del av den
ordinære utviklings- og releaseprosessen.

---

# English

## About this repository

This repository contains publicly available user guides and documentation for
applications developed and maintained by GTS Digiteam.

The purpose is to provide a common location for publishing application
documentation that can be shared with users without requiring a GitHub account.

## 📚 Available user guides

User guides are organized by application.

Each application should have its own folder:

```text
/
├── apps/
│   ├── app-name/
│   │   ├── index.html
│   │   └── assets/
│   │
│   └── another-app/
│       ├── index.html
│       └── assets/
│
└── README.md
```

The guides are published as websites using GitHub Pages.

## 🌐 Publishing

Documentation in this repository is published using GitHub Pages.

User guides may be maintained directly in this repository or automatically
published from the application's development repository using GitHub Actions.

A typical publishing flow is:

```text
Private application repository
            │
            │ GitHub Actions
            ▼
This public repository
            │
            │ GitHub Pages
            ▼
Public user guide
```

This allows the application source code to remain private while the user
documentation is made publicly available.

## ➕ Adding a new application

Create a separate folder under `apps` for each application.

For example:

```text
/apps/safety-card/
/apps/installation-roles/
/apps/equipment-register/
```

The recommended entry point for each user guide is:

```text
index.html
```

This provides clean URLs such as:

```text
https://<organization>.github.io/<repository>/apps/installation-roles/
```

instead of:

```text
https://<organization>.github.io/<repository>/apps/installation-roles/user-guide.html
```

## 🔄 Automated publishing

When documentation is maintained together with an application's source code,
the preferred approach is to publish the user guide automatically using
GitHub Actions.

The workflow should:

1. Run when documentation changes on the application's `main` branch.
2. Copy only files intended for public distribution.
3. Publish the files to the application's folder in this repository.
4. Commit the changes using GitHub Actions.
5. Let GitHub Pages publish the updated documentation.

This keeps the public documentation synchronized with the application while
maintaining a clear separation between public documentation and private
source code.

## 🔒 Important: This is a public repository

Everything committed to this repository must be considered publicly
accessible.

**Do not publish:**

- passwords or credentials
- API keys or access tokens
- connection strings
- internal system URLs
- personal or confidential information
- production data
- sensitive screenshots
- source code that is not intended for public distribution

Content should be reviewed before it is published.

## 🛠 Maintenance

GTS Digiteam is responsible for keeping the user guides up to date
when functionality or user workflows change.

Where possible, documentation updates should be included as part of the normal
application development and release process.

---

## Repository scope

This repository is intended for **published application documentation and
user guides only**.

Application source code, configuration, deployment files and other development
artifacts should remain in their respective development repositories.
