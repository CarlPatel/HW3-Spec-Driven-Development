// REQ-01–09: client-only state and authoritative prototype validation.
export const REASONS = ['Hydraulic','Electrical/Heater','Mechanical','Material','Setup/Changeover','Operator','Safety hold','Other'];
export const USERS = [
 {id:'teo',name:'Teo Salinas',role:'Technician',shift:'Night'},
 {id:'maya',name:'Maya Chen',role:'Technician',shift:'Day'},
 {id:'eli',name:'Eli Brooks',role:'Technician',shift:'Swing'},
 {id:'op',name:'Jordan Lee',role:'Operator',shift:'Day'},
 {id:'sup',name:'Sam Rivera',role:'Shift Supervisor',shift:'Day'},
 {id:'sup-night',name:'Riley Park',role:'Shift Supervisor',shift:'Night'},
 {id:'sup-swing',name:'Alex Morgan',role:'Shift Supervisor',shift:'Swing'}
];
export const MACHINES = [
 ['p17','Press 17','Atlas','IM-017','A',true,['Hydraulic','Electrical']],
 ['p12','Press 12','Red Fox','IM-012','A',true,['Hydraulic','Electrical']],
 ['m8','Molder 8','Molder 8','IM-008','B',true,['Electrical','Pneumatic']],
 ['p3','Press 3','Old Blue','IM-003','B',false,['Hydraulic','Electrical']],
 ['p21','Press 21','Orion','IM-021','C',true,['Electrical','Pneumatic']],
 ['p6','Press 6','Scout','IM-006','C',false,['Electrical']]
].map(([id,name,nickname,asset,line,sensors,energySources])=>({id,name,nickname,asset,line,sensors,energySources}));
const need=(ok,message)=>{if(!ok)throw new Error(message);};
const id=s=>`r${++s.sequence}`;
export function shiftAt(at){
 const d=new Date(at), h=d.getHours(); let name,startHour;
 if(h>=22){name='Night';startHour=22;}else if(h>=14){name='Swing';startHour=14;}else if(h>=6){name='Day';startHour=6;}else{name='Night';startHour=22;d.setDate(d.getDate()-1);}
 d.setHours(startHour,0,0,0); const start=+d;d.setHours(d.getHours()+8);
 return {name,start,end:+d};
}
export function verificationEnd(at){const sh=shiftAt(at);if(at===sh.start)return sh.end;return shiftAt(sh.end).end;}
export function createState(now=+new Date(2026,10,15,6,10),seed=true){
 const s={now,sequence:0,machines:structuredClone(MACHINES),users:structuredClone(USERS),events:[]};
 if(seed){const original=s.now;s.now=original-65*60000;let e=openEvent(s,'m8','manual',USERS[0]);addEntry(s,e,USERS[0],{found:'Hydraulic seep at return line',tested:'Seal inspected; pressure test pending',temporary:'Temporary seal installed',next:'Pressure test before restart'});
 s.now=original-40*60000;e=openEvent(s,'p12','sensor',USERS[0]);applyLock(s,e,USERS[0],'Hydraulic');verifyZero(s,e,USERS[0],e.locks[0].id);addEntry(s,e,USERS[0],{next:'Inspect pressure drop; electrical isolation still needed'});s.now=original;}
 return s;
}
export function machine(s,id){const m=s.machines.find(m=>m.id===id);need(m,'Machine not found');return m;}
// REQ-01/02, F-03: production intervals and administrative closeout are distinct.
export const openRecords = (s, machineId) => s.events.filter(e => e.machineId === machineId && e.closedAt === null);
export const activeFor = (s, machineId) => s.events.find(e => e.machineId === machineId && e.firstGoodAt === null);
export const openFor = (s, machineId) => activeFor(s, machineId) || openRecords(s, machineId).at(-1);
const editable = e => need(e.closedAt === null, 'This event is closed and read-only.');
const role = (u, roles) => need(roles.includes(u.role), `Requires ${roles.join(' or ')} role.`);
const stamp = (s, u) => ({user: {...u}, at: s.now, shift: u.shift});

export function openEvent(s, machineId, source, u) {
  const m = machine(s, machineId);
  need(source === 'manual' || source === 'sensor', 'Unknown stop source');
  if (source === 'sensor') need(m.sensors, 'This machine has no sensors; use Report stop.');
  else role(u, ['Technician', 'Operator']);
  const active = activeFor(s, machineId);
  if (active) return active;
  const previous = s.events.filter(e => e.machineId === machineId).at(-1);
  const e = {
    id: id(s), machineId, stoppedAt: s.now,
    source: source === 'sensor' ? 'sensor' : m.sensors ? 'manual' : 'manual – no sensor',
    openedBy: {...u}, openedShift: u.shift, firstGoodAt: null, closedAt: null, reason: '',
    entries: [], locks: [], releases: [], release: null, acknowledgments: [],
    sourceDecisions: [], includedLotoHold: false,
    previousEventId: previous?.id ?? null, repeatOf: null, reopenedBy: null
  };
  s.events.push(e);
  reconcileRepeats(s);
  return e;
}
export const downtime = (s, e) => Math.floor(((e.firstGoodAt ?? s.now) - e.stoppedAt) / 60000);
export const activeLocks = e => e.locks.filter(l => l.removedAt === null);

// REQ-06/09, F-01: applicability is explicit; no exclusion can hide lock history.
export function sourceDecision(e, source) {
  return e.sourceDecisions.filter(d => d.source === source).at(-1);
}
export function sourceApplicable(e, source) {
  return sourceDecision(e, source)?.applicable ?? true;
}
export function setSourceApplicable(s, e, u, source, applicable, reason = '') {
  editable(e);
  role(u, ['Shift Supervisor']);
  need(e.firstGoodAt === null, 'Isolation decisions are fixed after first good part.');
  need(machine(s, e.machineId).energySources.includes(source), 'Unknown energy source');
  need(typeof applicable === 'boolean', 'Choose Applicable or Not applicable.');
  need(applicable || String(reason).trim(), 'A reason is required to exclude an energy source.');
  need(applicable || !e.locks.some(l => l.source === source), 'Cannot exclude a source with recorded lock history.');
  const decision = {source, applicable, reason: String(reason).trim(), ...stamp(s, u)};
  e.sourceDecisions.push(decision);
  e.release = null;
  return decision;
}
export function isolationMissing(s, e, phase = 'release') {
  if (!e.includedLotoHold) return [];
  const missing = [];
  for (const source of machine(s, e.machineId).energySources) {
    if (sourceApplicable(e, source) && !e.locks.some(l => l.source === source)) {
      missing.push(`Applicable source not recorded – ${source}`);
    }
  }
  for (const l of e.locks) {
    const tag = `${l.source} (${l.id})`;
    if (!l.appliedBy?.name || !Number.isFinite(l.appliedAt)) missing.push(`Application identity/time – ${tag}`);
    if (!l.zeroEnergy || !l.verifiedBy?.name || !Number.isFinite(l.verifiedAt)) {
      missing.push(`Zero-energy verification identity/time – ${tag}`);
    }
    if (phase !== 'handover' && (l.removedAt === null || !l.removedBy?.name)) missing.push(`Lock removal – ${tag}`);
    if (l.appliedAt < e.stoppedAt ||
        (l.verifiedAt !== null && l.verifiedAt < l.appliedAt) ||
        (l.removedAt !== null && (l.removedAt < l.appliedAt || (l.verifiedAt !== null && l.removedAt < l.verifiedAt)))) {
      missing.push(`Invalid isolation chronology – ${tag}`);
    }
  }
  return missing;
}
export const releaseBlocked = e => e.includedLotoHold && (activeLocks(e).length > 0 || !e.release);
export function setReason(s, e, u, value) {
  editable(e); role(u, ['Technician']);
  need(REASONS.includes(value), 'Select a listed reason code.');
  e.reason = value; reconcileRepeats(s);
}
// REQ-02/06, F-02: check event time as well as permission at recording time.
export function confirmGood(s, e, u, at = s.now) {
  editable(e); role(u, ['Operator']);
  need(e.firstGoodAt === null, 'First good part is already recorded.');
  need(Number.isFinite(at) && at >= e.stoppedAt, 'First good part cannot precede stop time.');
  need(at <= s.now, 'First good part cannot be in the future.');
  need(!releaseBlocked(e), 'Release not authorized');
  if (e.includedLotoHold) {
    const missing = isolationMissing(s, e);
    need(!missing.length, `Missing: ${missing.join('; ')}`);
    need(at >= e.release.at && e.locks.every(l => at >= l.removedAt), 'First good part cannot precede lock removal or authorized release.');
  }
  e.firstGoodAt = at; e.firstGoodBy = {...u}; reconcileRepeats(s);
}
export function closeMissing(e, s) {
  return [
    ...(!e.reason ? ['Reason code'] : []),
    ...(!Number.isFinite(e.stoppedAt) ? ['Stop time'] : []),
    ...(e.firstGoodAt === null ? ['First good part'] : []),
    ...(s ? isolationMissing(s, e) : []),
    ...(releaseBlocked(e) ? ['Lockout not released'] : [])
  ];
}
export function closeEvent(s, e, u) {
  editable(e); role(u, ['Technician']);
  const missing = closeMissing(e, s);
  need(!missing.length, `Missing: ${missing.join('; ')}`);
  e.closedAt = s.now; e.closedBy = {...u}; reconcileRepeats(s);
}
export function applyLock(s, e, u, source) {
  editable(e); role(u, ['Technician']);
  need(e.firstGoodAt === null, 'Report a new stop before applying new locks.');
  need(machine(s, e.machineId).energySources.includes(source), 'Unknown energy source');
  need(sourceApplicable(e, source), 'Supervisor must mark this source Applicable before locking it.');
  need(!activeLocks(e).some(l => l.source === source), 'Lock already applied');
  const l = {id: id(s), source, appliedBy: {...u}, appliedAt: s.now, zeroEnergy: false,
    verifiedBy: null, verifiedAt: null, removedBy: null, removedAt: null};
  e.locks.push(l); e.includedLotoHold = true; e.release = null; return l;
}
function lockFor(e, lockId) {
  const l = e.locks.find(l => l.id === lockId);
  need(l && l.removedAt === null, 'Active lock not found; removed locks cannot be retrospectively verified.');
  return l;
}
export function verifyZero(s, e, u, lockId) {
  editable(e); role(u, ['Technician']);
  const l = lockFor(e, lockId);
  need(!l.zeroEnergy, 'Zero energy is already verified');
  need(s.now >= l.appliedAt, 'Verification cannot precede application.');
  l.zeroEnergy = true; l.verifiedBy = {...u}; l.verifiedAt = s.now;
}
export function removeLock(s, e, u, lockId) {
  editable(e); role(u, ['Technician']);
  const l = lockFor(e, lockId);
  need(s.now >= (l.verifiedAt ?? l.appliedAt), 'Removal cannot precede recorded isolation.');
  // Capture actual removal even when prior verification is missing. Never invent evidence.
  l.removedBy = {...u}; l.removedAt = s.now;
}
export function authorizeRelease(s, e, u) {
  editable(e); role(u, ['Shift Supervisor']);
  need(e.includedLotoHold, 'No lockout requires release');
  need(!e.release, 'Release already authorized');
  const missing = isolationMissing(s, e);
  need(!missing.length, `Missing: ${missing.join('; ')}`);
  need(e.locks.every(l => l.removedAt <= s.now), 'Release cannot precede lock removal.');
  e.release = stamp(s, u); e.releases.push(e.release);
}
// REQ-04/05: note capture and provenance remain unchanged.
export function addEntry(s, e, u, fields) {
  editable(e); role(u, ['Technician']);
  const data = Object.fromEntries(['found', 'tested', 'temporary', 'next'].map(k => [k, String(fields[k] ?? '').trim()]));
  need(Object.values(data).some(Boolean) || fields.photo, 'Add text or a photo.');
  const entry = {...data, photo: fields.photo ?? null, ...stamp(s, u)};
  e.entries.push(entry); return entry;
}
export function summary(e) {
  return {
    next: [...e.entries].reverse().find(n => n.next)?.next || 'No next action recorded',
    tested: e.entries.filter(n => n.tested).map(n => n.tested),
    people: [...new Set([...e.entries.map(n => n.user.name), ...e.locks.flatMap(l => [l.appliedBy.name, l.removedBy?.name, l.verifiedBy?.name].filter(Boolean))])],
    last: e.entries.at(-1)?.user.name || e.openedBy.name,
    shift: e.entries.at(-1)?.shift || e.openedShift
  };
}
// REQ-07, F-04: notes cannot satisfy responsibility acceptance.
function isolationFingerprint(e) {
  return JSON.stringify({locks: e.locks, sourceDecisions: e.sourceDecisions});
}
export function handover(s, e) {
  const sh = shiftAt(s.now), prior = e.closedAt === null && e.stoppedAt < sh.start;
  const fingerprint = isolationFingerprint(e);
  const ack = [...e.acknowledgments].reverse().find(a => a.shiftStart === sh.start && a.isolationFingerprint === fingerprint);
  const changed = prior && !ack && e.acknowledgments.some(a => a.shiftStart === sh.start);
  return {prior, ack, label: ack ? 'Acknowledged' : prior ?
    (s.now - sh.start >= 30 * 60000 ? 'Not acknowledged' : changed ? 'Reacknowledgment required' : 'Awaiting acknowledgment') : 'Current shift',
    overdue: prior && !ack && s.now - sh.start >= 30 * 60000};
}
export function acknowledge(s, e, u) {
  editable(e); role(u, ['Technician', 'Shift Supervisor']);
  const sh = shiftAt(s.now), h = handover(s, e);
  need(u.shift === sh.name, 'Select a user on the current clock shift.');
  need(h.prior, 'No previous-shift handover to acknowledge.');
  need(!h.ack, 'Already acknowledged the current isolation state this shift');
  const missing = isolationMissing(s, e, 'handover');
  need(!missing.length, `Missing: ${missing.join('; ')}`);
  const a = {...stamp(s, u), shiftStart: sh.start, isolationFingerprint: isolationFingerprint(e),
    locks: activeLocks(e).map(l => ({source: l.source, applier: l.appliedBy.name}))};
  e.acknowledgments.push(a); return a;
}
// REQ-08, F-03/F-05: establish full operating evidence before claiming verification.
function nextFullShift(at) {
  const sh = shiftAt(at);
  return at === sh.start ? sh : shiftAt(sh.end);
}
export function verificationEvidence(s, e) {
  if (e.firstGoodAt === null) return {kind: 'stopped', label: 'Awaiting evidence — production not resumed'};
  const subsequent = s.events.filter(n => n.machineId === e.machineId && n.id !== e.id &&
    n.stoppedAt >= e.firstGoodAt && s.events.indexOf(n) > s.events.indexOf(e)).sort((a, b) => a.stoppedAt - b.stoppedAt);
  let resume = e.firstGoodAt, candidate = nextFullShift(resume), interrupted = false;
  const relevant = [];
  for (const n of subsequent) {
    // A stop at the end cannot invalidate a completed operating shift.
    if (n.stoppedAt >= candidate.end) break;
    relevant.push(n);
    interrupted = true;
    if (n.firstGoodAt === null) {
      const unknown = relevant.some(n => !n.reason);
      const repeat = e.reason && relevant.find(n => n.reason === e.reason);
      return {kind: repeat ? 'repeat' : unknown || !e.reason ? 'pending' : 'interrupted', repeat,
        label: repeat ? 'Reopened – repeat fault' : unknown || !e.reason ? 'Awaiting evidence — uncoded stop or repair' : 'No matching recurrence observed — awaiting a full operating shift'};
    }
    resume = n.firstGoodAt;
    candidate = nextFullShift(resume);
    // A zero-duration stop at the exact shift start still interrupts that shift.
    if (n.stoppedAt === candidate.start) candidate = shiftAt(candidate.end);
  }
  const repeat = e.reason && relevant.find(n => n.reason === e.reason);
  if (repeat) return {kind: 'repeat', repeat, candidate, label: 'Reopened – repeat fault'};
  if (!e.reason || relevant.some(n => !n.reason)) return {kind: 'pending', candidate, label: 'Awaiting evidence — uncoded stop or repair'};
  if (s.now >= candidate.end) return {kind: 'verified', candidate, label: `Verified – recorded full ${candidate.name} shift`};
  return {kind: interrupted ? 'interrupted' : 'pending', candidate,
    label: interrupted ? 'No matching recurrence observed — awaiting a full operating shift' : 'Awaiting evidence — full operating shift pending'};
}
export function reconcileRepeats(s) {
  for (const e of s.events) { e.repeatOf = null; e.reopenedBy = null; }
  for (const e of s.events) {
    const result = verificationEvidence(s, e);
    if (result.repeat) { e.reopenedBy = result.repeat.id; result.repeat.repeatOf = e.id; }
  }
}
export function verification(s, e) {
  const evidence = verificationEvidence(s, e);
  if (evidence.kind === 'repeat' || e.firstGoodAt === null) return evidence.label;
  return e.closedAt === null ? 'Awaiting closeout' : evidence.label;
}
export function advanceClock(s, to) {
  need(Number.isFinite(to) && to >= s.now, 'Demo clock can only advance.');
  s.now = to; reconcileRepeats(s);
}
