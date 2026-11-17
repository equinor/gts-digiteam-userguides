---
title_nb: Elektro Sikkerhetskort
title_en: Electrical Authorization System
description_nb: Hurtigguider og brukerdokumentasjon for Elektro Sikkerhetskort.
description_en: Quick guides and user documentation for Electrical Authorization System.
status: Published
order: 10
initials: EAS
---

# Quick guides - Electrical safety cards

These guides describe features available in the current app. Menu labels appear
in Norwegian or English depending on the language selected in your profile. You
must sign in with an Equinor account to use the app. The actions available to you
depend on the role and authority assigned to you for the selected installation.

The screenshots show representative test views with synthetic, anonymised data.
The numbered circles refer to the steps in the text; the same number may appear
in more than one place within a step. Appearance and available actions may vary
with your role, the selected installation and the app version. The screenshots
use Norwegian labels.

## Open the app

Test: https://apps.equinor.com/eas20test

Production: Coming soon

## 1. Installer - prepare and follow up the installation

**Prerequisite:** An Admin/Superuser has created and activated the installation
and assigned you the **Installer / person in charge** role. If the installation
or role is missing, contact an Admin/Superuser.

1. Select the correct installation using the selector at the top of the app.
2. Open **Installations**, select the installation and review the tabs:
   - **Details:** Check that you are viewing the correct installation. Changes
     to the installation's basic configuration and status are made by an
     Admin/Superuser.
   - **Contacts:** Keep Equinor contacts, external companies and contact persons
     up to date. The Installer and Deputy can maintain Equinor contacts. The
     Installer, Deputy and Delegated person can maintain external companies and
     contacts.
   - **Roles:** Assign or revoke roles as needed. Set the correct card
     authority, key authority and validity period. External roles must be
     linked to the correct company. Only delegate authority that you are
     permitted to delegate.
   - **Permissions:** Check the default permissions, add any necessary
     installation-specific permissions and maintain their order and associated
     instructions. Changes to the shared permission catalogue should be
     carefully considered; cardholders may need to sign again when their card's
     permissions change.

![Roles tab for a demo installation. Marker 1 shows the installation selector, and marker 2 shows the installation tabs.](../images/hurtigguider/installasjon-roller.png)

*Figure 1. Select the installation (1), then open the appropriate tab under Installations (2).*

3. Open **Instructions** for the installation. Create or edit an instruction,
   upload a new file version or add a link, and publish it once it has been
   checked. Only published instructions are current for normal viewing.
   Instructions are a separate library, not part of card signing.

![Instruction library for a demo installation. Marker 3 shows the Instructions menu item.](../images/hurtigguider/instrukser.png)

*Figure 2. Open Instructions in step 3.*

4. Return to **Installations > Reminders**. Set up who should receive email,
   how often it should be sent and whether it should cover expired cards,
   cards nearing expiry or keys that have not been returned. No email is sent
   when there is nothing to report.
5. Check that the roles, contact information, permissions, published
   instructions and reminders are correct before starting normal operations.

The Installer and Deputy have the same installation-specific authority in the
app. They can manage the installation's roles and instructions. They cannot
change global default configuration or perform Admin/Superuser functions.

## 2. Issue safety cards and manage keys

**Prerequisite:** You have card authority and/or key authority for the
installation. Check the installation selector before starting; selecting an
installation does not in itself grant permission.

### Create a card

1. Select the correct installation using the installation selector at the top
   of the app.
2. Open **Safety cards** and select **New safety card**.

![Safety card list for a demo installation. Marker 1 shows the installation selector, and marker 2 shows Safety cards and New safety card.](../images/hurtigguider/sikkerhetskort.png)

*Figure 3. Select the installation (1), then open the page and start the wizard (2).*

3. Find the person in the Office 365 directory if they have an Equinor account.
   Select **External without Equinor account** for a recipient without an
   account. Fill in any missing personal and company information.
4. Enter the validity dates and the date of the most recently completed FSE
   course. Specify the **Validity area** for high voltage and low voltage.
5. Select the card's **Permissions**, or explicitly select **No permissions**.
6. Select keys that have already been returned, register new keys to be handed
   out, or explicitly select **No keys handed out**.
7. Check the **Review** step and select **Complete and create card**. The card number
   is assigned automatically. Afterwards, check the signature status and any
   signing request in the card details.

There can only be one card per person per installation. Do not create a new
card if a card is still in force. A card that is no longer in force can be
reissued with the same card number; its previous history is retained.

### Renew cards

- A cardholder can request renewal from the card details. This is a request,
  not a renewal.
- With card authority, you can renew from the card details or select several
  cards in the card list and use **Renew selected cards**. Enter the FSE date
  and the new valid-to date. Check the result for each card; one card may fail
  even if others are renewed.
- Review the card history when you need to check previous changes or
  signatures.

### Hand out and take back keys

1. Open **Keys** and select **Hand out keys** or **Hand in keys**.

![Keys page for a demo installation. Marker 1 shows Keys, 2 Hand out keys and 3 Hand in keys.](../images/hurtigguider/nokler.png)

*Figure 4. Open Keys (1), then choose hand-out (2) or hand-in (3).*

2. When handing out a key, select an available key and link it to the correct
   active card. You can also register a new key and hand it out in the same
   workflow.
3. When taking back a key, select a key recorded as handed out. The return is
   recorded as a separate event; it does not overwrite the hand-out history.
4. Check the status and history in the key details. A key can be returned even
   if the associated card has expired.

You can send a new signing request from an unsigned card or key if you have the
appropriate authority. The recipient must confirm their own receipt; do not
sign on behalf of the cardholder.

## 3. Ordinary user - internal

**Prerequisite:** You are signed in with an Equinor account. As an ordinary
user, you can view your own information and perform actions for yourself. The
card and key lists may also show the installation's records in read-only mode;
this does not give you permission to change or sign other people's records.

1. Select the installation you want to view. **Overview** shows your relevant
   card/key tasks and any items awaiting your signature.
2. Open a card or key to view its details, validity, status and signature
   information.
3. When a signature is missing, select **Sign and accept** after checking the
   information. If you have received a Teams approval request, you can approve
   in Teams or sign in the app.

![Overview page in the app. Marker 1 shows the installation selector, 2 My actions and 3 Go to signing.](../images/hurtigguider/oversikt.png)

*Figure 5. Select the installation (1), find your tasks (2), and open signing (3).*

4. If you need a renewal, open the card and select **Request renewal**. A person
   with card authority must process the request. A request does not change the
   validity date until it has been processed.
5. Open **Instructions** to find published instructions for an installation.
   The card details may also link to relevant instructions.
6. From the card details, you can request a valid card as a PDF sent to the
   email address registered on the card.
7. Open **Profile** to save your preferred installation and language.

You can only sign receipt for your own cards and keys. If you cannot find your
card or an action you need, contact the installation's Installer / person in
charge.

## 4. Ordinary user - external

This guide applies to external personnel who have an Equinor account and sign
in to the app. As an ordinary user, follow the steps in **Ordinary user -
internal** for your own cards, signatures, renewal requests, instructions and
profile preferences. The overview in figure 5 also applies to external users;
the tasks and records you see depend on the installation and your role.

- Being registered as a cardholder or being able to sign in does not
  automatically grant card or key authority.
- You cannot create, change or renew other people's cards, hand out or take
  back other people's keys, or change the installation's roles and instructions
  without a specifically assigned role and authority.
- The card and key lists may show the installation's records in read-only mode.
  Signing and personal tasks apply to your own cards and keys; actions on other
  people's records require specific authority.

**Recipient without an Equinor account:** You are not a user of the app. When a
card or key is issued to you, you receive a signing link and a one-time code by
email. Open the link, enter the code in the form and confirm receipt. Use the
code before it expires, and do not share it. If the link or code is missing or
has expired, contact the person who issued the card or key for a new signing
request. This signing page does not grant access to the app or to other card
and key information.

## 5. External user with card and key authority

**Prerequisite:** You have an Equinor account and the **External installer** or
**External delegated person** role for the correct installation, with card
and/or key authority assigned.

1. Select the installation where you have been assigned the role. Check that
   your company is shown as the company for the assignment.
2. Create and maintain cards through **Safety cards**, in the same way as in
   the guide for card issuers. You can only select or register people from your
   own company at installations where you have authority.
3. When renewing, process cards covered by your card authority. Enter the FSE
   and validity dates, and check the result for each card.
4. Hand out and take back keys through **Keys**. Link each key to the correct
   active card in your own company. Check the key status and history afterwards.
5. If the recipient's signature is missing, you can send a new signing request
   for a card or key within your authority. The recipient signs for themselves.

The screenshots in figures 3 and 4 show the same card and key pages. The actions
available to you are limited to the installation, company and authority
assigned to you.

Your authority only applies to the assigned installation and your own company.
It does not grant access to manage the installation's permissions, contacts,
instructions or roles. You can view the installation's other card and key lists
in read-only mode, but cannot perform actions on records outside your own
company and assigned authority. If you need extended or renewed authority,
contact the installation's Installer / person in charge. An external recipient
without an Equinor account follows only the signing instructions in the previous
section and cannot perform issuer tasks in the app.
