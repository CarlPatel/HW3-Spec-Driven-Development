"""Full combined model of the three stakeholders, removing equivalent goals only.
Run: python goal_model_all.py
Outputs: goal_model_all.mmd and mermaid_all.txt beside this file.
The compact diagram retains goals, refinements, and agent responsibility links;
repetitive operation nodes are omitted to stay within Mermaid edge limits.

132 goals retain all 137 original goals' evidence. IDs are G-1 through G-132.
SOURCE-G IDs identify the individual input goals and are not current model IDs.
MERGED_SOURCE_GOALS documents the five duplicate pairs and retained wording.
Distinct conditions, mechanisms, broad objectives, and agent responsibilities
remain separate. In particular, reason-code enforcement differs from an inferred
prompt; event logging differs from release authorization; safety verification
differs from sensor alerts; maintenance handoff differs from isolation release.

Original partial refinements and OR alternatives are preserved, with duplicate
edges and self-edges removed after merging. Parent-child merges inherit the
remaining children. H4/H5 annotations describe the source draft construction;
no new claim of exhaustive refinement or satisfaction is made.
Yellow nodes are inherited inferred goals and require stakeholder validation.
The five deduplication rewrites combine supported information without adding
requirements. Leaf borders are used only where an agent exists and no refinement
remains. Team roles and soft-goal acceptance criteria still need validation.
Physical isolation and safety are human controls; a record is not an interlock.
Release fields apply at release, not as a demand to release during handoff.

The existing 22-goal overview matrix and use cases have not been renumbered to
this model: its goal IDs form a separate model version and need remapping if used.
"""
from pathlib import Path
from goalmodeling.schema import (AchieveGoal, MaintainGoal, AvoidGoal, SoftGoal,
 Agent, AgentType, Operation, OperationCategory, PerformanceLink, Refinement,
 generate_graph, generate_pako_link)

SOURCE_GOALS = {'G-1': {'type': 'MaintainGoal',
         'category': 'functional',
         'text': 'Molding presses remain operational',
         'sources': [{'timestamp': '2026-10-28T12:45:51.599Z',
                      'quote': 'I keep the molding presses running—troubleshoot faults, make repairs, and '
                               'handle the scheduled maintenance on night shift.',
                      'stakeholder': 'Teo',
                      'original_goal_id': 'SOURCE-G-1'}],
         'inferred': False,
         'interpretation': '',
         'original_goal_ids': ['SOURCE-G-1'],
         'stakeholders': ['Teo'],
         'agents': []},
 'G-2': {'type': 'SoftGoal',
         'category': 'non-functional',
         'text': 'Time lost during diagnosis, repairs, and shift handoff is minimized',
         'sources': [{'timestamp': '2026-10-28T12:52:57.806Z',
                      'quote': 'The main bottleneck is the asynchronous data entry and poor shift-to-shift '
                               'handoff. I’m troubleshooting from fault codes, machine state, and component '
                               'test results, but the CMMS history is often stale or inconsistently coded, '
                               'so I lose time duplicating diagnostics and validating whether the fault is '
                               'intermittent or recurring.',
                      'stakeholder': 'Teo',
                      'original_goal_id': 'SOURCE-G-2'}],
         'inferred': False,
         'interpretation': '',
         'original_goal_ids': ['SOURCE-G-2'],
         'stakeholders': ['Teo'],
         'agents': []},
 'G-3': {'type': 'AchieveGoal',
         'category': 'functional',
         'text': 'Recent faults and prior repairs for the selected press are displayed on the tablet at the '
                 'press',
         'sources': [{'timestamp': '2026-10-28T12:49:41.850Z',
                      'quote': 'Yes, it can hide recurring faults—especially when the same repair gets '
                               'written in different ways or not at all. I’d want the tablet to show recent '
                               'faults and repairs for that press while I’m standing at it, and let me add a '
                               'quick note as soon as I find the cause, so we can see when “the usual” is '
                               'happening again.',
                      'stakeholder': 'Teo',
                      'original_goal_id': 'SOURCE-G-3'},
                     {'timestamp': '2026-10-28T12:49:41.850Z',
                      'quote': 'Yes, it can hide recurring faults—especially when the same repair gets '
                               'written in different ways or not at all. I’d want the tablet to show recent '
                               'faults and repairs for that press while I’m standing at it, and let me add a '
                               'quick note as soon as I find the cause, so we can see when “the usual” is '
                               'happening again.',
                      'stakeholder': 'Teo',
                      'original_goal_id': 'SOURCE-G-4'}],
         'inferred': False,
         'interpretation': '',
         'original_goal_ids': ['SOURCE-G-3', 'SOURCE-G-4'],
         'stakeholders': ['Teo'],
         'agents': ['system']},
 'G-4': {'type': 'AchieveGoal',
         'category': 'functional',
         'text': 'Previous-shift tests, changes, and repair outcomes are displayed',
         'sources': [{'timestamp': '2026-10-28T13:01:03.537Z',
                      'quote': 'Yeah, that’s right. The handoff is where we lose time—knowing what was '
                               'tried, what changed, and whether it actually held. If I can see that at the '
                               'press and leave my own note there, the next shift won’t be starting from '
                               'zero.',
                      'stakeholder': 'Teo',
                      'original_goal_id': 'SOURCE-G-5'}],
         'inferred': False,
         'interpretation': '',
         'original_goal_ids': ['SOURCE-G-5'],
         'stakeholders': ['Teo'],
         'agents': ['system']},
 'G-5': {'type': 'AchieveGoal',
         'category': 'functional',
         'text': 'History and live sensor readings are displayed together',
         'sources': [{'timestamp': '2026-10-28T12:58:12.153Z',
                      'quote': 'Let me think… when I’m at a press, I need the recent fault history and live '
                               'readings together, not buried in separate screens. If a sensor saw the '
                               'temperature drifting before the alarm, show that beside the repair notes, '
                               'and let me pull up the right spare part and its location quickly.',
                      'stakeholder': 'Teo',
                      'original_goal_id': 'SOURCE-G-6'}],
         'inferred': False,
         'interpretation': '',
         'original_goal_ids': ['SOURCE-G-6'],
         'stakeholders': ['Teo'],
         'agents': ['system']},
 'G-6': {'type': 'AchieveGoal',
         'category': 'functional',
         'text': 'Pre-alarm temperature drift is displayed beside repair notes if a sensor recorded it',
         'sources': [{'timestamp': '2026-10-28T12:58:12.153Z',
                      'quote': 'Let me think… when I’m at a press, I need the recent fault history and live '
                               'readings together, not buried in separate screens. If a sensor saw the '
                               'temperature drifting before the alarm, show that beside the repair notes, '
                               'and let me pull up the right spare part and its location quickly.',
                      'stakeholder': 'Teo',
                      'original_goal_id': 'SOURCE-G-7'}],
         'inferred': False,
         'interpretation': '',
         'original_goal_ids': ['SOURCE-G-7'],
         'stakeholders': ['Teo'],
         'agents': ['system']},
 'G-7': {'type': 'AchieveGoal',
         'category': 'functional',
         'text': 'Technicians record machine stops, maintenance findings, and repair actions on tablets at '
                 'the press',
         'sources': [{'timestamp': '2026-10-28T12:57:07.862Z',
                      'quote': 'Right. Short prompts, not a full form. If I’m at Press 7 with gloves on and '
                               'the floor noise going, I need to capture the fault, what I checked, what I '
                               'changed, and whether it held without walking off to a computer.',
                      'stakeholder': 'Teo',
                      'original_goal_id': 'SOURCE-G-8'},
                     {'timestamp': '2026-10-28T16:59:04.516Z',
                      'quote': 'Well, last month a molding press on our bottleneck line failed during a '
                               'large automotive order, and we lost 86 minutes before the first good part '
                               'was produced. I’d want the technician to log the stop and repair on the '
                               'tablet while the system captures downtime in minutes, requires a reason '
                               'code, and shows the impact against the production order so I can prioritize '
                               'the next response based on facts rather than radio calls.',
                      'stakeholder': 'Angela',
                      'original_goal_id': 'SOURCE-G-41'}],
         'inferred': False,
         'interpretation': '',
         'original_goal_ids': ['SOURCE-G-8', 'SOURCE-G-41'],
         'stakeholders': ['Teo', 'Angela'],
         'agents': ['technician']},
 'G-8': {'type': 'AchieveGoal',
         'category': 'functional',
         'text': 'Fault code, symptoms, alarms, and meter readings are recorded for the press',
         'sources': [{'timestamp': '2026-10-28T12:50:56.871Z',
                      'quote': 'I note the fault code, symptoms, meter readings, alarms, components tested, '
                               'parts changed, and whether the repair held through a production run. I’ll '
                               'also write down machine-specific quirks—things like a connector that needs '
                               'reseating or a heater zone that drifts before it fails.',
                      'stakeholder': 'Teo',
                      'original_goal_id': 'SOURCE-G-9'}],
         'inferred': False,
         'interpretation': '',
         'original_goal_ids': ['SOURCE-G-9'],
         'stakeholders': ['Teo'],
         'agents': ['technician']},
 'G-9': {'type': 'AchieveGoal',
         'category': 'functional',
         'text': 'Components tested and their results are recorded',
         'sources': [{'timestamp': '2026-10-28T12:52:57.806Z',
                      'quote': 'The main bottleneck is the asynchronous data entry and poor shift-to-shift '
                               'handoff. I’m troubleshooting from fault codes, machine state, and component '
                               'test results, but the CMMS history is often stale or inconsistently coded, '
                               'so I lose time duplicating diagnostics and validating whether the fault is '
                               'intermittent or recurring.',
                      'stakeholder': 'Teo',
                      'original_goal_id': 'SOURCE-G-10'}],
         'inferred': False,
         'interpretation': '',
         'original_goal_ids': ['SOURCE-G-10'],
         'stakeholders': ['Teo'],
         'agents': ['technician']},
 'G-10': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Changed parts and corrective actions are recorded',
          'sources': [{'timestamp': '2026-10-28T12:53:38.355Z',
                       'quote': 'Yeah, the entries aren’t always consistent—one tech logs a high-temp '
                                'deviation, another just writes “heater issue.” Part numbers, fault codes, '
                                'and corrective actions get mixed together, so the next shift has to '
                                'reconstruct the diagnostic trail.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-11'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-11'],
          'stakeholders': ['Teo'],
          'agents': ['technician']},
 'G-11': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Whether the repair held through a production run is recorded',
          'sources': [{'timestamp': '2026-10-28T12:50:56.871Z',
                       'quote': 'I note the fault code, symptoms, meter readings, alarms, components tested, '
                                'parts changed, and whether the repair held through a production run. I’ll '
                                'also write down machine-specific quirks—things like a connector that needs '
                                'reseating or a heater zone that drifts before it fails.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-12'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-12'],
          'stakeholders': ['Teo'],
          'agents': ['technician']},
 'G-12': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'A quick note is recorded when the cause is found',
          'sources': [{'timestamp': '2026-10-28T12:49:41.850Z',
                       'quote': 'Yes, it can hide recurring faults—especially when the same repair gets '
                                'written in different ways or not at all. I’d want the tablet to show recent '
                                'faults and repairs for that press while I’m standing at it, and let me add '
                                'a quick note as soon as I find the cause, so we can see when “the usual” is '
                                'happening again.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-13'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-13'],
          'stakeholders': ['Teo'],
          'agents': ['technician']},
 'G-13': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'A failed-part photo is attached to the repair record',
          'sources': [{'timestamp': '2026-10-28T12:57:29.710Z',
                       'quote': 'Right. With gloves on, I’m not typing a paragraph while Press 7 is waiting. '
                                'Let me snap a photo of the failed part or leave a short voice note, then I '
                                'can clean it up later if needed.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-14'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-14'],
          'stakeholders': ['Teo'],
          'agents': ['system']},
 'G-14': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'A short voice note is attached to the repair record',
          'sources': [{'timestamp': '2026-10-28T12:57:29.710Z',
                       'quote': 'Right. With gloves on, I’m not typing a paragraph while Press 7 is waiting. '
                                'Let me snap a photo of the failed part or leave a short voice note, then I '
                                'can clean it up later if needed.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-15'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-15'],
          'stakeholders': ['Teo'],
          'agents': ['system']},
 'G-15': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'An initial repair note can be cleaned up later if needed',
          'sources': [{'timestamp': '2026-10-28T12:57:29.710Z',
                       'quote': 'Right. With gloves on, I’m not typing a paragraph while Press 7 is waiting. '
                                'Let me snap a photo of the failed part or leave a short voice note, then I '
                                'can clean it up later if needed.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-16'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-16'],
          'stakeholders': ['Teo'],
          'agents': ['system']},
 'G-16': {'type': 'SoftGoal',
          'category': 'non-functional',
          'text': 'Maintenance entry is quick and usable with gloves in a noisy shop floor',
          'sources': [{'timestamp': '2026-10-28T12:57:07.862Z',
                       'quote': 'Right. Short prompts, not a full form. If I’m at Press 7 with gloves on and '
                                'the floor noise going, I need to capture the fault, what I checked, what I '
                                'changed, and whether it held without walking off to a computer.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-17'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-17'],
          'stakeholders': ['Teo'],
          'agents': []},
 'G-17': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Short prompts request what was tested, changed, and whether the repair held',
          'sources': [{'timestamp': '2026-10-28T12:56:32.600Z',
                       'quote': 'Not exactly. It’s less that they’re bad at notes and more that the '
                                'free-range box doesn’t remind them to capture what was tested, what '
                                'changed, or whether the repair held, especially when the line’s down. A few '
                                'quick prompts would help, as long as it doesn’t turn into a long form.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-18'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-18'],
          'stakeholders': ['Teo'],
          'agents': ['system']},
 'G-18': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'A few simple entry fields and an adjacent free note are available',
          'sources': [{'timestamp': '2026-10-28T12:54:54.481Z',
                       'quote': 'A few simple fields with a free note beside them. Don’t make me fill out a '
                                'dozen boxes while the press is down.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-19'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-19'],
          'stakeholders': ['Teo'],
          'agents': ['system']},
 'G-19': {'type': 'SoftGoal',
          'category': 'non-functional',
          'text': 'Required entry avoids lengthy forms and excessive categorization',
          'sources': [{'timestamp': '2026-10-28T12:50:10.990Z',
                       'quote': 'Not exactly. I need the history to be easy to find and consistent enough to '
                                'spot patterns, but I’m not looking to sort every little thing into a dozen '
                                'boxes while a press is down.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-20'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-20'],
          'stakeholders': ['Teo'],
          'agents': ['system']},
 'G-20': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'The correct spare part and its location can be retrieved',
          'sources': [{'timestamp': '2026-10-28T12:58:12.153Z',
                       'quote': 'Let me think… when I’m at a press, I need the recent fault history and live '
                                'readings together, not buried in separate screens. If a sensor saw the '
                                'temperature drifting before the alarm, show that beside the repair notes, '
                                'and let me pull up the right spare part and its location quickly.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-21'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-21'],
          'stakeholders': ['Teo'],
          'agents': ['system']},
 'G-21': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'The intended press can be found by searching its floor nickname',
          'sources': [{'timestamp': '2026-10-28T13:02:45.658Z',
                       'quote': 'One thing—let me find the press by its floor nickname, not just some asset '
                                'number nobody uses. Other than that, keep it quick and useful at the '
                                'machine; if it turns into office paperwork, the night shift won’t keep up '
                                'with it.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-22'},
                      {'timestamp': '2026-10-28T13:03:14.265Z',
                       'quote': 'Right, the nickname should be how we find it on the floor, with the asset '
                                'number underneath for the official record. If I search “Old Blue” and get '
                                'three machines, that’s no good, so the floor area or line should show too.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-23'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-22', 'SOURCE-G-23'],
          'stakeholders': ['Teo'],
          'agents': ['system']},
 'G-22': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Search results show asset number beneath nickname and floor area or line',
          'sources': [{'timestamp': '2026-10-28T13:03:14.265Z',
                       'quote': 'Right, the nickname should be how we find it on the floor, with the asset '
                                'number underneath for the official record. If I search “Old Blue” and get '
                                'three machines, that’s no good, so the floor area or line should show too.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-24'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-24'],
          'stakeholders': ['Teo'],
          'agents': ['system']},
 'G-23': {'type': 'SoftGoal',
          'category': 'non-functional',
          'text': 'Maintenance history is consistent enough for recurring-fault patterns to be recognized',
          'sources': [{'timestamp': '2026-10-28T12:50:10.990Z',
                       'quote': 'Not exactly. I need the history to be easy to find and consistent enough to '
                                'spot patterns, but I’m not looking to sort every little thing into a dozen '
                                'boxes while a press is down.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-25'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-25'],
          'stakeholders': ['Teo'],
          'agents': []},
 'G-24': {'type': 'AvoidGoal',
          'category': 'functional',
          'text': 'Already completed diagnostics are repeated unnecessarily',
          'sources': [{'timestamp': '2026-10-28T12:52:57.806Z',
                       'quote': 'The main bottleneck is the asynchronous data entry and poor shift-to-shift '
                                'handoff. I’m troubleshooting from fault codes, machine state, and component '
                                'test results, but the CMMS history is often stale or inconsistently coded, '
                                'so I lose time duplicating diagnostics and validating whether the fault is '
                                'intermittent or recurring.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-26'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-26'],
          'stakeholders': ['Teo'],
          'agents': []},
 'G-25': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Ownership and intended use of personal troubleshooting knowledge are understood before '
                  'sharing',
          'sources': [{'timestamp': '2026-10-28T12:51:49.043Z',
                       'quote': 'Not usually. Those are things I keep in my notebook, and I’m careful about '
                                'putting all my hard-earned tricks into the company system without knowing '
                                'who owns them or how they’ll be used.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-27'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-27'],
          'stakeholders': ['Teo'],
          'agents': []},
 'G-26': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Machine-specific troubleshooting knowledge is recorded if the technician chooses to share '
                  'after understanding ownership and use',
          'sources': [{'timestamp': '2026-10-28T12:52:07.052Z',
                       'quote': 'Not exactly. It’s more that those tricks are part of my experience, and I '
                                'want to know how they’ll be used before I put them in the company system.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-28'}],
          'inferred': True,
          'interpretation': 'Conditional sharing and explanatory workflow are interpretations; the '
                            'stakeholder requests understanding, but specifies no policy owner, approval '
                            'mechanism, or interface.',
          'original_goal_ids': ['SOURCE-G-28'],
          'stakeholders': ['Teo'],
          'agents': ['technician']},
 'G-27': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Fault codes, part numbers, and corrective actions remain distinguishable in records',
          'sources': [{'timestamp': '2026-10-28T12:53:38.355Z',
                       'quote': 'Yeah, the entries aren’t always consistent—one tech logs a high-temp '
                                'deviation, another just writes “heater issue.” Part numbers, fault codes, '
                                'and corrective actions get mixed together, so the next shift has to '
                                'reconstruct the diagnostic trail.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-29'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-29'],
          'stakeholders': ['Teo'],
          'agents': ['system']},
 'G-28': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Initial supporting repair evidence is captured without typing a paragraph',
          'sources': [{'timestamp': '2026-10-28T12:57:29.710Z',
                       'quote': 'Right. With gloves on, I’m not typing a paragraph while Press 7 is waiting. '
                                'Let me snap a photo of the failed part or leave a short voice note, then I '
                                'can clean it up later if needed.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-30'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-30'],
          'stakeholders': ['Teo'],
          'agents': []},
 'G-29': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Repaired press stability is checked through a production run',
          'sources': [{'timestamp': '2026-10-28T12:46:29.759Z',
                       'quote': 'I check the fault code and the machine history, then work through the '
                                'electrical, hydraulic, and temperature circuits until I find the cause. On '
                                'the presses I’m watching clamp pressure, injection pressure, heater zones, '
                                'and cycle time—not just clearing the alarm. After the repair, I run parts '
                                'and monitor the press to make sure it holds steady.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-31'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-31'],
          'stakeholders': ['Teo'],
          'agents': ['technician']},
 'G-30': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Electrical, hydraulic, and temperature circuits are investigated to identify the fault '
                  'cause',
          'sources': [{'timestamp': '2026-10-28T12:46:29.759Z',
                       'quote': 'I check the fault code and the machine history, then work through the '
                                'electrical, hydraulic, and temperature circuits until I find the cause. On '
                                'the presses I’m watching clamp pressure, injection pressure, heater zones, '
                                'and cycle time—not just clearing the alarm. After the repair, I run parts '
                                'and monitor the press to make sure it holds steady.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-32'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-32'],
          'stakeholders': ['Teo'],
          'agents': ['technician']},
 'G-31': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Scheduled night-shift maintenance is performed',
          'sources': [{'timestamp': '2026-10-28T12:45:51.599Z',
                       'quote': 'I keep the molding presses running—troubleshoot faults, make repairs, and '
                                'handle the scheduled maintenance on night shift.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-33'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-33'],
          'stakeholders': ['Teo'],
          'agents': ['technician']},
 'G-32': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'The faulty component is repaired or replaced after appropriate isolation',
          'sources': [{'timestamp': '2026-10-28T12:47:31.502Z',
                       'quote': 'Press 7 threw a high-temperature deviation on zone three, then started '
                                'short-cycling. I checked the thermocouple signal, SSR output, and '
                                'heater-band resistance; the day shift had already swapped the thermocouple, '
                                'but didn’t note that in the log, so I nearly repeated it. The band was '
                                'open, so I isolated the press, replaced it, cleared the alarm, and ran '
                                'production until the zone held temperature and the cycle time stayed '
                                'steady.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-34'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-34'],
          'stakeholders': ['Teo'],
          'agents': ['technician']},
 'G-33': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'A technician receives an explanation of ownership and intended use before sharing '
                  'personal troubleshooting knowledge',
          'sources': [{'timestamp': '2026-10-28T12:52:07.052Z',
                       'quote': 'Not exactly. It’s more that those tricks are part of my experience, and I '
                                'want to know how they’ll be used before I put them in the company system.',
                       'stakeholder': 'Teo',
                       'original_goal_id': 'SOURCE-G-35'}],
          'inferred': True,
          'interpretation': 'Conditional sharing and explanatory workflow are interpretations; the '
                            'stakeholder requests understanding, but specifies no policy owner, approval '
                            'mechanism, or interface.',
          'original_goal_ids': ['SOURCE-G-35'],
          'stakeholders': ['Teo'],
          'agents': ['organization']},
 'G-34': {'type': 'MaintainGoal',
          'category': 'functional',
          'text': 'Plant operates safely and delivers quality parts on schedule across three shifts',
          'sources': [{'timestamp': '2026-10-28T16:57:20.830Z',
                       'quote': 'I’m responsible for keeping the plant running safely and meeting production '
                                'commitments across all three shifts. That includes monitoring equipment '
                                'performance, coordinating maintenance priorities, and making sure we '
                                'deliver quality parts on schedule.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-36'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-36'],
          'stakeholders': ['Angela'],
          'agents': []},
 'G-35': {'type': 'SoftGoal',
          'category': 'non-functional',
          'text': 'Downtime is measurably reduced without unnecessary production disruption',
          'sources': [{'timestamp': '2026-10-28T17:23:57.280Z',
                       'quote': 'No, I think that covers the main operational needs. Thanks, Carl—please '
                                'make sure the final system is judged on measurable downtime reduction, '
                                'complete maintenance records, and whether it helps us plan work without '
                                'disrupting production. Goodbye, and good luck with the design.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-37'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-37'],
          'stakeholders': ['Angela'],
          'agents': []},
 'G-36': {'type': 'SoftGoal',
          'category': 'non-functional',
          'text': 'Maintenance records are complete, consistent, and trustworthy across shifts',
          'sources': [{'timestamp': '2026-10-28T16:59:49.814Z',
                       'quote': 'That’s right. The numbers only help if technicians enter them consistently '
                                'and I can trust the record across all three shifts.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-38'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-38'],
          'stakeholders': ['Angela'],
          'agents': []},
 'G-37': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Downtime and production impact are available for maintenance prioritization',
          'sources': [{'timestamp': '2026-10-28T17:13:27.465Z',
                       'quote': 'The most informative thing would be a reliable view of downtime in minutes '
                                'by machine and reason code, with repeat failures highlighted. I also need '
                                'to see the current machine status and production-order impact, so I can '
                                'prioritize the critical losses rather than just the most recent complaint.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-39'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-39'],
          'stakeholders': ['Angela'],
          'agents': []},
 'G-38': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Equipment criticality, downtime, failure mode, order impact, and technician availability '
                  'inform priority',
          'sources': [{'timestamp': '2026-10-28T16:57:56.405Z',
                       'quote': 'I prioritize work by equipment criticality, current downtime, failure mode, '
                                'and impact on the production schedule. A failed bottleneck machine gets '
                                'immediate attention, while preventive maintenance and lower-risk corrective '
                                'work are sequenced around production orders and technician availability.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-40'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-40'],
          'stakeholders': ['Angela'],
          'agents': ['manager']},
 'G-39': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Downtime duration is captured in minutes for each machine event',
          'sources': [{'timestamp': '2026-10-28T16:59:04.516Z',
                       'quote': 'Well, last month a molding press on our bottleneck line failed during a '
                                'large automotive order, and we lost 86 minutes before the first good part '
                                'was produced. I’d want the technician to log the stop and repair on the '
                                'tablet while the system captures downtime in minutes, requires a reason '
                                'code, and shows the impact against the production order so I can prioritize '
                                'the next response based on facts rather than radio calls.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-42'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-42'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-40': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'A downtime reason code is required for the event record',
          'sources': [{'timestamp': '2026-10-28T16:59:04.516Z',
                       'quote': 'Well, last month a molding press on our bottleneck line failed during a '
                                'large automotive order, and we lost 86 minutes before the first good part '
                                'was produced. I’d want the technician to log the stop and repair on the '
                                'tablet while the system captures downtime in minutes, requires a reason '
                                'code, and shows the impact against the production order so I can prioritize '
                                'the next response based on facts rather than radio calls.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-43'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-43'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-41': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Production-order impact is shown alongside the downtime event',
          'sources': [{'timestamp': '2026-10-28T16:59:04.516Z',
                       'quote': 'Well, last month a molding press on our bottleneck line failed during a '
                                'large automotive order, and we lost 86 minutes before the first good part '
                                'was produced. I’d want the technician to log the stop and repair on the '
                                'tablet while the system captures downtime in minutes, requires a reason '
                                'code, and shows the impact against the production order so I can prioritize '
                                'the next response based on facts rather than radio calls.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-44'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-44'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-42': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Downtime minutes are displayed by machine and reason code with repeat failures '
                  'highlighted',
          'sources': [{'timestamp': '2026-10-28T17:13:27.465Z',
                       'quote': 'The most informative thing would be a reliable view of downtime in minutes '
                                'by machine and reason code, with repeat failures highlighted. I also need '
                                'to see the current machine status and production-order impact, so I can '
                                'prioritize the critical losses rather than just the most recent complaint.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-45'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-45'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-43': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Current machine status and approved keeping-down status are visible before prioritization',
          'sources': [{'timestamp': '2026-10-28T17:23:18.989Z',
                       'quote': 'Well, first I need to see machines that are currently down or losing the '
                                'most minutes, especially critical machines tied to an active production '
                                'order. Then I’d prioritize repeat failures and overdue preventive '
                                'maintenance, but only after the record shows the reason code, current '
                                'status, and whether a supervisor has approved keeping the machine down.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-46'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-46'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-44': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Open repairs, temporary fixes, awaited parts, and watched machines are communicated at '
                  'handover',
          'sources': [{'timestamp': '2026-10-28T17:00:33.563Z',
                       'quote': 'We use a shift handover meeting and a maintenance log, but the quality '
                                'varies by shift. The outgoing technician explains open repairs, temporary '
                                'fixes, parts waiting, and machines being watched; the incoming technician '
                                'reviews that and calls the supervisor if anything is unclear. The written '
                                'record is supposed to be the source of truth, but missing reason codes and '
                                'incomplete updates still create problems.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-47'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-47'],
          'stakeholders': ['Angela'],
          'agents': ['technician']},
 'G-45': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Fault, diagnosis, work, parts and quantities, tests, machine status, and downtime reason '
                  'are recorded',
          'sources': [{'timestamp': '2026-10-28T17:10:16.529Z',
                       'quote': 'The technician fills out the fault description, machine status, diagnosis, '
                                'work performed, parts and quantities used, measurements or test results, '
                                'and the reason code for the downtime. The supervisor records the priority, '
                                'escalation decision, staffing or production impact, whether a production '
                                'stoppage is approved, and who authorized the machine’s release back into '
                                'production.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-48'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-48'],
          'stakeholders': ['Angela'],
          'agents': ['technician']},
 'G-46': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Escalations reach an authorized supervisor with the necessary technical facts',
          'sources': [{'timestamp': '2026-10-28T17:04:09.383Z',
                       'quote': 'The biggest bottleneck is the gap between the technician finding the '
                                'problem and a supervisor deciding what happens next. I’d solve that with a '
                                'tablet workflow that captures the fault, work already attempted, current '
                                'machine status, and escalation reason, then routes it to the supervisor for '
                                'an explicit production-stop decision. That keeps the repair record complete '
                                'without allowing a technician’s entry to stop production by itself.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-49'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-49'],
          'stakeholders': ['Angela'],
          'agents': []},
 'G-47': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Work is stopped and the machine made safe if there is uncertainty about proceeding',
          'sources': [{'timestamp': '2026-10-28T17:01:34.874Z',
                       'quote': 'They stop the work, make the machine safe, and contact the shift supervisor '
                                'or maintenance lead. The supervisor checks the machine history, manuals, '
                                'and available expertise, then either assigns the next step or escalates it '
                                'to engineering or the equipment supplier.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-50'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-50'],
          'stakeholders': ['Angela'],
          'agents': ['technician']},
 'G-48': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'The issue and attempted work are escalated if there is a safety concern, repeated '
                  'failure, or no clear repair path',
          'sources': [{'timestamp': '2026-10-28T17:02:22.815Z',
                       'quote': 'Not exactly—the supervisor doesn’t necessarily know more technically, but '
                                'she has the authority to stop production, reassign people, or call '
                                'engineering and the supplier. The technician records the issue, explains '
                                'what was tried, and escalates when there’s a safety concern, repeated '
                                'failure, or no clear repair path.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-51'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-51'],
          'stakeholders': ['Angela'],
          'agents': ['technician']},
 'G-49': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Fault, attempted work, machine status, and escalation reason are routed to the supervisor',
          'sources': [{'timestamp': '2026-10-28T17:04:09.383Z',
                       'quote': 'The biggest bottleneck is the gap between the technician finding the '
                                'problem and a supervisor deciding what happens next. I’d solve that with a '
                                'tablet workflow that captures the fault, work already attempted, current '
                                'machine status, and escalation reason, then routes it to the supervisor for '
                                'an explicit production-stop decision. That keeps the repair record complete '
                                'without allowing a technician’s entry to stop production by itself.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-52'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-52'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-50': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'History, manuals, and expertise are reviewed before next steps or further escalation are '
                  'assigned',
          'sources': [{'timestamp': '2026-10-28T17:01:34.874Z',
                       'quote': 'They stop the work, make the machine safe, and contact the shift supervisor '
                                'or maintenance lead. The supervisor checks the machine history, manuals, '
                                'and available expertise, then either assigns the next step or escalates it '
                                'to engineering or the equipment supplier.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-53'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-53'],
          'stakeholders': ['Angela'],
          'agents': ['supervisor']},
 'G-51': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Criticality, safety, repeat failures, parts, and production impact inform the recorded '
                  'escalation decision',
          'sources': [{'timestamp': '2026-10-28T17:04:52.240Z',
                       'quote': 'We have standard escalation criteria, but not a rigid decision tree. The '
                                'supervisor considers machine criticality, safety status, repeat-failure '
                                'history, spare-parts availability, and production impact, then records '
                                'whether the repair continues, engineering is called, or an approved '
                                'production stoppage is required.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-54'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-54'],
          'stakeholders': ['Angela'],
          'agents': ['supervisor']},
 'G-52': {'type': 'AvoidGoal',
          'category': 'functional',
          'text': 'A technician repair entry alone authorizes a production stoppage',
          'sources': [{'timestamp': '2026-10-28T17:04:09.383Z',
                       'quote': 'The biggest bottleneck is the gap between the technician finding the '
                                'problem and a supervisor deciding what happens next. I’d solve that with a '
                                'tablet workflow that captures the fault, work already attempted, current '
                                'machine status, and escalation reason, then routes it to the supervisor for '
                                'an explicit production-stop decision. That keeps the repair record complete '
                                'without allowing a technician’s entry to stop production by itself.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-55'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-55'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-53': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Priority, escalation, staffing impact, production impact, and stoppage approval are '
                  'recorded separately from technical facts',
          'sources': [{'timestamp': '2026-10-28T17:10:16.529Z',
                       'quote': 'The technician fills out the fault description, machine status, diagnosis, '
                                'work performed, parts and quantities used, measurements or test results, '
                                'and the reason code for the downtime. The supervisor records the priority, '
                                'escalation decision, staffing or production impact, whether a production '
                                'stoppage is approved, and who authorized the machine’s release back into '
                                'production.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-56'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-56'],
          'stakeholders': ['Angela'],
          'agents': ['supervisor']},
 'G-54': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Plant-wide, major-commitment, critical-machine, and cross-shift exceptions receive '
                  'plant-manager review',
          'sources': [{'timestamp': '2026-10-28T17:15:23.414Z',
                       'quote': 'I approve exceptions that affect plant-wide priorities, major production '
                                'commitments, or a critical machine—especially when a supervisor needs to '
                                'keep it down longer than planned. Routine repair escalation and the initial '
                                'production-stop decision belong to the shift supervisor; I review the '
                                'situation when it impacts the schedule, customer delivery, or requires '
                                'resources across shifts.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-57'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-57'],
          'stakeholders': ['Angela'],
          'agents': ['manager']},
 'G-55': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Exceptions and critical losses are filtered by impact and urgency',
          'sources': [{'timestamp': '2026-10-28T17:15:49.783Z',
                       'quote': 'It is a lot of work, which is why I need the information filtered by impact '
                                'and urgency. I can’t personally chase every repair across three shifts; the '
                                'system should make exceptions and critical losses visible quickly.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-58'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-58'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-56': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Repair events and release decisions are traceable for customer audits',
          'sources': [{'timestamp': '2026-10-28T17:07:57.243Z',
                       'quote': 'Not exactly. The incomplete record didn’t cause the repair to take longer; '
                                'it made the repair difficult to verify afterward and left us exposed during '
                                'an automotive customer audit. For safety-related parts, I need the '
                                'technician, parts replaced, repair actions, and release decision traceable '
                                'to that specific machine event.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-59'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-59'],
          'stakeholders': ['Angela'],
          'agents': []},
 'G-57': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Technician identity, parts replaced, repair actions, and release decision are linked to '
                  'the specific machine event',
          'sources': [{'timestamp': '2026-10-28T17:07:57.243Z',
                       'quote': 'Not exactly. The incomplete record didn’t cause the repair to take longer; '
                                'it made the repair difficult to verify afterward and left us exposed during '
                                'an automotive customer audit. For safety-related parts, I need the '
                                'technician, parts replaced, repair actions, and release decision traceable '
                                'to that specific machine event.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-60'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-60'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-58': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Release approver and approval time are recorded as mandatory traceability for '
                  'safety-related parts',
          'sources': [{'timestamp': '2026-10-28T17:09:35.943Z',
                       'quote': 'I mentioned the machine release decision—the record must show who approved '
                                'putting it back into production and when. For safety-related parts, that '
                                'approval is part of the repair traceability, not an optional note.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-61'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-61'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-59': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Parts use and shortages are recorded for repair and production decisions',
          'sources': [{'timestamp': '2026-10-28T17:05:35.788Z',
                       'quote': 'We keep crib stock for common wear items—seals, sensors, belts, and '
                                'contactors—but critical assemblies and specialized components may require a '
                                'purchase order. The technician records the part number and quantity issued '
                                'against the work order; if a part is unavailable, the supervisor marks the '
                                'machine as awaiting parts and escalates based on lead time and production '
                                'impact.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-62'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-62'],
          'stakeholders': ['Angela'],
          'agents': []},
 'G-60': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Issued part number and quantity are recorded against the work order',
          'sources': [{'timestamp': '2026-10-28T17:05:35.788Z',
                       'quote': 'We keep crib stock for common wear items—seals, sensors, belts, and '
                                'contactors—but critical assemblies and specialized components may require a '
                                'purchase order. The technician records the part number and quantity issued '
                                'against the work order; if a part is unavailable, the supervisor marks the '
                                'machine as awaiting parts and escalates based on lead time and production '
                                'impact.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-63'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-63'],
          'stakeholders': ['Angela'],
          'agents': ['technician']},
 'G-61': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'The machine is marked awaiting parts and escalated by lead time and order impact if a '
                  'part is unavailable',
          'sources': [{'timestamp': '2026-10-28T17:05:35.788Z',
                       'quote': 'We keep crib stock for common wear items—seals, sensors, belts, and '
                                'contactors—but critical assemblies and specialized components may require a '
                                'purchase order. The technician records the part number and quantity issued '
                                'against the work order; if a part is unavailable, the supervisor marks the '
                                'machine as awaiting parts and escalates based on lead time and production '
                                'impact.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-64'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-64'],
          'stakeholders': ['Angela'],
          'agents': ['supervisor']},
 'G-62': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Stock accuracy, stockouts, lead time, and downtime waiting for parts are available for '
                  'review',
          'sources': [{'timestamp': '2026-10-28T17:06:14.414Z',
                       'quote': 'If you mean spare-part availability, we measure stock accuracy, stockouts, '
                                'supplier lead time, and minutes of downtime waiting for a part. I also look '
                                'at repair cycle time, repeat failures after repair, preventive-maintenance '
                                'completion, and which machines consume the most parts. The critical number '
                                'is whether a part shortage extended downtime or forced us to change the '
                                'production plan.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-65'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-65'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-63': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Repair cycle time, repeat failures, preventive completion, and parts consumption by '
                  'machine are available for review',
          'sources': [{'timestamp': '2026-10-28T17:06:14.414Z',
                       'quote': 'If you mean spare-part availability, we measure stock accuracy, stockouts, '
                                'supplier lead time, and minutes of downtime waiting for a part. I also look '
                                'at repair cycle time, repeat failures after repair, preventive-maintenance '
                                'completion, and which machines consume the most parts. The critical number '
                                'is whether a part shortage extended downtime or forced us to change the '
                                'production plan.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-66'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-66'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-64': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Part-shortage effects on downtime and production-plan changes are visible',
          'sources': [{'timestamp': '2026-10-28T17:06:14.414Z',
                       'quote': 'If you mean spare-part availability, we measure stock accuracy, stockouts, '
                                'supplier lead time, and minutes of downtime waiting for a part. I also look '
                                'at repair cycle time, repeat failures after repair, preventive-maintenance '
                                'completion, and which machines consume the most parts. The critical number '
                                'is whether a part shortage extended downtime or forced us to change the '
                                'production plan.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-67'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-67'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-65': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Preventive maintenance is coordinated with production orders',
          'sources': [{'timestamp': '2026-10-28T17:17:27.157Z',
                       'quote': 'One additional point: preventive maintenance needs to be visible against '
                                'the production schedule, so we can plan it around orders instead of '
                                'discovering conflicts at the last minute. I also want the system to show '
                                'overdue maintenance and upcoming work by machine criticality, not just '
                                'record completed repairs.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-68'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-68'],
          'stakeholders': ['Angela'],
          'agents': []},
 'G-66': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Preventive work becomes due according to required hours, cycles, or calendar-day '
                  'intervals',
          'sources': [{'timestamp': '2026-10-28T17:18:13.322Z',
                       'quote': 'Not exactly a uniform calendar schedule. Preventive maintenance should be '
                                'triggered by the machine’s required interval—hours, cycles, or calendar '
                                'days—then placed in an available production window around current orders, '
                                'with overdue work clearly escalated by machine criticality. Maintenance '
                                'shouldn’t block the production schedule automatically; any conflict needs '
                                'an explicit supervisor or plant-level approval.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-69'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-69'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-67': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Overdue and upcoming work are displayed and overdue work escalated by machine criticality',
          'sources': [{'timestamp': '2026-10-28T17:17:27.157Z',
                       'quote': 'One additional point: preventive maintenance needs to be visible against '
                                'the production schedule, so we can plan it around orders instead of '
                                'discovering conflicts at the last minute. I also want the system to show '
                                'overdue maintenance and upcoming work by machine criticality, not just '
                                'record completed repairs.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-70'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-70'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-68': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'A supervisor coordinates a maintenance window against orders and actual team availability',
          'sources': [{'timestamp': '2026-10-28T17:18:53.064Z',
                       'quote': 'Yes, we do some preventive maintenance during night shifts and planned '
                                'production gaps, but night availability isn’t guaranteed. The maintenance '
                                'team checks the production schedule, then the supervisor coordinates a '
                                'window; if the work conflicts with an order, it must be escalated for '
                                'approval rather than blocking production automatically.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-71'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-71'],
          'stakeholders': ['Angela'],
          'agents': ['supervisor']},
 'G-69': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Another available production window is selected if planned maintenance conflicts with an '
                  'order',
          'sources': [{'timestamp': '2026-10-28T17:19:21.719Z',
                       'quote': 'Yes, we see conflicts fairly often, especially when an urgent order fills '
                                'the planned production window or a machine runs longer than expected. The '
                                'supervisor checks the order impact and machine criticality, then either '
                                'finds another window, coordinates night-shift work, or escalates the '
                                'conflict for approval.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-72'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-72'],
          'stakeholders': ['Angela'],
          'agents': ['supervisor']},
 'G-70': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Night-shift maintenance is coordinated if planned maintenance conflicts with an order and '
                  'night capacity is available',
          'sources': [{'timestamp': '2026-10-28T17:19:21.719Z',
                       'quote': 'Yes, we see conflicts fairly often, especially when an urgent order fills '
                                'the planned production window or a machine runs longer than expected. The '
                                'supervisor checks the order impact and machine criticality, then either '
                                'finds another window, coordinates night-shift work, or escalates the '
                                'conflict for approval.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-73'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-73'],
          'stakeholders': ['Angela'],
          'agents': ['supervisor']},
 'G-71': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'A scheduling conflict is escalated for explicit supervisor or plant-level approval if '
                  'maintenance conflicts with production',
          'sources': [{'timestamp': '2026-10-28T17:18:13.322Z',
                       'quote': 'Not exactly a uniform calendar schedule. Preventive maintenance should be '
                                'triggered by the machine’s required interval—hours, cycles, or calendar '
                                'days—then placed in an available production window around current orders, '
                                'with overdue work clearly escalated by machine criticality. Maintenance '
                                'shouldn’t block the production schedule automatically; any conflict needs '
                                'an explicit supervisor or plant-level approval.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-74'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-74'],
          'stakeholders': ['Angela'],
          'agents': ['supervisor']},
 'G-72': {'type': 'AvoidGoal',
          'category': 'functional',
          'text': 'Maintenance planning automatically blocks the production schedule without explicit '
                  'approval',
          'sources': [{'timestamp': '2026-10-28T17:18:13.322Z',
                       'quote': 'Not exactly a uniform calendar schedule. Preventive maintenance should be '
                                'triggered by the machine’s required interval—hours, cycles, or calendar '
                                'days—then placed in an available production window around current orders, '
                                'with overdue work clearly escalated by machine criticality. Maintenance '
                                'shouldn’t block the production schedule automatically; any conflict needs '
                                'an explicit supervisor or plant-level approval.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-75'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-75'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-73': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Schedule-conflict impact and approval status are clearly displayed',
          'sources': [{'timestamp': '2026-10-28T17:19:53.497Z',
                       'quote': 'Right. The key is that maintenance planning has to work with production, '
                                'not against it. If a conflict appears, I need to see the impact and the '
                                'approval status clearly so we make a deliberate decision rather than '
                                'discovering the problem after the order is late.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-76'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-76'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-74': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Existing machine data supports verification without replacing technician diagnosis '
                  'records',
          'sources': [{'timestamp': '2026-10-28T17:20:30.621Z',
                       'quote': 'Well, the system should use the machine data we already have alongside '
                                'technician entries, so reported downtime can be checked against actual '
                                'machine states. Beyond that, I think we’ve covered the operational '
                                'priorities; I’ll judge it by whether it reduces downtime and gives me '
                                'records I can trust.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-77'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-77'],
          'stakeholders': ['Angela'],
          'agents': []},
 'G-75': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Available run-stop states, cycle counts, alarms, and sensor readings are used alongside '
                  'technician entries',
          'sources': [{'timestamp': '2026-10-28T17:20:57.765Z',
                       'quote': 'We already collect machine run and stop states, cycle counts, alarm events, '
                                'and some temperature or pressure readings from the PLCs and plant '
                                'monitoring system. Coverage and detail vary by machine, so technician '
                                'entries still matter for the actual diagnosis, repair action, and downtime '
                                'reason.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-78'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-78'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-76': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Reported downtime can be checked against available actual machine states',
          'sources': [{'timestamp': '2026-10-28T17:20:30.621Z',
                       'quote': 'Well, the system should use the machine data we already have alongside '
                                'technician entries, so reported downtime can be checked against actual '
                                'machine states. Beyond that, I think we’ve covered the operational '
                                'priorities; I’ll judge it by whether it reduces downtime and gives me '
                                'records I can trust.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-79'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-79'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-77': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Machine-data availability, coverage gaps, and authoritative technician entries are '
                  'identified',
          'sources': [{'timestamp': '2026-10-28T17:22:25.750Z',
                       'quote': 'You’re welcome. The important point is that the system should show where '
                                'machine data is available and where the technician’s entry is the '
                                'authoritative record.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-80'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-80'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-78': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Desktop schedules, reports, and downtime analysis are available',
          'sources': [{'timestamp': '2026-10-28T17:14:45.270Z',
                       'quote': 'Well, I split my time between the office and the production floor. I use a '
                                'desktop for schedules, reports, and downtime analysis, but on the floor I '
                                'need a tablet or phone-sized view to check machine status, open repairs, '
                                'and approvals without going back to my office.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-81'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-81'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-79': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Machine status, open repairs, and approvals are available in a tablet or phone-sized '
                  'floor view',
          'sources': [{'timestamp': '2026-10-28T17:14:45.270Z',
                       'quote': 'Well, I split my time between the office and the production floor. I use a '
                                'desktop for schedules, reports, and downtime analysis, but on the floor I '
                                'need a tablet or phone-sized view to check machine status, open repairs, '
                                'and approvals without going back to my office.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-82'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-82'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-80': {'type': 'SoftGoal',
          'category': 'non-functional',
          'text': 'Critical losses and exceptions become visible quickly enough for timely decisions',
          'sources': [{'timestamp': '2026-10-28T17:15:49.783Z',
                       'quote': 'It is a lot of work, which is why I need the information filtered by impact '
                                'and urgency. I can’t personally chase every repair across three shifts; the '
                                'system should make exceptions and critical losses visible quickly.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-83'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-83'],
          'stakeholders': ['Angela'],
          'agents': []},
 'G-81': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'The response to a maintenance scheduling conflict is coordinated',
          'sources': [{'timestamp': '2026-10-28T17:19:21.719Z',
                       'quote': 'Yes, we see conflicts fairly often, especially when an urgent order fills '
                                'the planned production window or a machine runs longer than expected. The '
                                'supervisor checks the order impact and machine criticality, then either '
                                'finds another window, coordinates night-shift work, or escalates the '
                                'conflict for approval.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-84'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-84'],
          'stakeholders': ['Angela'],
          'agents': []},
 'G-82': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'A technician is prompted to supply a missing reason code before an event is treated as '
                  'complete',
          'sources': [{'timestamp': '2026-10-28T17:10:51.282Z',
                       'quote': 'The biggest gap is the downtime reason code, followed by incomplete updates '
                                'on what was tried and the machine’s current status. Technicians often enter '
                                'a quick description but skip the code, so I can’t reliably separate setup '
                                'issues, parts failures, operator causes, and repeat faults when I review '
                                'downtime across shifts.',
                       'stakeholder': 'Angela',
                       'original_goal_id': 'SOURCE-G-85'}],
          'inferred': True,
          'interpretation': 'Missing-code prompt and completion timing are inferred; Angela requires a code '
                            'but does not specify validation timing.',
          'original_goal_ids': ['SOURCE-G-85'],
          'stakeholders': ['Angela'],
          'agents': ['system']},
 'G-83': {'type': 'AvoidGoal',
          'category': 'non-functional',
          'text': 'Maintenance activities cause injuries or expose people to uncontrolled hazards',
          'sources': [{'timestamp': '2026-10-28T22:04:17.839Z',
                       'quote': 'That’s right. Fast is useful, but not if it encourages somebody to bypass a '
                                'safety stop or work with incomplete information. Zero injuries and complete '
                                'records are the standard.',
                       'stakeholder': 'Rob',
                       'original_goal_id': 'SOURCE-G-86'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-86'],
          'stakeholders': ['Rob'],
          'agents': []},
 'G-84': {'type': 'MaintainGoal',
          'category': 'non-functional',
          'text': 'Safety records remain complete, trustworthy, and verifiable for inspections',
          'sources': [{'timestamp': '2026-10-28T22:03:44.559Z',
                       'quote': 'Well, nothing major beyond this: the system should never let speed or '
                                'convenience override a safety stop. If it helps us prevent injuries and '
                                'produce complete, trustworthy records for inspections, then it’s doing its '
                                'job.',
                       'stakeholder': 'Rob',
                       'original_goal_id': 'SOURCE-G-87'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-87'],
          'stakeholders': ['Rob'],
          'agents': []},
 'G-85': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Task-specific hazards, severity, likelihood, and hierarchy-based controls are assessed '
                  'before maintenance starts',
          'sources': [{'timestamp': '2026-10-28T21:37:51.624Z',
                       'quote': 'Hazard assessments identify task-specific hazards, evaluate risk severity '
                                'and likelihood, and establish controls through the hierarchy of controls. '
                                'For maintenance, that includes energy isolation, machine guarding, chemical '
                                'exposure, confined-space hazards, PPE requirements, and verifying that '
                                'controls are effective before work begins.',
                       'stakeholder': 'Rob',
                       'original_goal_id': 'SOURCE-G-88'},
                      {'timestamp': '2026-10-28T21:37:51.624Z',
                       'quote': 'Hazard assessments identify task-specific hazards, evaluate risk severity '
                                'and likelihood, and establish controls through the hierarchy of controls. '
                                'For maintenance, that includes energy isolation, machine guarding, chemical '
                                'exposure, confined-space hazards, PPE requirements, and verifying that '
                                'controls are effective before work begins.',
                       'stakeholder': 'Rob',
                       'original_goal_id': 'SOURCE-G-89'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-88', 'SOURCE-G-89'],
          'stakeholders': ['Rob'],
          'agents': ['ehs']},
 'G-86': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Job steps, hazards, energy sources, PPE, permits, emergency actions, and responsibilities '
                  'are reviewed before work',
          'sources': [{'timestamp': '2026-10-28T21:49:37.482Z',
                       'quote': 'Pre-job meetings happen before maintenance starts, with the technician, '
                                'supervisor, and anyone else involved reviewing the job steps, hazards, '
                                'energy sources, PPE, permits, and emergency actions. We make sure everyone '
                                'understands the controls and who is responsible before the work begins; if '
                                'the conditions change, we stop and reassess.',
                       'stakeholder': 'Rob',
                       'original_goal_id': 'SOURCE-G-90'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-90'],
          'stakeholders': ['Rob'],
          'agents': ['team']},
 'G-87': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Every hazardous energy source is identified, isolated, locked, tagged, and verified at '
                  'zero energy before equipment is touched',
          'sources': [{'timestamp': '2026-10-28T21:50:13.658Z',
                       'quote': 'Energy sources are anything that can injure someone if they aren’t '
                                'isolated—electrical, hydraulic, pneumatic, mechanical, thermal, chemical, '
                                'or stored energy such as pressure or gravity. Before maintenance, the '
                                'technician identifies every source, isolates it, locks and tags it, and '
                                'verifies zero energy before touching the equipment.',
                       'stakeholder': 'Rob',
                       'original_goal_id': 'SOURCE-G-91'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-91'],
          'stakeholders': ['Rob'],
          'agents': ['technician']},
 'G-88': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Required PPE is suitable and in good condition and task training and fit testing are '
                  'verified where applicable',
          'sources': [{'timestamp': '2026-10-28T21:38:39.592Z',
                       'quote': 'PPE procedures specify what protection is required for the task—such as eye '
                                'protection, gloves, hearing protection, respirators, or arc-rated '
                                'clothing—and workers have to be trained and fit-tested where applicable. We '
                                'also check that the equipment is in good condition and that supervisors '
                                'verify compliance before work starts. That ties into permits, machine '
                                'guarding, energy isolation, and documenting any corrective action when '
                                'controls aren’t followed.',
                       'stakeholder': 'Rob',
                       'original_goal_id': 'SOURCE-G-92'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-92'],
          'stakeholders': ['Rob'],
          'agents': ['supervisor']},
 'G-89': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Work stops and hazards are reassessed if conditions change',
          'sources': [{'timestamp': '2026-10-28T21:49:37.482Z',
                       'quote': 'Pre-job meetings happen before maintenance starts, with the technician, '
                                'supervisor, and anyone else involved reviewing the job steps, hazards, '
                                'energy sources, PPE, permits, and emergency actions. We make sure everyone '
                                'understands the controls and who is responsible before the work begins; if '
                                'the conditions change, we stop and reassess.',
                       'stakeholder': 'Rob',
                       'original_goal_id': 'SOURCE-G-93'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-93'],
          'stakeholders': ['Rob'],
          'agents': ['team']},
 'G-90': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Unsafe work stops immediately until controls are corrected and verified',
          'sources': [{'timestamp': '2026-10-28T21:47:04.497Z',
                       'quote': 'First I stop the work and make sure the area and people are safe, then I '
                                'notify the supervisor and verify the control—especially lockout/tagout, '
                                'guarding, and PPE—is corrected before anything resumes. I document what '
                                'happened, investigate whether it was an incident or near miss, assign '
                                'corrective actions, and track them to closure; retraining is required where '
                                'competency or procedure was lacking.',
                       'stakeholder': 'Rob',
                       'original_goal_id': 'SOURCE-G-94'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-94'],
          'stakeholders': ['Rob'],
          'agents': []},
 'G-91': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Work is stopped and people and area made safe if LOTO, guarding, PPE, or energy '
                  'verification are inadequate',
          'sources': [{'timestamp': '2026-10-28T21:41:04.480Z',
                       'quote': 'Missing lockout/tagout, disabled guards, wrong PPE, or a worker entering '
                                'the area before energy is verified. Any one of those means the job stops '
                                'until it’s corrected.',
                       'stakeholder': 'Rob',
                       'original_goal_id': 'SOURCE-G-95'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-95'],
          'stakeholders': ['Rob'],
          'agents': ['team']},
 'G-92': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'The supervisor and EHS are notified before work resumes after a safety violation',
          'sources': [{'timestamp': '2026-10-28T21:42:34.960Z',
                       'quote': 'We stop the job immediately, make the area safe, and notify the supervisor '
                                'and me before work can resume. We document the violation, correct the '
                                'isolation or other control, and require the worker to be retrained; '
                                'repeated or deliberate violations can lead to discipline. Any resulting '
                                'incident or near miss gets investigated, corrective actions are assigned '
                                'and tracked, and the records are retained for inspections. We also review '
                                'the permit, verify PPE and guarding, and check that the next shift '
                                'understands the equipment’s condition.',
                       'stakeholder': 'Rob',
                       'original_goal_id': 'SOURCE-G-96'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-96'],
          'stakeholders': ['Rob'],
          'agents': ['team']},
 'G-93': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Corrected controls are verified before work resumes',
          'sources': [{'timestamp': '2026-10-28T21:47:04.497Z',
                       'quote': 'First I stop the work and make sure the area and people are safe, then I '
                                'notify the supervisor and verify the control—especially lockout/tagout, '
                                'guarding, and PPE—is corrected before anything resumes. I document what '
                                'happened, investigate whether it was an incident or near miss, assign '
                                'corrective actions, and track them to closure; retraining is required where '
                                'competency or procedure was lacking.',
                       'stakeholder': 'Rob',
                       'original_goal_id': 'SOURCE-G-97'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-97'],
          'stakeholders': ['Rob'],
          'agents': ['ehs']},
 'G-94': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Violations are documented and required retraining is assigned',
          'sources': [{'timestamp': '2026-10-28T21:42:34.960Z',
                       'quote': 'We stop the job immediately, make the area safe, and notify the supervisor '
                                'and me before work can resume. We document the violation, correct the '
                                'isolation or other control, and require the worker to be retrained; '
                                'repeated or deliberate violations can lead to discipline. Any resulting '
                                'incident or near miss gets investigated, corrective actions are assigned '
                                'and tracked, and the records are retained for inspections. We also review '
                                'the permit, verify PPE and guarding, and check that the next shift '
                                'understands the equipment’s condition.',
                       'stakeholder': 'Rob',
                       'original_goal_id': 'SOURCE-G-98'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-98'],
          'stakeholders': ['Rob'],
          'agents': ['ehs']},
 'G-95': {'type': 'AvoidGoal',
          'category': 'functional',
          'text': 'Speed or convenience bypasses a safety stop',
          'sources': [{'timestamp': '2026-10-28T22:03:44.559Z',
                       'quote': 'Well, nothing major beyond this: the system should never let speed or '
                                'convenience override a safety stop. If it helps us prevent injuries and '
                                'produce complete, trustworthy records for inspections, then it’s doing its '
                                'job.',
                       'stakeholder': 'Rob',
                       'original_goal_id': 'SOURCE-G-99'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-99'],
          'stakeholders': ['Rob'],
          'agents': ['system']},
 'G-96': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Complete isolation and safety records govern handoff and job closeout',
          'sources': [{'timestamp': '2026-10-28T21:59:40.547Z',
                       'quote': 'Mostly right. I want the records available on the floor and usable with '
                                'poor connectivity, but tablets must not distract anyone operating moving '
                                'machinery. The system also needs to prevent incomplete LOTO records from '
                                'being handed off or closed, including who applied the lock, when, and who '
                                'released it.',
                       'stakeholder': 'Rob',
                       'original_goal_id': 'SOURCE-G-100'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-100'],
          'stakeholders': ['Rob'],
          'agents': []},
 'G-97': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Equipment, job, hazards, controls, PPE, permits, and linked safety events are recorded',
          'sources': [{'timestamp': '2026-10-28T21:57:23.161Z',
                       'quote': 'Critical safety information means the equipment and job, identified '
                                'hazards, required controls, PPE, permits, and lockout/tagout details. It '
                                'also includes zero-energy verification, who applied and released the locks, '
                                'supervisor approval, and any incident, near miss, or corrective action '
                                'linked to the work.',
                       'stakeholder': 'Rob',
                       'original_goal_id': 'SOURCE-G-101'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-101'],
          'stakeholders': ['Rob'],
          'agents': ['technician']},
 'G-98': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'Energy sources, isolation steps, each lock and tag applier and application time, '
                  'verifier, zero-energy verification, and releaser are recorded',
          'sources': [{'timestamp': '2026-10-28T21:53:33.114Z',
                       'quote': 'The record needs the equipment and job identified, every energy source '
                                'listed, the isolation steps completed, and zero-energy verification '
                                'recorded. It must show who applied each lock and tag, when it was applied, '
                                'who verified the isolation, and who released it when the work was complete. '
                                'A supervisor also needs to review it before the job is closed, and '
                                'incomplete fields must prevent closeout rather than being left for the next '
                                'shift.',
                       'stakeholder': 'Rob',
                       'original_goal_id': 'SOURCE-G-102'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-102'],
          'stakeholders': ['Rob'],
          'agents': ['technician']},
 'G-99': {'type': 'AchieveGoal',
          'category': 'functional',
          'text': 'LOTO details are linked to the maintenance job and permit rather than only an incident '
                  'report',
          'sources': [{'timestamp': '2026-10-28T21:50:49.475Z',
                       'quote': 'Not usually in the incident report. The lockout/tagout details belong with '
                                'the maintenance job and permit record, including the energy sources, who '
                                'applied each lock, when it was applied, verification of zero energy, and '
                                'who released it. If something goes wrong or there’s a near miss, we link '
                                'those records to the incident investigation.',
                       'stakeholder': 'Rob',
                       'original_goal_id': 'SOURCE-G-103'}],
          'inferred': False,
          'interpretation': '',
          'original_goal_ids': ['SOURCE-G-103'],
          'stakeholders': ['Rob'],
          'agents': ['system']},
 'G-100': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'A supervisor reviews work, conditions, and documentation before approving closeout',
           'sources': [{'timestamp': '2026-10-28T21:39:55.085Z',
                        'quote': 'They inspect the work, the conditions, and the paperwork, then approve it '
                                 'when everything looks right. If something isn’t right, they send it back '
                                 'for correction before it’s closed out.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-104'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-104'],
           'stakeholders': ['Rob'],
           'agents': ['supervisor']},
 'G-101': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Incomplete critical safety fields prevent job closeout',
           'sources': [{'timestamp': '2026-10-28T21:53:33.114Z',
                        'quote': 'The record needs the equipment and job identified, every energy source '
                                 'listed, the isolation steps completed, and zero-energy verification '
                                 'recorded. It must show who applied each lock and tag, when it was applied, '
                                 'who verified the isolation, and who released it when the work was '
                                 'complete. A supervisor also needs to review it before the job is closed, '
                                 'and incomplete fields must prevent closeout rather than being left for the '
                                 'next shift.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-105'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-105'],
           'stakeholders': ['Rob'],
           'agents': ['system']},
 'G-102': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Incomplete LOTO records are prevented from being handed to the next shift',
           'sources': [{'timestamp': '2026-10-28T21:59:40.547Z',
                        'quote': 'Mostly right. I want the records available on the floor and usable with '
                                 'poor connectivity, but tablets must not distract anyone operating moving '
                                 'machinery. The system also needs to prevent incomplete LOTO records from '
                                 'being handed off or closed, including who applied the lock, when, and who '
                                 'released it.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-106'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-106'],
           'stakeholders': ['Rob'],
           'agents': ['system']},
 'G-103': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Isolation ownership and verification state are clear to the incoming shift before work',
           'sources': [{'timestamp': '2026-10-28T21:52:03.796Z',
                        'quote': 'The outgoing technician had started the repair late and the handoff was '
                                 'mostly verbal, with the paperwork left incomplete. The morning crew '
                                 'couldn’t tell exactly who owned the isolation or whether the zero-energy '
                                 'verification had been completed, so they stopped rather than guessing.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-107'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-107'],
           'stakeholders': ['Rob'],
           'agents': ['team']},
 'G-104': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Incomplete or incorrect records are returned for correction before closeout',
           'sources': [{'timestamp': '2026-10-28T21:39:55.085Z',
                        'quote': 'They inspect the work, the conditions, and the paperwork, then approve it '
                                 'when everything looks right. If something isn’t right, they send it back '
                                 'for correction before it’s closed out.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-108'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-108'],
           'stakeholders': ['Rob'],
           'agents': ['supervisor']},
 'G-105': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Incidents and near misses are investigated and corrective actions verified',
           'sources': [{'timestamp': '2026-10-28T21:47:04.497Z',
                        'quote': 'First I stop the work and make sure the area and people are safe, then I '
                                 'notify the supervisor and verify the control—especially lockout/tagout, '
                                 'guarding, and PPE—is corrected before anything resumes. I document what '
                                 'happened, investigate whether it was an incident or near miss, assign '
                                 'corrective actions, and track them to closure; retraining is required '
                                 'where competency or procedure was lacking.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-109'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-109'],
           'stakeholders': ['Rob'],
           'agents': []},
 'G-106': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'A near miss is reported within 24 hours even if nobody was hurt',
           'sources': [{'timestamp': '2026-10-28T21:48:09.404Z',
                        'quote': 'We secure the area, preserve the facts, interview the people involved, and '
                                 'identify what control failed or was missing. Corrective actions are '
                                 'assigned with an owner and due date, then I verify they’re actually '
                                 'completed; a near miss must be reported within 24 hours even when nobody '
                                 'was hurt.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-110'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-110'],
           'stakeholders': ['Rob'],
           'agents': ['team']},
 'G-107': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'The area is secured, facts preserved, people interviewed, and failed or missing controls '
                   'identified',
           'sources': [{'timestamp': '2026-10-28T21:48:09.404Z',
                        'quote': 'We secure the area, preserve the facts, interview the people involved, and '
                                 'identify what control failed or was missing. Corrective actions are '
                                 'assigned with an owner and due date, then I verify they’re actually '
                                 'completed; a near miss must be reported within 24 hours even when nobody '
                                 'was hurt.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-111'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-111'],
           'stakeholders': ['Rob'],
           'agents': ['ehs']},
 'G-108': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Corrective actions receive an owner and due date and are tracked to closure',
           'sources': [{'timestamp': '2026-10-28T21:48:09.404Z',
                        'quote': 'We secure the area, preserve the facts, interview the people involved, and '
                                 'identify what control failed or was missing. Corrective actions are '
                                 'assigned with an owner and due date, then I verify they’re actually '
                                 'completed; a near miss must be reported within 24 hours even when nobody '
                                 'was hurt.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-112'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-112'],
           'stakeholders': ['Rob'],
           'agents': ['ehs']},
 'G-109': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Corrective action completion is verified rather than merely recorded',
           'sources': [{'timestamp': '2026-10-28T21:48:09.404Z',
                        'quote': 'We secure the area, preserve the facts, interview the people involved, and '
                                 'identify what control failed or was missing. Corrective actions are '
                                 'assigned with an owner and due date, then I verify they’re actually '
                                 'completed; a near miss must be reported within 24 hours even when nobody '
                                 'was hurt.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-113'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-113'],
           'stakeholders': ['Rob'],
           'agents': ['ehs']},
 'G-110': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Overdue safety actions and actions awaiting verification are conspicuous',
           'sources': [{'timestamp': '2026-10-28T22:02:43.126Z',
                        'quote': 'One last thing: the system should make it obvious when a safety action is '
                                 'overdue or still awaiting verification, rather than letting it disappear '
                                 'in a list. I’d also want an audit trail showing who changed a record and '
                                 'when, because during an inspection we need facts, not guesses.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-114'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-114'],
           'stakeholders': ['Rob'],
           'agents': ['system']},
 'G-111': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Incident investigations link to relevant maintenance, LOTO, and permit records if an '
                   'incident or near miss occurs',
           'sources': [{'timestamp': '2026-10-28T21:50:49.475Z',
                        'quote': 'Not usually in the incident report. The lockout/tagout details belong with '
                                 'the maintenance job and permit record, including the energy sources, who '
                                 'applied each lock, when it was applied, verification of zero energy, and '
                                 'who released it. If something goes wrong or there’s a near miss, we link '
                                 'those records to the incident investigation.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-115'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-115'],
           'stakeholders': ['Rob'],
           'agents': ['system']},
 'G-112': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'A separate environmental report records material, amount, location, response, and '
                   'corrective actions if a maintenance chemical spill occurs',
           'sources': [{'timestamp': '2026-10-28T21:54:48.953Z',
                        'quote': 'It’s both: it’s a company requirement and part of our environmental '
                                 'compliance obligations. A chemical spill during maintenance gets its own '
                                 'environmental report, with the material, amount, location, response, and '
                                 'corrective actions documented separately from the maintenance and safety '
                                 'records.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-116'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-116'],
           'stakeholders': ['Rob'],
           'agents': ['ehs']},
 'G-113': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'People and area are evacuated or secured until safe if a significant spill requires it',
           'sources': [{'timestamp': '2026-10-28T21:54:17.864Z',
                        'quote': 'Yes. We had a maintenance job where a chemical line was opened before it '
                                 'was fully drained, causing a significant spill and forcing us to evacuate '
                                 'the area until it was safe. Nobody was injured, but we stopped the work, '
                                 'investigated the failure, and completed a separate environmental report in '
                                 'addition to the maintenance and safety records.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-117'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-117'],
           'stakeholders': ['Rob'],
           'agents': ['team']},
 'G-114': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Task instruction and demonstrated competency precede maintenance work',
           'sources': [{'timestamp': '2026-10-28T21:43:29.342Z',
                        'quote': 'Training covers the safe method for the task, hazard recognition, PPE, '
                                 'machine guarding, and lockout/tagout verification. Before someone performs '
                                 'maintenance, they need the right instruction and demonstrated competency; '
                                 'after a violation, retraining is corrective action, not a substitute for '
                                 'accountability. We also document attendance, the subject covered, the '
                                 'trainer, and any required refresher date. Separately, I review permits, '
                                 'emergency equipment, and corrective actions during inspections, because '
                                 'paperwork that can’t be verified won’t protect anyone during a regulatory '
                                 'visit.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-118'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-118'],
           'stakeholders': ['Rob'],
           'agents': ['supervisor']},
 'G-115': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Training attendance, subject, trainer, and required refresher date are recorded',
           'sources': [{'timestamp': '2026-10-28T21:43:29.342Z',
                        'quote': 'Training covers the safe method for the task, hazard recognition, PPE, '
                                 'machine guarding, and lockout/tagout verification. Before someone performs '
                                 'maintenance, they need the right instruction and demonstrated competency; '
                                 'after a violation, retraining is corrective action, not a substitute for '
                                 'accountability. We also document attendance, the subject covered, the '
                                 'trainer, and any required refresher date. Separately, I review permits, '
                                 'emergency equipment, and corrective actions during inspections, because '
                                 'paperwork that can’t be verified won’t protect anyone during a regulatory '
                                 'visit.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-119'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-119'],
           'stakeholders': ['Rob'],
           'agents': ['system']},
 'G-116': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Refresher training, permits, and emergency equipment are reviewed or inspected',
           'sources': [{'timestamp': '2026-10-28T21:39:23.025Z',
                        'quote': 'Well, technicians usually record the problem and repair in the maintenance '
                                 'log or CMMS, while safety items go on inspection forms, incident reports, '
                                 'or near-miss forms. Supervisors review the paperwork, and I follow up on '
                                 'corrective actions and retain records for inspections. We also conduct '
                                 'refresher training, review permits, inspect emergency equipment, and '
                                 'prepare for regulatory visits.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-120'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-120'],
           'stakeholders': ['Rob'],
           'agents': ['ehs']},
 'G-117': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Maintenance, LOTO, permit, inspection, incident, and corrective-action evidence is '
                   'accessible together on the floor and during inspections',
           'sources': [{'timestamp': '2026-10-28T21:56:49.332Z',
                        'quote': 'A reliable floor system that brings the maintenance, LOTO, permit, '
                                 'inspection, incident, and corrective-action records together would make a '
                                 'big difference. It needs to work with poor connectivity and require the '
                                 'critical safety information before a job can be closed, because incomplete '
                                 'records become dangerous during shift handoffs and regulatory inspections.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-121'},
                       {'timestamp': '2026-10-28T21:56:49.332Z',
                        'quote': 'A reliable floor system that brings the maintenance, LOTO, permit, '
                                 'inspection, incident, and corrective-action records together would make a '
                                 'big difference. It needs to work with poor connectivity and require the '
                                 'critical safety information before a job can be closed, because incomplete '
                                 'records become dangerous during shift handoffs and regulatory inspections.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-122'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-121', 'SOURCE-G-122'],
           'stakeholders': ['Rob'],
           'agents': ['system']},
 'G-118': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Training records and other retained evidence are accessible and traceable to equipment '
                   'and people',
           'sources': [{'timestamp': '2026-10-28T21:56:07.039Z',
                        'quote': 'Not only in my safety records. Incident, near-miss, inspection, and '
                                 'corrective-action reports are kept in the EHS files, while maintenance and '
                                 'LOTO records belong with the job in the CMMS; permits and some checklists '
                                 'may still be in area binders, and training records are maintained '
                                 'separately. I need access to all of it during an inspection, with the '
                                 'records retained and traceable to the equipment and people involved.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-123'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-123'],
           'stakeholders': ['Rob'],
           'agents': ['system']},
 'G-119': {'type': 'MaintainGoal',
           'category': 'non-functional',
           'text': 'Critical floor records remain usable under poor connectivity',
           'sources': [{'timestamp': '2026-10-28T21:45:44.551Z',
                        'quote': 'Right, a single source of truth would make inspections and follow-up much '
                                 'more reliable. But it has to work on the floor, including areas with poor '
                                 'connectivity; otherwise people will go back to paper, and we’ll have the '
                                 'same gaps under a different name.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-124'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-124'],
           'stakeholders': ['Rob'],
           'agents': ['system']},
 'G-120': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Record creator, changer, reviewer, and closer identity and event date and time are '
                   'retained in an audit trail',
           'sources': [{'timestamp': '2026-10-28T22:03:15.057Z',
                        'quote': 'Right. The audit trail should show who created, changed, reviewed, or '
                                 'closed a record, along with the date and time. That way, if something is '
                                 'questioned during an inspection, we can see what happened instead of '
                                 'relying on somebody’s memory.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-125'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-125'],
           'stakeholders': ['Rob'],
           'agents': ['system']},
 'G-121': {'type': 'AvoidGoal',
           'category': 'non-functional',
           'text': 'Tablet use distracts workers from moving equipment or material handling',
           'sources': [{'timestamp': '2026-10-28T21:59:40.547Z',
                        'quote': 'Mostly right. I want the records available on the floor and usable with '
                                 'poor connectivity, but tablets must not distract anyone operating moving '
                                 'machinery. The system also needs to prevent incomplete LOTO records from '
                                 'being handed off or closed, including who applied the lock, when, and who '
                                 'released it.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-126'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-126'],
           'stakeholders': ['Rob'],
           'agents': []},
 'G-122': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Tablet use occurs from a safe location',
           'sources': [{'timestamp': '2026-10-28T22:00:13.791Z',
                        'quote': 'I mean a tablet can become a hazard if someone is looking down at it while '
                                 'a machine is running or moving materials. Operators should use it only '
                                 'from a safe location, during a pause, or when another qualified person is '
                                 'monitoring the area; no screen is worth taking your eyes off moving '
                                 'equipment.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-127'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-127'],
           'stakeholders': ['Rob'],
           'agents': ['operator']},
 'G-123': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Tablet use occurs during an appropriate pause',
           'sources': [{'timestamp': '2026-10-28T22:00:13.791Z',
                        'quote': 'I mean a tablet can become a hazard if someone is looking down at it while '
                                 'a machine is running or moving materials. Operators should use it only '
                                 'from a safe location, during a pause, or when another qualified person is '
                                 'monitoring the area; no screen is worth taking your eyes off moving '
                                 'equipment.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-128'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-128'],
           'stakeholders': ['Rob'],
           'agents': ['operator']},
 'G-124': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Tablet use occurs while another qualified person monitors the area',
           'sources': [{'timestamp': '2026-10-28T22:00:13.791Z',
                        'quote': 'I mean a tablet can become a hazard if someone is looking down at it while '
                                 'a machine is running or moving materials. Operators should use it only '
                                 'from a safe location, during a pause, or when another qualified person is '
                                 'monitoring the area; no screen is worth taking your eyes off moving '
                                 'equipment.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-129'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-129'],
           'stakeholders': ['Rob'],
           'agents': ['operator']},
 'G-125': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Safety-critical sensor conditions prompt human action and EHS follow-up',
           'sources': [{'timestamp': '2026-10-28T22:02:10.785Z',
                        'quote': 'Right, that’s the idea. The supervisor has to act on the floor '
                                 'immediately, while I need the safety-critical alert and the follow-up '
                                 'record so I can verify the hazard was controlled. Sensor data can warn us, '
                                 'but it never replaces lockout, verification, or a person making the area '
                                 'safe.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-130'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-130'],
           'stakeholders': ['Rob'],
           'agents': []},
 'G-126': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Available sensor data helps flag abnormal temperature, pressure, vibration, or guarding '
                   'conditions',
           'sources': [{'timestamp': '2026-10-28T22:00:51.024Z',
                        'quote': 'Well, the sensor data could help flag abnormal temperatures, pressure, '
                                 'vibration, or guarding conditions, but it cannot replace a worker’s '
                                 'verification before maintenance starts. And if the system shows a '
                                 'safety-critical condition, it needs to be visible to the right supervisor '
                                 'and me, not buried in a maintenance screen.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-131'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-131'],
           'stakeholders': ['Rob'],
           'agents': ['system']},
 'G-127': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Safety-critical alerts are promptly visible to the area supervisor and EHS',
           'sources': [{'timestamp': '2026-10-28T22:01:25.663Z',
                        'quote': 'Not necessarily first every time, but I need to be notified promptly when '
                                 'the condition is safety-critical or could expose someone to danger. The '
                                 'area supervisor should act immediately, and I need visibility for '
                                 'verification and follow-up; sensor data is an alert, not permission to '
                                 'keep working.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-132'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-132'],
           'stakeholders': ['Rob'],
           'agents': ['system']},
 'G-128': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'The area supervisor acts immediately on a safety-critical condition',
           'sources': [{'timestamp': '2026-10-28T22:01:25.663Z',
                        'quote': 'Not necessarily first every time, but I need to be notified promptly when '
                                 'the condition is safety-critical or could expose someone to danger. The '
                                 'area supervisor should act immediately, and I need visibility for '
                                 'verification and follow-up; sensor data is an alert, not permission to '
                                 'keep working.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-133'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-133'],
           'stakeholders': ['Rob'],
           'agents': ['supervisor']},
 'G-129': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'EHS verifies hazard control using the alert and follow-up record',
           'sources': [{'timestamp': '2026-10-28T22:02:10.785Z',
                        'quote': 'Right, that’s the idea. The supervisor has to act on the floor '
                                 'immediately, while I need the safety-critical alert and the follow-up '
                                 'record so I can verify the hazard was controlled. Sensor data can warn us, '
                                 'but it never replaces lockout, verification, or a person making the area '
                                 'safe.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-134'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-134'],
           'stakeholders': ['Rob'],
           'agents': ['ehs']},
 'G-130': {'type': 'AvoidGoal',
           'category': 'functional',
           'text': 'Sensor data substitutes for human isolation verification or authorizes unsafe continued '
                   'work',
           'sources': [{'timestamp': '2026-10-28T22:02:10.785Z',
                        'quote': 'Right, that’s the idea. The supervisor has to act on the floor '
                                 'immediately, while I need the safety-critical alert and the follow-up '
                                 'record so I can verify the hazard was controlled. Sensor data can warn us, '
                                 'but it never replaces lockout, verification, or a person making the area '
                                 'safe.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-135'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-135'],
           'stakeholders': ['Rob'],
           'agents': ['team']},
 'G-131': {'type': 'MaintainGoal',
           'category': 'functional',
           'text': 'EHS retains independent safety authority including stopping unsafe jobs',
           'sources': [{'timestamp': '2026-10-28T21:40:34.274Z',
                        'quote': 'Not exactly. I’m responsible for the EHS function and have authority over '
                                 'safety compliance, but supervisors oversee the maintenance work and verify '
                                 'conditions in their areas. I don’t report to them for safety decisions; I '
                                 'review their work and can stop a job if the controls aren’t right.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-136'}],
           'inferred': False,
           'interpretation': '',
           'original_goal_ids': ['SOURCE-G-136'],
           'stakeholders': ['Rob'],
           'agents': ['ehs']},
 'G-132': {'type': 'AchieveGoal',
           'category': 'functional',
           'text': 'Critical records captured during connectivity loss are retained and synchronized when '
                   'service returns',
           'sources': [{'timestamp': '2026-10-28T21:45:44.551Z',
                        'quote': 'Right, a single source of truth would make inspections and follow-up much '
                                 'more reliable. But it has to work on the floor, including areas with poor '
                                 'connectivity; otherwise people will go back to paper, and we’ll have the '
                                 'same gaps under a different name.',
                        'stakeholder': 'Rob',
                        'original_goal_id': 'SOURCE-G-137'}],
           'inferred': True,
           'interpretation': 'Local retention and synchronization are an inferred implementation of '
                             'poor-connectivity usability; storage, synchronization, and conflict rules need '
                             'confirmation.',
           'original_goal_ids': ['SOURCE-G-137'],
           'stakeholders': ['Rob'],
           'agents': ['system']}}

REFINEMENTS = {1: [('H4', [2, 29, 30, 31, 32])], 2: [('H4', [3, 7, 16, 20, 21, 23, 24])], 3: [('H4', [4, 5, 6])], 7: [('H5', [8, 9, 10, 11, 12, 15, 28])], 16: [('H4', [17, 18, 19, 28])], 21: [('H4', [22])], 23: [('H4', [17, 27])], 24: [('H4', [4])], 25: [('H4', [33])], 28: [('H4', [13]), ('H4', [14])], 34: [('H4', [35, 36, 37, 46, 56, 59, 65, 74, 78, 79])], 35: [('H4', [38, 55, 80])], 36: [('H4', [7, 39, 40, 44, 45, 57, 58, 82])], 37: [('H4', [39, 41, 42, 43])], 46: [('H5', [47, 48, 49, 50, 51, 52, 53, 54])], 56: [('H4', [57, 58])], 59: [('H5', [60, 61, 62, 63, 64])], 65: [('H4', [66, 67, 68, 72, 73, 81])], 74: [('H4', [75, 76, 77])], 80: [('H4', [55, 79])], 81: [('H4', [69]), ('H4', [70]), ('H4', [71])], 83: [('H4', [85, 90, 95, 96, 105, 112, 113, 114, 116, 121, 125, 131])], 84: [('H4', [96, 105, 115, 117, 120])], 85: [('H5', [86, 87, 88, 89])], 90: [('H5', [91, 92, 93, 94])], 96: [('H5', [97, 98, 99, 100, 101, 102, 103, 104])], 105: [('H4', [106, 107, 108, 109, 110, 111])], 116: [('H4', [117, 118, 119])], 119: [('H4', [132])], 121: [('H4', [122]), ('H4', [123]), ('H4', [124])], 125: [('H5', [126, 127, 128, 129, 130])]}

ROOT_IDS = [1, 25, 26, 34, 83, 84]

MERGED_SOURCE_GOALS = {'SOURCE-G-4': {'retained_source_goal': 'SOURCE-G-3',
                'combined_goal': 'G-3',
                'combined_text': 'Recent faults and prior repairs for the selected press are displayed on '
                                 'the tablet at the press'},
 'SOURCE-G-23': {'retained_source_goal': 'SOURCE-G-22',
                 'combined_goal': 'G-21',
                 'combined_text': 'The intended press can be found by searching its floor nickname'},
 'SOURCE-G-41': {'retained_source_goal': 'SOURCE-G-8',
                 'combined_goal': 'G-7',
                 'combined_text': 'Technicians record machine stops, maintenance findings, and repair '
                                  'actions on tablets at the press'},
 'SOURCE-G-89': {'retained_source_goal': 'SOURCE-G-88',
                 'combined_goal': 'G-85',
                 'combined_text': 'Task-specific hazards, severity, likelihood, and hierarchy-based controls '
                                  'are assessed before maintenance starts'},
 'SOURCE-G-122': {'retained_source_goal': 'SOURCE-G-121',
                  'combined_goal': 'G-117',
                  'combined_text': 'Maintenance, LOTO, permit, inspection, incident, and corrective-action '
                                   'evidence is accessible together on the floor and during inspections'}}

def build_model():
    names = {'system': 'Maintenance logging system', 'technician': 'Maintenance technician',
             'organization': 'Organization policy representative - inferred responsibility',
             'supervisor': 'Shift supervisor or maintenance lead', 'manager': 'Plant manager',
             'ehs': 'EHS coordinator', 'team': 'Maintenance team - accountability to confirm',
             'operator': 'Worker using tablet'}
    agents = {key: Agent(name, AgentType.SOFTWARE_AGENT if key == 'system'
                        else AgentType.ENVIRONMENT_AGENT) for key, name in names.items()}
    types = {'AchieveGoal': AchieveGoal, 'MaintainGoal': MaintainGoal,
             'AvoidGoal': AvoidGoal, 'SoftGoal': SoftGoal}
    goals = {}
    for gid, record in SOURCE_GOALS.items():
        performances = []
        for actor in record['agents']:
            category = (OperationCategory.SOFTWARE_TO_BE_OPERATION if actor == 'system'
                        else OperationCategory.ENVIRONMENT_OPERATION)
            performances.append(PerformanceLink(agents[actor], Operation(record['text'], category)))
        goals[gid] = types[record['type']](name=f"{gid}: {record['text']}",
            annotation=record['category'], performs=performances,
            leaf=bool(performances) and int(gid[2:]) not in REFINEMENTS)
    for parent, alternatives in REFINEMENTS.items():
        goals[f'G-{parent}'].disjunctions = [Refinement(complete=False,
            children=[goals[f'G-{c}'] for c in children], annotation=annotation)
            for annotation, children in alternatives]
    return goals

def render_model():
    goals = build_model()
    # Compact visualization: keep each responsible agent connected to its goal,
    # but omit operation nodes that repeat the goal text. Full operations remain
    # available through build_model() and all source evidence remains above.
    for goal in goals.values():
        for performance in goal.performs:
            performance.operation = None
    graph = generate_graph([goals[f'G-{i}'] for i in ROOT_IDS], [])
    graph += '\nclassDef inferred fill:#fff176,stroke:#000\n'
    for gid, record in SOURCE_GOALS.items():
        if record['inferred']:
            graph += f"class {goals[gid].get_node_id()} inferred\n"
    return graph

if __name__ == '__main__':
    graph = render_model()
    folder = Path(__file__).resolve().parent
    (folder / 'goal_model_all.mmd').write_text(graph, encoding='utf-8')
    link = generate_pako_link(graph, 'edit')
    (folder / 'mermaid_all.txt').write_text(link + '\n', encoding='utf-8')
    print(link)
