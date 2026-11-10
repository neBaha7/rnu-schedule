# RNU Class Schedule

My class schedule from schedule.rnu.lv for 26 Oct to 25 Dec 2026, as an iOS-style web app and a PDF.

## Files

- `index.html` is the web app. It has day, week and course views and needs no build step. Open it in a browser, or serve it with GitHub Pages.
- `RNU_schedule_10Nov-25Dec_2026.pdf` is the printable schedule, 10 Nov to 25 Dec.
- `build_schedule.py` builds the PDF. Run `pip install reportlab` and then `python3 build_schedule.py`.

## Updating the schedule

The class data is typed in by hand from the site's month view.

- In `index.html`, add or change `addWeek(...)` lines in the schedule data section.
- In `build_schedule.py`, edit the `weeks` list.

## Known gaps

- Only start times are listed. The month view does not show rooms, lecturers or end times.
- Thu 12 Nov, 15:30 was cut off in the screenshot. It is assumed from the usual Thursday pattern and marked "to be confirmed".
- Nothing is listed after 25 Dec on the site.
