"""Rebuild the JSON, diagrams, provenance tables, review views, and partial ZIP.

The use-case texts and mappings below were explicitly authored from the supplied
interviews. Generation only serializes those decisions; it does not infer links.
No reflection text is generated, edited, or included by this script.
"""
from pathlib import Path
from collections import Counter
import csv
import html
import json
import re
import zipfile
from goal_catalog import GOALS, ALIASES
from model_support import HERE, export_model

BASE = HERE if (HERE/'sources').exists() else HERE.parent
REVIEW = BASE/'review'
SOURCE = HERE/'sources' if (HERE/'sources').exists() else BASE.parent/'Requirements Elicitation'/'sources'
MARK = '<mark style="background-color:#fff59d">{}</mark>'

def added(text):
    return MARK.format(text)

USE_CASES = []
MAPPINGS = []
UC_EVIDENCE = {}

def uc(n,name,actors,pre,steps,post,nfr,goals,evidence):
    """Each step is (text, explicit matching goal IDs); outer list position is m."""
    uid=f'UC-{n}'
    USE_CASES.append(dict(uc_name=name,uc_id=uid,actors=actors,pre_conditions=pre,
        flow_of_events=[s for s,_ in steps],post_conditions=post,non_functional=nfr))
    UC_EVIDENCE[uid]=evidence.split()
    MAPPINGS.extend((uid,f'G-{g}') for g in goals)
    for m,(_,gs) in enumerate(steps,1):
        MAPPINGS.extend((f'{uid}@{m}',f'G-{g}') for g in gs)


uc(1,'Diagnose a press fault and capture findings',
 ['Mechanic','Maintenance system'],
 ['A press is showing a fault or producing bad parts.',
  added('The mechanic uses the tablet from a safe stationary position away from moving machinery.')],
 [
  (added('The mechanic selects the affected asset record.'),[7,57]),
  ('The mechanic reviews the shift handoff, prior troubleshooting, closed work orders, and recorded part numbers.',[14,15,16]),
  ('The system displays actual temperature, setpoint, and normal range together.',[4]),
  (added('If a live reading is unavailable or stale, the system flags that condition instead of presenting it as current; the mechanic obtains a current reading before relying on it.'),[75]),
  ('The mechanic compares temperature behavior with part quality and heater cycling to form the diagnosis.',[3,5]),
  ('The mechanic records the asset, symptom or fault code, actual reading, and setpoint.',[7,8]),
  ('The mechanic attaches a quick photo or short voice note rather than typing the entire account.',[11,12,13]),
  (added('If a voice note is used, the mechanic confirms that its content accurately represents the finding before publishing it.'),[72]),
  (added('The mechanic records the required shared facts separately from personal notebook content; personal notes are private unless the mechanic explicitly selects content to share.'),[23,24,76]),
  ('The mechanic captures the finding and any change before moving on, using the briefest practical interaction.',[2,10]),
 ],
 ['The shared record contains the identified fault, measured values, and captured evidence.',
  added('Personal working notes have not been copied into the shared record without the mechanic selecting them.')],
 ['Capture should require little effort with gloves and in noise.',
  'Tablet use must not distract personnel around moving machinery.',
  added('An unavailable live reading is visibly distinguished from a current reading.')],
 [1,2,3,6,23,67,74],
 'T0@00:59:52.304 T0@01:00:17.854 T0@01:02:46.799 T2@01:31:05.537 R@17:34:09.701')

uc(2,'Locate a replacement part, repair, and verify the press',
 ['Mechanic','Maintenance system'],
 ['The mechanic has identified a suspected press fault and needs a replacement part.',
  added('Physical work follows the plant safety procedure; a software record is not proof of physical isolation.')],
 [
  ('The mechanic retrieves the exact part number, stock quantity, crib location, and any approved substitute.',[17,18]),
  ('The mechanic checks the crib bin against the press part number and obtains the matching part.',[17,18]),
  ('The mechanic stops the press and confirms lockout/tagout before opening equipment.',[19,20]),
  ('The mechanic records the confirmed safety check on the tablet.',[21]),
  ('The mechanic checks the heater band and connections, replaces the weak band, and records what was tested or changed and the installed part number.',[9,22]),
  ('The mechanic performs the verification run and records actual temperature, part quality, and whether verification passed.',[8,9,22]),
  (added('If verification fails, the mechanic records the failure and leaves the issue open for further diagnosis; a successful repair is not declared.'),[9,38,41]),
 ],
 ['The work order records tests, corrective action, installed part, measured values, and verification status.',
  'The outcome is available for the next shift to avoid repeating undocumented checks.'],
 ['Isolation must be confirmed before equipment is opened.',
  'Repair evidence must remain traceable to the equipment and work order.'],
 [1,6,19],
 'T0@01:02:46.799 T2@01:30:30.890 T2@01:31:05.537 T2@01:32:31.268 T2@01:33:22.867')

uc(3,'Complete a work order and acknowledge the shift handover',
 ['Mechanic','Outgoing supervisor','Incoming supervisor','Maintenance system'],
 ['A maintenance work order or unresolved machine issue must be handed to the next shift.'],
 [
  ('The outgoing supervisor reviews stopped machines, open repairs, machine status, work ownership, expected restoration, and production impact.',[26,27]),
  ('The system presents linked downtime, alarms, diagnosis, corrective action, reason code, parts, readings, and verification details.',[6,7,8,9,28,54]),
  ('The supervisor checks downtime minutes against the machine stop and first good part.',[30,33]),
  ('If the work order is being completed, the system requires a reason code; missing codes or other required fields are shown to the supervisor.',[31,32]),
  ('The supervisor obtains the missing reason before completion, and assigns responsibility for missing safety-release items.',[31,42]),
  ('The outgoing and incoming supervisors agree the open-work owner, what to monitor, and when to escalate.',[27,29]),
  ('The incoming supervisor acknowledges the digital handoff after the critical fields are complete.',[53]),
  ('The system associates the handover facts with the equipment, time window, and shift for access across all three shifts.',[44,57]),
 ],
 ['The next shift has an acknowledged handover with explicit machine status and work ownership.',
  'A completed work order includes its reason code and checked downtime minutes; unresolved issues remain identified.'],
 ['Missing required data must be visible instead of disappearing into the next shift.',
  'Maintenance data must be accurate enough to support decisions.'],
 [6,25,26,30,44],
 'A@13:32:47.328 A@13:33:20.301 A@13:34:52.902 A@13:37:46.015 R@17:33:39.894')

uc(4,'Prioritize and escalate an unresolved machine issue',
 ['Shift supervisor','Maintenance lead','Production supervisor','Angela'],
 ['A machine issue remains unresolved and its production or safety impact needs review.'],
 [
  ('The supervisor checks whether the machine is a bottleneck, lacks a practical backup, stops a production cell, or has a history of long downtime or high-impact quality issues.',[34]),
  ('The supervisor reviews the restoration estimate, current status, and production impact.',[27]),
  ('If the restoration target is exceeded, critical equipment is affected, or a safety or quality risk exists, the supervisor escalates to the maintenance lead, production supervisor, or Angela.',[35,36]),
  ('The escalation record identifies its owner, time, reason, and next action.',[37]),
  ('The supervisor includes monitoring and escalation expectations in the handover.',[29]),
 ],
 ['An issue meeting an escalation condition has a named escalation owner and next action.',
  'The next shift can see the current escalation state.'],
 ['Priority should reflect actual equipment and production impact rather than an unclassified alarm alone.'],
 [25,34,35],
 'A@13:31:57.701 A@13:33:54.358 A@13:34:52.902 A@13:35:19.832')

uc(5,'Review safety hold and authorize return to service',
 ['Mechanic','Shift supervisor','Authorized release person','Maintenance system'],
 ['A repaired or held machine is being considered for return to service.'],
 [
  ('The technician records the failure, corrective action, replaced parts, readings, verification outcome, and safety documentation.',[7,8,9,39,40,54]),
  ('The isolation record identifies the equipment, isolation points, each lock applier, date and time, and release authorizer and performer.',[49]),
  ('The supervisor checks hazard assessment, isolation, alarm status, applicable permits, inspection, and unresolved hazards and validates the controls.',[38,48,51]),
  ('The supervisor identifies the person responsible for each missing release item; the hold remains visible.',[42,68]),
  ('If required fields or release documentation are incomplete, or a hazard is unresolved, equipment remains on hold despite production pressure.',[38,41]),
  (added('If a release request is attempted while checks are incomplete, the system rejects the request and displays the missing items.'),[73]),
  ('If the required controls and records are complete and hazards addressed, the authorized person records the return-to-service authorization and the technician/supervisor acknowledgments before equipment release.',[38,50,51]),
  ('The system retains the permit, photos, alarms, release decision, and history of record changes with the work order.',[40,54,55]),
 ],
 ['Equipment is either held with visible outstanding items or released following recorded approval and validated controls.',
  'The decision, responsible persons, and supporting records are traceable.'],
 ['Production pressure must not override the safety hold.',
  'Personnel must not be penalized for following the procedure and stopping an unsafe restart.',
  added('The system records and checks authorization; it does not itself apply locks or physically prove isolation.')],
 [38,41,45,46,68],
 'A@13:35:53.834 A@13:36:11.712 A@13:37:14.563 R@17:31:15.628 R@17:33:39.894 R@17:44:38.682')

uc(6,'Report and follow through on a near miss',
 ['Reporter','Shift supervisor','Safety coordinator','Corrective-action owner'],
 ['A near miss is observed or mentioned during a handoff, even if nobody is injured.'],
 [
  ('The person hearing or observing the near miss opens a report with what happened, where, when, and who was involved, within 24 hours.',[61,62]),
  ('A named person owns the report and the supervisor acknowledges it before the 24-hour deadline.',[62,63]),
  ('The report is treated as part of normal handover and is not closed merely because the event was mentioned verbally.',[61,53]),
  ('The safety coordinator reviews the facts, existing controls, and changes needed to prevent recurrence without punishing the reporter for speaking up.',[64]),
  ('A named person owns any resulting corrective action, and its completion is verified.',[65]),
 ],
 ['The near miss has a recorded, acknowledged report and reviewed facts.',
  'Any identified corrective action has an owner and verified completion before that action is treated as complete.'],
 ['Reporting and supervisor acknowledgment occur within the stakeholder-specified 24 hours.',
  'Required reporting facts should be brief and review should focus on unsafe conditions rather than blame.'],
 [46,61,64,65],
 'R@17:34:09.701 R@17:45:20.933 R@17:45:57.392 R@17:46:28.516 R@17:46:57.049')

uc(7,'Create a separate environmental spill report',
 ['Reporter','Safety coordinator'],
 ['A chemical spill occurs during maintenance.'],
 [
  ('The reporter creates a separate environmental report for the chemical spill instead of recording it only as a repair-log note.',[66]),
  (added('The reporter references the affected equipment and maintenance time window so the spill report can be found alongside the maintenance context.'),[57,58]),
 ],
 ['The spill is documented in a separate environmental report.'],
 ['The environmental report remains distinct from ordinary repair notes.'],
 [66],
 'R@17:34:09.701 R@17:44:38.682')

uc(8,'Investigate a safety alarm or recurring failure',
 ['Mechanic','Shift supervisor','Safety coordinator'],
 ['A sensor alarm or recurring failure calls for a maintenance safety decision.'],
 [
  ('The supervisor stops affected work and documents the hazard if the alarm requires investigation.',[69]),
  ('The technician and supervisor verify the hazard, isolation, and whether the alarm is still active; the safety coordinator reviews the permit and equipment history.',[48,49,69]),
  ('The alarm information is preserved with the maintenance record.',[54]),
  ('The safety coordinator reviews recurring alarms and failure modes and determines whether shutdown, corrective action, or a formal safety inspection is needed.',[70]),
  ('The equipment remains unreleased until the hazard is addressed and required records and authorization are complete.',[38,41]),
 ],
 ['The alarm and hazard decision are recorded and an unsafe release has been prevented.'],
 ['Safety-critical findings must be prominent rather than buried in general maintenance notes.',
  'Tablet use must not distract personnel around moving machinery.'],
 [46,48,67,68,69,70],
 'R@17:30:09.217 R@17:30:42.356 R@17:32:26.552 R@17:33:12.862 R@17:50:37.717')

uc(9,'Retrieve and export an inspectable equipment history',
 ['Safety coordinator','Inspector','Maintenance system'],
 ['An inspector requests maintenance and safety evidence for equipment and a time period.'],
 [
  (added('The safety coordinator enters the equipment identifier and requested time window.'),[56,57]),
  ('The system retrieves the linked maintenance, isolation, alarms, permits, photos, corrective actions, acknowledgments, and return-to-service history.',[54,56,58]),
  ('The coordinator reviews who changed what and when, retaining the history of corrections.',[55]),
  ('The coordinator retrieves readable records for the full inspection period even if equipment has been retired or personnel have changed jobs.',[59]),
  (added('If the applicable inspection retention period has not been configured, the safety coordinator defines it before any record disposal is scheduled; no arbitrary duration is substituted.'),[77]),
  ('The coordinator exports the requested records in a form the inspector can review without access to the entire operating system.',[60]),
 ],
 ['The inspector can review a complete equipment history and correction history without relying on staff memory.'],
 ['Records remain readable and retrievable for the full applicable inspection period.',
  'Export does not require granting broad access to the operating system.'],
 [55,56,57,58,59,60],
 'R@17:44:38.682 R@17:47:27.669 R@17:48:39.537 R@17:49:15.529')


def source_records():
    names={'T0':'teo-initial.csv','T1':'teo-follow-up-1.csv','T2':'teo-follow-up-2.csv',
        'A':'angela-initial.csv','R':'rob-interview.csv'}
    result={}
    for prefix,fn in names.items():
        with (SOURCE/fn).open(encoding='utf-8-sig',newline='') as f:
            for record,row in enumerate(csv.DictReader(f),1):
                if row['Speaker']=='Stakeholder':
                    key=prefix+'@'+row['Timestamp'][11:-1]
                    result[key]={'file':fn,'record':record,**row}
    return result


def write_json(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def build():
    REVIEW.mkdir(exist_ok=True)
    models={name:export_model(name)[0] for name in ('teo','angela','rob','combined')}
    specs=models['combined']['specs']
    sources=source_records()
    for s in GOALS.values():
        for ref in s['evidence']:
            assert ref in sources, (s['id'],ref)
    for refs in UC_EVIDENCE.values():
        assert all(r in sources for r in refs)
    write_json(HERE/'use_cases.json',USE_CASES)
    rows=list(dict.fromkeys((u,ALIASES.get(g,g)) for u,g in MAPPINGS))
    matched_goals={g for _,g in rows}
    all_steps=[f"{u['uc_id']}@{i}" for u in USE_CASES for i in range(1,len(u['flow_of_events'])+1)]
    matched_ucs={u for u,_ in rows}
    for u in [x['uc_id'] for x in USE_CASES]+all_steps:
        if u not in matched_ucs: rows.append((u,'None'))
    for gid in specs:
        if gid not in matched_goals: rows.append(('None',gid))
    # Literal 2 x P as requested in the handout: first array is UC/step IDs;
    # second array is the corresponding goal IDs. None is the literal string
    # requested by the handout, not JSON null.
    write_json(HERE/'matrix.json',[[u for u,_ in rows],[g for _,g in rows]])
    write_json(REVIEW/'matrix.rows.json',rows)
    with (REVIEW/'matrix.csv').open('w',newline='') as f:
        w=csv.writer(f); w.writerow(['Use case or step ID','Goal ID']); w.writerows(rows)
    evidence={gid:{**s,'source_passages':[sources[r] for r in s['evidence']]} for gid,s in specs.items()}
    write_json(REVIEW/'goal_evidence.json',evidence)
    write_json(REVIEW/'use_case_evidence.json',{u:[sources[r] for r in refs] for u,refs in UC_EVIDENCE.items()})
    with (REVIEW/'goal_evidence.csv').open('w',newline='') as f:
        w=csv.writer(f)
        w.writerow(['Goal ID','Goal','Kind','Category','Agent','Added interpretation','Source CSV','CSV record','UTC timestamp','Stakeholder evidence'])
        for gid,s in specs.items():
            for r in s['evidence']:
                p=sources[r]
                w.writerow([gid,s['text'],s['kind'],s['category'],s['agent'],s['inferred'],p['file'],p['record'],p['Timestamp'],p['Speech']])
    # Readable HTML mirrors exactly the model catalog and JSON, including
    # yellow highlighting, and contains no personal reflection.
    style='body{font:16px/1.5 system-ui;max-width:1100px;margin:36px auto;padding:0 24px;color:#18212b} table{border-collapse:collapse;width:100%}td,th{padding:9px;border:1px solid #bbb;text-align:left;vertical-align:top}h1,h2{color:#153c56}mark{background:#fff59d}code{font-size:14px}.small{font-size:13px;color:#475569}li{margin:6px 0}'
    parts=[f'<!doctype html><html><meta charset="utf-8"><title>Requirements Analysis review</title><style>{style}</style><body>',
      '<h1>Requirements Analysis: review copy</h1><p>AI-generated draft based on Teo, Angela, and Rob interviews. Yellow marks an interpretation not explicitly stated in the source. Personal reflection is intentionally absent.</p>',
      '<h2>Combined goal catalog</h2><table><tr><th>ID</th><th>Goal</th><th>Type / category</th><th>Agent and evidence</th></tr>']
    for gid,s in specs.items():
        text=html.escape(f"{s['kind']}[{s['text']}]")
        if s['inferred']: text=MARK.format(text)
        parts.append(f'<tr><td>{gid}</td><td>{text}</td><td>{s["kind"]}<br>{s["category"]}</td><td>{html.escape(s["agent"] or "Refined below")}<br><span class="small">{"; ".join(s["evidence"])}</span></td></tr>')
    parts.append('</table><h2>Use cases</h2>')
    for u in USE_CASES:
        parts.append(f'<h3>{u["uc_id"]}: {u["uc_name"]}</h3><p><b>Actors:</b> {", ".join(u["actors"])}</p>')
        for key,title in [('pre_conditions','Preconditions'),('flow_of_events','Flow of events'),('post_conditions','Postconditions'),('non_functional','Non-functional requirements')]:
            parts.append(f'<h4>{title}</h4><ol>')
            for i,text in enumerate(u[key],1):
                prefix=f'<code>{u["uc_id"]}@{i}</code> ' if key=='flow_of_events' else ''
                parts.append(f'<li>{prefix}{text}</li>')
            parts.append('</ol>')
    parts.append('<h2>Traceability matrix</h2><p>Readable transpose of matrix.json (which is stored as 2 x P).</p><table><tr><th>Use case / step</th><th>Goal</th></tr>')
    parts.extend(f'<tr><td>{u}</td><td>{g}</td></tr>' for u,g in rows)
    parts.append('</table></body></html>')
    (REVIEW/'review.html').write_text('\n'.join(parts),encoding='utf-8')
    make_diagram_viewer()
    # Validate artifact semantics, references, graph topology, and highlight coverage.
    assert len(GOALS)==len(set(GOALS))
    for name,model in models.items():
        children={c for _,cs,_,_ in model['relations'] for c in cs}
        for gid,s in model['specs'].items():
            if gid not in {p for p,_,_,_ in model['relations']}:
                assert s['agent'], (name,'unassigned leaf',gid)
        def walk(gid,stack):
            assert gid not in stack, (name,'cycle',gid)
            for p,cs,code,full in model['relations']:
                if p==gid:
                    assert code in {'H3','H4','H5','H6','H7','H8','H9','H10','H11','H12','P1','P2','P3','P4','P5','P6','P7'}
                    for c in cs: walk(c,stack|{gid})
        for root in model['roots']: walk(root,set())
    for u,g in rows:
        assert u=='None' or u in {x['uc_id'] for x in USE_CASES}|set(all_steps),u
        assert g=='None' or g in specs,g
    assert set(specs) <= {g for _,g in rows}
    assert set(all_steps) <= {u for u,_ in rows}
    assert {s['category'] for s in specs.values()}=={'functional','non-functional'}
    assert any(Counter(p for p,_,_,_ in model['relations'])[p]>1 for model in models.values() for p,_,_,_ in model['relations'])
    report={'status':'PASS','individual_goal_counts':{n:len(m['specs']) for n,m in models.items() if n!='combined'},
        'combined_goal_count':len(specs),'retired_duplicate_ids':ALIASES,'use_case_count':len(USE_CASES),
        'use_case_step_count':len(all_steps),'matrix_shape':[2,len(rows)],
        'added_goal_ids':[k for k,s in specs.items() if s['inferred']],
        'unmapped_goals':[g for u,g in rows if u=='None'],
        'checks':['all goal evidence references resolve to stakeholder utterances','every combined goal and use-case step represented in matrix','all leaf goals assigned to an agent','refinement graphs are acyclic','explicit OR alternative exists','functional and non-functional categories present','no retired goal IDs referenced in matrix'],
        'missing_required_file':'reflections.pdf (intentionally left for Timothy)',
        'cautions':['Structural validation does not replace the student review of source accuracy and refinement semantics.','Potential conflict links are conditional tensions, explained in analysis.md.']}
    write_json(REVIEW/'validation.json',report)
    print(json.dumps(report,indent=2))


def make_diagram_viewer():
    data={n:(HERE/'generated'/f'goal_model_{n}.mmd').read_text() for n in ('combined','teo','angela','rob')}
    # connect-src 'none' and a local-only script policy keep all model content
    # in the local file. The vendor bundle was downloaded separately as public
    # software; model text is never sent to the library's download server.
    page='''<!doctype html><html><head><meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'self' 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; font-src data:; connect-src 'none'">
<title>Offline goal model review</title>
<style>body{font:16px system-ui;margin:24px;color:#17212b}h1{margin-bottom:6px}button,select{padding:8px;font-size:15px;margin:4px}#viewport{overflow:auto;width:calc(100vw - 54px);height:72vh;border:1px solid #abc;background:#fff}#status{padding:8px;background:#eef4f8;margin:12px 0}#legend{background:#fff59d;padding:5px}svg{max-width:none!important}#error{color:#b91c1c;white-space:pre-wrap}</style>
</head><body><h1>Offline goal model review</h1>
<p>Local rendering only. Drag the scrollbars to inspect the full graph; use zoom to read individual branches. <span id="legend">Yellow: added interpretation</span></p>
<label>Model <select id="model"><option value="combined">Combined</option><option value="teo">Teo</option><option value="angela">Angela</option><option value="rob">Rob</option></select></label>
<button id="out">Zoom out</button><button id="in">Zoom in</button><button id="fit">Fit width</button><button id="actual">100%</button><span id="zoom"></span>
<label>Find goal <input id="goal" placeholder="G-38" size="7"></label><button id="find">Focus goal</button>
<div id="status">Checking all four diagrams...</div><div id="error"></div><div id="viewport"><div id="graph"></div></div>
<script src="vendor/mermaid.min.js"></script><script>
const diagrams=__DATA__;
const cache={};let zoom=1;let current='combined';
mermaid.initialize({startOnLoad:false,securityLevel:'strict',theme:'neutral',maxTextSize:200000,flowchart:{htmlLabels:true,curve:'linear',nodeSpacing:35,rankSpacing:60},themeVariables:{fontFamily:'Arial',fontSize:'15px'}});
function resize(){const svg=document.querySelector('#graph svg');if(!svg)return;const box=svg.viewBox.baseVal;svg.style.width=(box.width*zoom)+'px';svg.style.height=(box.height*zoom)+'px';document.querySelector('#zoom').textContent=Math.round(zoom*100)+'%';}
function show(name){current=name;document.querySelector('#graph').innerHTML=cache[name];resize();document.querySelector('#viewport').scrollTo(0,0);}
document.querySelector('#model').onchange=e=>show(e.target.value);
document.querySelector('#in').onclick=()=>{zoom=Math.min(2,zoom*1.25);resize()};
document.querySelector('#out').onclick=()=>{zoom=Math.max(.03,zoom/1.25);resize()};
document.querySelector('#actual').onclick=()=>{zoom=1;resize()};
document.querySelector('#fit').onclick=()=>{const s=document.querySelector('#graph svg');zoom=document.querySelector('#viewport').clientWidth/s.viewBox.baseVal.width;resize()};
document.querySelector('#find').onclick=()=>{const id=document.querySelector('#goal').value.trim().toUpperCase();const nodes=[...document.querySelectorAll('#graph svg .node')];const n=nodes.find(n=>n.textContent.includes(id+' '));if(!n){document.querySelector('#error').textContent='Goal not found in this view';return}document.querySelector('#error').textContent='';zoom=1;resize();const v=document.querySelector('#viewport');const r=n.getBoundingClientRect();const b=v.getBoundingClientRect();v.scrollBy(r.left-b.left-v.clientWidth/2+r.width/2,r.top-b.top-v.clientHeight/2+r.height/2)};
(async()=>{try{for(const [name,code] of Object.entries(diagrams)){await mermaid.parse(code);const result=await mermaid.render('model_'+name,code);cache[name]=result.svg;document.querySelector('#status').textContent='Rendered '+Object.keys(cache).length+' of 4 diagrams';}show('combined');document.querySelector('#status').textContent='PASS: Combined, Teo, Angela, and Rob diagrams parsed and rendered successfully. No external connections allowed.';}catch(e){document.querySelector('#status').textContent='FAIL: diagram rendering';document.querySelector('#error').textContent=String(e);}})();
</script></body></html>'''
    (REVIEW/'diagrams.html').write_text(page.replace('__DATA__',json.dumps(data).replace('</','<\\/')),encoding='utf-8')


if __name__=='__main__':
    build()
