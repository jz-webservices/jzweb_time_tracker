# jzweb_time_tracker

Odoo-Modul zur einfachen Start/Stopp-Zeiterfassung mit automatischer Buchung ins Projekt-Timesheet.

## Funktionen

- **Systray-Timer**: Start/Stopp direkt aus der Odoo-Oberfläche (oben rechts)
- **Projekt & Aufgabe**: Beim Starten optional Projekt und Aufgabe auswählen
- **Automatische Timesheet-Buchung**: Beim Stoppen wird automatisch ein Eintrag in der Projektzeit (`account.analytic.line`) angelegt
- **Kalenderansicht**: Alle Zeiteinträge als Kalenderblöcke sichtbar
- **Listen-, Pivot- und Graphansicht**: Auswertungen nach Projekt, Mitarbeiter, Zeitraum
- **Dauern-Rundung**: Die exakte Stoppzeit bleibt erhalten – die gebuchte Dauer im Timesheet wird optional aufgerundet

## Einstellungen

Unter **Einstellungen → Time Tracker**:

| Option | Beschreibung |
|---|---|
| Keine Rundung | Dauer wird exakt ins Timesheet gebucht |
| 5 Minuten | Dauer wird auf die nächsten vollen 5 Min aufgerundet |
| 10 Minuten | Dauer wird auf die nächsten vollen 10 Min aufgerundet |
| 15 Minuten | Dauer wird auf die nächsten vollen 15 Min aufgerundet |
| 30 Minuten | Dauer wird auf die nächsten vollen 30 Min aufgerundet |

> Die Stoppzeit im TimeTracker selbst bleibt immer exakt. Die Rundung wirkt nur auf den `unit_amount`-Wert im Projekt-Timesheet.

## Abhängigkeiten

- `base`
- `project`
- `calendar`
- `hr_timesheet`

## Versionshistorie

| Version | Änderung |
|---|---|
| 1.6.0 | Rundung von Stoppzeit auf Timesheet-Dauer umgestellt |
| 1.5.0 | Systray-Timer, Kalender- und Graphansicht |
| 1.3.0 | Timesheet-Integration, Kunden-Feld, Sicherheitsrollen |
