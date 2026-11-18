# Browser observation index

Each row links to the captured rendered DOM at that step. A row may demonstrate a gap; this list is not a statement that all checks passed.

| ID | Observation |
|---|---|
| [UI-01](UI-01.txt) | Apply Electrical lock without a reason or note |
| [UI-02](UI-02.txt) | Unverified active Electrical lock blocks incoming Swing handover |
| [UI-03](UI-03.txt) | Active lock blocks first good part |
| [UI-04](UI-04.txt) | Technician cannot authorize release |
| [UI-05](UI-05.txt) | Supervisor cannot release active lock |
| [UI-06](UI-06.txt) | Removed but never zero-energy-verified lock permits supervisor release |
| [UI-07](UI-07.txt) | First good part at 12:00 accepted although recorded lock removal and release occurred at 14:00 |
| [UI-08](UI-08.txt) | Event closes despite historical missing zero-energy verification and first-good-part preceding release |
| [UI-09](UI-09.txt) | Sensorless machine opens manual event with no other inputs |
| [UI-10](UI-10.txt) | Missing closure fields are listed |
| [UI-11](UI-11.txt) | Empty repair entry rejected |
| [UI-12](UI-12.txt) | Repair note saved with automatic author and time and latest-next-action summary |
| [UI-13](UI-13.txt) | Running downtime reaches 30 minutes after two +15 controls |
| [UI-14](UI-14.txt) | First good part before stop is rejected |
| [UI-15](UI-15.txt) | Future first good part is rejected |
| [UI-16](UI-16.txt) | Confirmed downtime stays at 30 minutes after clock advances |
| [UI-17](UI-17.txt) | Coded no-lockout event closes with valid timing |
| [UI-18](UI-18.txt) | Repeated sensor stop keeps the same open event |
| [UI-19](UI-19.txt) | A new stop after first good part but before event closure is absorbed into old event and old clock stays stopped |
| [UI-20](UI-20.txt) | Verified still-active lock permits handover and records its applier |
| [UI-21](UI-21.txt) | At 06:29 previous-shift handover is awaiting acknowledgment |
| [UI-22](UI-22.txt) | At 06:30 previous-shift handover becomes Not acknowledged and list is highlighted |
| [UI-23](UI-23.txt) | Operator acknowledgment is refused |
| [UI-24](UI-24.txt) | Current-shift repair entry clears an overdue unacknowledged handover without recording an acknowledgment |
| [UI-25](UI-25.txt) | 06:10 first good part remains Awaiting verification at 21:59 |
| [UI-26](UI-26.txt) | No-repeat repair becomes Verified at end of next full Swing shift |
| [UI-27](UI-27.txt) | Uncoded pre-deadline new stop holds previous repair awaiting verification after deadline |
| [UI-28](UI-28.txt) | Late reason assignment reopens prior repair by stop timestamp and links repeat |
| [UI-29](UI-29.txt) | Reclassifying ongoing 07:00 stop as Electrical/Heater marks earlier Hydraulic fix Verified-ran-full-Swing despite no later first good part |
| [UI-30](UI-30.txt) | Earlier repair history displays Verified-ran-full-Swing while the current machine remains Open |
| [UI-31](UI-31.txt) | Photo-only browser upload attempt blocked before file selection by missing extension file-URL access |
| [UI-32](UI-32.txt) | Open repairs filter includes only Press 12 and Molder 8 with their summary and acknowledgment state |
| [UI-33](UI-33.txt) | All machines restores all six assets after filtering |
