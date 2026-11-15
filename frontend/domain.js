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
export const openFor=(s,machineId)=>s.events.find(e=>e.machineId===machineId&&e.closedAt===null);
const editable=e=>need(e.closedAt===null,'This event is closed and read-only.');
const role=(u,roles)=>need(roles.includes(u.role),`Requires ${roles.join(' or ')} role.`);
const stamp=(s,u)=>({user:{...u},at:s.now,shift:u.shift});
// REQ-01–03
export function openEvent(s,machineId,source,u){
 const m=machine(s,machineId);need(source==='manual'||source==='sensor','Unknown stop source');
 if(source==='sensor')need(m.sensors,'This machine has no sensors; use Report stop.');else role(u,['Technician','Operator']);
 const existing=openFor(s,machineId);if(existing)return existing;
 const e={id:id(s),machineId,stoppedAt:s.now,source:source==='sensor'?'sensor':m.sensors?'manual':'manual – no sensor',openedBy:{...u},openedShift:u.shift,firstGoodAt:null,closedAt:null,reason:'',entries:[],locks:[],releases:[],release:null,acknowledgments:[],includedLotoHold:false,repeatOf:null,reopenedBy:null};s.events.push(e);return e;
}
export const downtime=(s,e)=>Math.floor(((e.firstGoodAt??s.now)-e.stoppedAt)/60000);
export function setReason(s,e,u,value){editable(e);role(u,['Technician']);need(REASONS.includes(value),'Select a listed reason code.');e.reason=value;reconcileRepeats(s);}
export function activeLocks(e){return e.locks.filter(l=>l.removedAt===null);}
export const releaseBlocked=e=>e.includedLotoHold&&(activeLocks(e).length>0||!e.release);
export function confirmGood(s,e,u,at=s.now){editable(e);role(u,['Operator']);need(e.firstGoodAt===null,'First good part is already recorded.');need(Number.isFinite(at)&&at>=e.stoppedAt,'First good part cannot precede stop time.');need(at<=s.now,'First good part cannot be in the future.');need(!releaseBlocked(e),'Release not authorized');e.firstGoodAt=at;e.firstGoodBy={...u};}
export function closeMissing(e){return [...(!e.reason?['Reason code']:[]),...(!Number.isFinite(e.stoppedAt)?['Stop time']:[]),...(e.firstGoodAt===null?['First good part']:[]),...(releaseBlocked(e)?['Lockout not released']:[])];}
export function closeEvent(s,e,u){editable(e);role(u,['Technician']);const missing=closeMissing(e);need(!missing.length,`Missing: ${missing.join('; ')}`);e.closedAt=s.now;e.closedBy={...u};reconcileRepeats(s);}
// REQ-06/09: guards live here as well as the UI.
export function applyLock(s,e,u,source){editable(e);role(u,['Technician']);need(e.firstGoodAt===null,'Close the completed event and report a new stop before applying new locks.');need(machine(s,e.machineId).energySources.includes(source),'Unknown energy source');need(!activeLocks(e).some(l=>l.source===source),'Lock already applied');
 const l={id:id(s),source,appliedBy:{...u},appliedAt:s.now,zeroEnergy:false,verifiedBy:null,verifiedAt:null,removedBy:null,removedAt:null};e.locks.push(l);e.includedLotoHold=true;e.release=null;return l;}
function lockFor(e,lockId){const l=e.locks.find(l=>l.id===lockId);need(l&&l.removedAt===null,'Active lock not found');return l;}
export function verifyZero(s,e,u,lockId){editable(e);role(u,['Technician']);const l=lockFor(e,lockId);need(!l.zeroEnergy,'Zero energy is already verified');l.zeroEnergy=true;l.verifiedBy={...u};l.verifiedAt=s.now;}
export function removeLock(s,e,u,lockId){editable(e);role(u,['Technician']);const l=lockFor(e,lockId);l.removedBy={...u};l.removedAt=s.now;}
export function authorizeRelease(s,e,u){editable(e);role(u,['Shift Supervisor']);need(e.includedLotoHold,'No lockout requires release');need(!e.release,'Release already authorized');const active=activeLocks(e);need(!active.length,`Locks still applied: ${active.map(l=>l.source).join(', ')}`);e.release=stamp(s,u);e.releases.push(e.release);}
// REQ-04/05/07/09
export function addEntry(s,e,u,fields){editable(e);role(u,['Technician']);const data=Object.fromEntries(['found','tested','temporary','next'].map(k=>[k,String(fields[k]??'').trim()]));need(Object.values(data).some(Boolean)||fields.photo,'Add text or a photo.');const entry={...data,photo:fields.photo??null,...stamp(s,u)};e.entries.push(entry);return entry;}
export function summary(e){const entries=e.entries;return {next:[...entries].reverse().find(n=>n.next)?.next||'No next action recorded',tested:entries.filter(n=>n.tested).map(n=>n.tested),people:[...new Set([...entries.map(n=>n.user.name),...e.locks.flatMap(l=>[l.appliedBy.name,l.removedBy?.name,l.verifiedBy?.name].filter(Boolean))])],last:entries.at(-1)?.user.name||e.openedBy.name,shift:entries.at(-1)?.shift||e.openedShift};}
function workTime(e){return Math.max(e.stoppedAt,...e.entries.map(n=>n.at),...e.locks.map(l=>l.appliedAt));}
export function handover(s,e){const sh=shiftAt(s.now),prior=workTime(e)<sh.start;const ack=e.acknowledgments.find(a=>a.shiftStart===sh.start);return {prior,ack,label:ack?'Acknowledged':prior?(s.now-sh.start>=30*60000?'Not acknowledged':'Awaiting acknowledgment'):'Current shift',overdue:prior&&!ack&&s.now-sh.start>=30*60000};}
export function acknowledge(s,e,u){editable(e);role(u,['Technician','Shift Supervisor']);const sh=shiftAt(s.now);need(u.shift===sh.name,'Select a user on the current clock shift.');const h=handover(s,e);need(h.prior,'No previous-shift handover to acknowledge.');need(!h.ack,'Already acknowledged this shift');const missing=activeLocks(e).filter(l=>!l.zeroEnergy);need(!missing.length,`Missing: ${missing.map(l=>`Zero-energy verification – ${l.source}`).join('; ')}`);const a={...stamp(s,u),shiftStart:sh.start,locks:activeLocks(e).map(l=>({source:l.source,applier:l.appliedBy.name}))};e.acknowledgments.push(a);return a;}
// REQ-08: repeat links preserve one-open-event invariant and original closure record.
export function reconcileRepeats(s){for(const e of s.events){e.repeatOf=null;e.reopenedBy=null;}for(const e of s.events){if(e.closedAt===null)continue;const repeat=s.events.filter(n=>n.machineId===e.machineId&&n.stoppedAt>=e.closedAt&&n.id!==e.id&&n.stoppedAt<verificationEnd(e.firstGoodAt)&&n.reason&&n.reason===e.reason).sort((a,b)=>a.stoppedAt-b.stoppedAt)[0];if(repeat){e.reopenedBy=repeat.id;repeat.repeatOf=e.id;}}}
export function verification(s,e){if(e.closedAt===null)return 'Not yet closed';if(e.reopenedBy)return 'Reopened – repeat fault';const end=verificationEnd(e.firstGoodAt);const pending=s.events.some(n=>n.id!==e.id&&n.machineId===e.machineId&&n.stoppedAt>=e.closedAt&&n.stoppedAt<end&&!n.reason);return s.now>=end&&!pending?`Verified – ran full ${shiftAt(end-1).name} shift`:'Awaiting verification';}
export function advanceClock(s,to){need(Number.isFinite(to)&&to>=s.now,'Demo clock can only advance.');s.now=to;reconcileRepeats(s);}
