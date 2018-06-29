# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


## Not released yet - Version 1.0 (Summer 2018)

### Added

- New professors module! Insert personal info like name, surname, photo, website and email. You can also link professors to their subjects!
- New marks module! Add your marks (also with weight) and let the software calculate your average!
- New agenda module! Add your events, like homework, exams or memos, setting a date, a title, a description and an attachment if you want!
- Added new inputs in subjects.
- Themes! Too bored of the Windows native style? Now you can use your preferred theme!
- Auto update program!! Every time you update the app, your database will be updated too automatically!
- You can choose if you want to receive updates for the app!
- Added docstrings and functions in the code

### Changed

- Refreshed menu screen
- Now updates notifications are divided into Alpha, Beta and Stable!
- Enhancements to settings, subjects and timetable screens, now there is a beatiful table and you can use right click!! (It opens a contestual menu, by the way! :) )
- General graphical enhancements
- Code enhancements (functionals and styling, following PEP 8 guidelines)
- Changed storage from File to SQLITE3
- Reduced a lot app start time and size. Who don't want a smaller and faster app?

### Fixed

- Transifex translations download issue is now solved!

### Removed

- Removed internal "Delete all data" feature. You have to open Documenti\School Life Diary folder manually. You cannot click DELETE ALL button in settings. Probably this feature will be back in 1.1.


## Version 0.3.0.1 (11/30/2017)

### Fixed
- Fixed a problem which caused an error on startup: some files aren't included with the last version installer.


## Version 0.3 (10/18/2017)

### Added
- Note management (title, description, attached file (with double-click opening). Notes that contain attachments will display the attachment if you double-click.
- New translation management: In addition to local translations, which are updated with each new version of the software, it will be possible to download new translations or update existing ones manually via the language change window.

### Changed
- Now subjjects will be automatically sorted alphabetically.
- UI enhancements

### Fixed
- Fixed the problem that caused the error when starting the program when you try to open it without the internet. The program searched for updates but because the connection is not connected, it ends the execution. The software will now run normally, but will display a warning about the connection failure.

## Version 0.2.1 (09/02/ 2017)

### Added
- Added a new menu with shortcuts and a new option to change language
- Added support for languages. Only Italian (it) and English (en) available for now

### Changed
- Code and Graphic Enhancements


## Version 0.2 (08/27/2017)

### Added
- Materials management with implementation in time
- Added the ability to back up data with its restore
- Added the ability to delete the entire application database (all files that contain the data application will be deleted, except backups). This function requires 3 confirmations to be executed.
- Link to the agenda (in the future will be integrated into the software)
- Link to the Mobile Votes section (in the future will be integrated into the software)

### Changed
- Graphic Enhancements: Now for Windows users it uses the theme base of your Windows version instead of the Windows XP / 2000 theme; While MAC and Linux users use the default theme (aqua for MAC)


## Version 0.1 (08/11/2017)
First beta version with full time management and related settings
- Initial interface
- Time management
- Main menu
- Settings