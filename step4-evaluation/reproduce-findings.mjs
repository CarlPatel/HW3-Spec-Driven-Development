// Reproduces observed V1 behavior; these assertions do NOT endorse it as correct.
// Run against the pinned snapshot with: node reproduce-findings.mjs
import assert from 'node:assert/strict';
import * as D from './source-snapshot/frontend/domain.js';
const at=(h,m=0)=>+new Date(2026,10,15,h,m);
const [teo,maya,,op,sup]=D.USERS;
const fresh=(time=at(2,14))=>{const s=D.createState(time,false);return [s,D.openEvent(s,'p17','sensor',teo)];};
const closed=()=>{const [s,e]=fresh();D.advanceClock(s,at(3,2));D.confirmGood(s,e,op);D.setReason(s,e,teo,'Hydraulic');D.closeEvent(s,e,teo);return [s,e];};
const observations=[];

{
 const [s,e]=fresh(); const lock=D.applyLock(s,e,teo,'Hydraulic');
 D.removeLock(s,e,teo,lock.id);D.authorizeRelease(s,e,sup);
 D.confirmGood(s,e,op);D.setReason(s,e,teo,'Hydraulic');D.closeEvent(s,e,teo);
 assert.equal(lock.zeroEnergy,false);assert.notEqual(e.closedAt,null);
 observations.push({id:'PROBE-01',finding:'F-01',observed:'An unverified lock record can be removed, released, and closed.',zeroEnergy:lock.zeroEnergy,closed:e.closedAt!==null});
}
{
 const [s,e]=fresh();const lock=D.applyLock(s,e,teo,'Hydraulic');D.verifyZero(s,e,teo,lock.id);
 D.advanceClock(s,at(3));D.removeLock(s,e,teo,lock.id);D.authorizeRelease(s,e,sup);
 D.confirmGood(s,e,op,at(2,30));
 assert.ok(e.firstGoodAt<e.release.at && e.firstGoodAt<lock.removedAt);
 observations.push({id:'PROBE-02',finding:'F-02',observed:'Stored first-good-part time can precede lock removal and release.',firstGoodPart:'02:30',lockRemoval:'03:00',release:'03:00'});
}
{
 const [s,e]=fresh();D.advanceClock(s,at(3,2));D.confirmGood(s,e,op);D.advanceClock(s,at(3,10));
 const second=D.openEvent(s,'p17','sensor',teo);assert.equal(second,e);assert.equal(s.events.length,1);assert.equal(D.downtime(s,e),48);
 observations.push({id:'PROBE-03',finding:'F-03',observed:'A stop after resumed production is absorbed into the not-yet-closed event; clock stays stopped.',events:s.events.length,retainedStop:'02:14',retainedFirstGoodPart:'03:02',ignoredNewStop:'03:10',downtime:48});
}
{
 const [s,e]=fresh(at(5));D.addEntry(s,e,teo,{next:'Pressure test'});D.advanceClock(s,at(6,30));
 const before=D.handover(s,e).label;assert.equal(before,'Not acknowledged');
 D.addEntry(s,e,maya,{found:'Pressure still needs checking'});const after=D.handover(s,e).label;
 assert.equal(after,'Current shift');assert.equal(e.acknowledgments.length,0);
 observations.push({id:'PROBE-04',finding:'F-04',observed:'A current-shift note erases the overdue handover state without an acknowledgment.',before,after,acknowledgments:e.acknowledgments.length});
}
{
 const [s,e]=closed();D.advanceClock(s,at(7));const other=D.openEvent(s,'p17','sensor',teo);D.setReason(s,other,teo,'Electrical/Heater');
 D.advanceClock(s,at(14));const label=D.verification(s,e);
 assert.equal(label,'Verified – ran full Day shift');assert.equal(other.firstGoodAt,null);assert.equal(other.closedAt,null);
 observations.push({id:'PROBE-05',finding:'F-05',observed:'Repair is labeled as having run a full shift although another ongoing stop covers that shift.',label,ongoingStop:'07:00',ongoingStopFirstGoodPart:other.firstGoodAt});
}
{
 const [s,e]=fresh(at(5));const lock=D.applyLock(s,e,teo,'Hydraulic');D.verifyZero(s,e,teo,lock.id);
 D.advanceClock(s,at(6,10));D.acknowledge(s,e,maya);D.removeLock(s,e,teo,lock.id);D.authorizeRelease(s,e,sup);
 assert.equal(e.locks.some(l=>l.source==='Electrical'),false);
 observations.push({id:'PROBE-06',finding:'F-01',observed:'Gates evaluate recorded/applied locks only, without a job-level required-source applicability decision.',machineSources:D.machine(s,'p17').energySources,recordedSources:e.locks.map(l=>l.source),releaseAuthorized:!!e.release});
}
console.log(JSON.stringify({baselineCommit:'bef8e6c0bfae46af486e561841c32f9c8d159b88',purpose:'Reproduce observed requirements gaps, not pass/fail claims of stakeholder satisfaction.',observations},null,2));
