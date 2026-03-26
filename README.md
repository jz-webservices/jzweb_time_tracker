# jzweb_time_tracker

**Odoo-Version: 19.0**

Odoo-Modul zur einfachen Start/Stopp-Zeiterfassung mit automatischer Buchung ins Projekt-Timesheet.

## Funktionen

- **Systray-Timer**: Start/Stopp direkt aus der Odoo-Oberfläche (oben rechts)
- **Projekt & Aufgabe**: Beim Starten optional Projekt und Aufgabe auswählen (nur offene Tasks werden angezeigt)
- **Automatische Timesheet-Buchung**: Beim Stoppen wird automatisch ein Eintrag in der Projektzeit (`account.analytic.line`) angelegt
- **Kalenderansicht**: Alle Zeiteinträge als Kalenderblöcke sichtbar
- **Listen-, Pivot- und Graphansicht**: Auswertungen nach Projekt, Mitarbeiter, Kunde und Zeitraum
- **Dauern-Rundung**: Die exakte Stoppzeit bleibt erhalten – die gebuchte Dauer im Timesheet wird optional aufgerundet
- **Manuelle Nacherfassung**: Vergessene Zeiten können nachgetragen werden – Start- und Endzeit manuell eingeben, Eintrag wird direkt als erledigt gespeichert

## Einstellungen

Unter **Einstellungen → Time Tracker**:

| Option | Beschreibung |
|---|---|
| Keine Rundung | Dauer wird exakt ins Timesheet gebucht (Standard) |
| 5 Minuten | Dauer wird auf die nächsten vollen 5 Min aufgerundet |
| 10 Minuten | Dauer wird auf die nächsten vollen 10 Min aufgerundet |
| 15 Minuten | Dauer wird auf die nächsten vollen 15 Min aufgerundet |
| 30 Minuten | Dauer wird auf die nächsten vollen 30 Min aufgerundet |

> Die Stoppzeit im TimeTracker selbst bleibt immer exakt. Die Rundung wirkt nur auf den `unit_amount`-Wert im Projekt-Timesheet.

> Der Standardwert wird bei jedem Modul-Upgrade automatisch auf **Keine Rundung** zurückgesetzt.

## Voraussetzungen

- **Odoo 19.0** (andere Versionen werden nicht unterstützt)
- Die folgenden Odoo-Module müssen installiert sein:

| Modul | Beschreibung |
|---|---|
| `base` | Odoo-Grundmodul (immer vorhanden) |
| `project` | Projektverwaltung |
| `calendar` | Kalenderansicht |
| `hr_timesheet` | Projekt-Timesheet & Mitarbeiterverwaltung |

> **Wichtig:** `hr_timesheet` bringt die Mitarbeiterverwaltung (`hr`) mit. Jeder Benutzer, der den Time Tracker verwenden soll, muss unter **Mitarbeiter** als Mitarbeiter angelegt und mit seinem Odoo-Benutzer verknüpft sein. Fehlt diese Verknüpfung, wird kein Timesheet-Eintrag erstellt.

## Installation

1. Den Ordner `jzweb_time_tracker` in das Odoo-`addons`-Verzeichnis kopieren.
2. Odoo neu starten.
3. Im Odoo-Backend den **Entwicklermodus** aktivieren (Einstellungen → Allgemein → Entwicklermodus).
4. Unter **Apps → App-Liste aktualisieren** klicken.
5. Nach `Time Tracker` suchen und installieren.

## Versionshistorie

| Version | Änderung |
|---|---|
| 1.10.0 | Manuelle Nacherfassung: Start + End manuell eingeben → direkt als erledigt speichern |
| 1.9.0 | Task-Dropdown filtert abgeschlossene/stornierte Tasks heraus |
| 1.8.0 | Zeitaufrollung wird bei Upgrade automatisch auf 0 zurückgesetzt |
| 1.6.0 | Rundung von Stoppzeit auf Timesheet-Dauer umgestellt |
| 1.5.0 | Systray-Timer, Kalender- und Graphansicht |
| 1.3.0 | Timesheet-Integration, Kunden-Feld, Sicherheitsrollen |
