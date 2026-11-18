import {test} from 'node:test';
import assert from 'node:assert/strict';
import * as D from '../frontend/domain.js';
const at=(h,m=0,day=15)=>+new Date(2026,10,day,h,m);
const [teo,maya,,op,sup]=D.USERS;
const setup=(t=at(2,14),machine='p17')=>{const s=D.createState(t,false);return [s,D.openEvent(s,machine,'manual',teo)];};
function code(s,e,reason='Hydraulic'){D.setReason(s,e,teo,reason);}
function finish(s,e,time=s.now){D.confirmGood(s,e,op,time);code(s,e);D.closeEvent(s,e,teo);}
function isolation(s,e){return D.machine(s,e.machineId).energySources.map(source=>{const l=D.applyLock(s,e,teo,source);D.verifyZero(s,e,teo,l.id);return l;});}
function release(s,e){for(const l of D.activeLocks(e))D.removeLock(s,e,maya,l.id);D.authorizeRelease(s,e,sup);}

test('REQ-01: no-field sensor/manual stops and active interval deduplication',()=>{
 const [s,e]=setup();assert.equal(D.openEvent(s,'p17','sensor',teo),e);assert.equal(s.events.length,1);
 const old=D.openEvent(s,'p3','manual',teo);assert.equal(old.source,'manual – no sensor');
 assert.throws(()=>D.openEvent(s,'p3','sensor',teo),/no sensors/);
});
test('REQ-02: running/frozen whole minutes and invalid timestamp refusals',()=>{
 const [s,e]=setup();D.advanceClock(s,at(2,44));assert.equal(D.downtime(s,e),30);
 assert.throws(()=>D.confirmGood(s,e,op,at(2,10)),/precede/);assert.throws(()=>D.confirmGood(s,e,op,at(3)),/future/);
 D.advanceClock(s,at(3,2));D.confirmGood(s,e,op);D.advanceClock(s,at(4));assert.equal(D.downtime(s,e),48);
});
test('REQ-03: fixed code list, missing fields and early code preservation',()=>{
 const [s,e]=setup();assert.throws(()=>D.closeEvent(s,e,teo),/Reason code; First good part/);
 assert.throws(()=>code(s,e,'free text'),/listed/);code(s,e);assert.throws(()=>D.closeEvent(s,e,teo),/First good part/);
 D.confirmGood(s,e,op);D.closeEvent(s,e,teo);assert.equal(e.reason,'Hydraulic');
});
test('F-01: removed unverified lock retains missing verifier evidence and blocks release/closeout',()=>{
 const [s,e]=setup(at(5),'p6');const l=D.applyLock(s,e,teo,'Electrical');D.removeLock(s,e,maya,l.id);
 assert.throws(()=>D.authorizeRelease(s,e,sup),/Zero-energy verification identity\/time/);
 assert.throws(()=>D.closeEvent(s,e,teo),/Zero-energy verification identity\/time/);
 assert.throws(()=>D.verifyZero(s,e,teo,l.id),/retrospectively/);
 assert.equal(l.zeroEnergy,false);assert.equal(l.appliedBy.name,teo.name);assert.equal(l.removedBy.name,maya.name);
});
test('F-01: applicable sources are required at handover and release',()=>{
 const [s,e]=setup(at(5));const l=D.applyLock(s,e,teo,'Hydraulic');D.verifyZero(s,e,teo,l.id);
 D.advanceClock(s,at(6,10));assert.throws(()=>D.acknowledge(s,e,maya),/Applicable source not recorded – Electrical/);
 D.removeLock(s,e,maya,l.id);assert.throws(()=>D.authorizeRelease(s,e,sup),/Electrical/);
});
test('F-01: only supervisor may exclude untouched source with explicit stamped reason',()=>{
 const [s,e]=setup();assert.throws(()=>D.setSourceApplicable(s,e,teo,'Electrical',false,'Not used'),/Shift Supervisor/);
 assert.throws(()=>D.setSourceApplicable(s,e,sup,'Electrical',false,'  '),/reason/);
 D.setSourceApplicable(s,e,sup,'Electrical',false,'Mechanical work; electrical outside mock task');
 assert.equal(D.sourceDecision(e,'Electrical').user.name,sup.name);
 const l=D.applyLock(s,e,teo,'Hydraulic');D.verifyZero(s,e,teo,l.id);release(s,e);D.confirmGood(s,e,op);
 assert.equal(e.sourceDecisions.length,1);assert.ok(e.release);
});
test('F-01: exclusion cannot hide history and excluded source cannot be locked',()=>{
 const [s,e]=setup();const l=D.applyLock(s,e,teo,'Hydraulic');D.removeLock(s,e,teo,l.id);
 assert.throws(()=>D.setSourceApplicable(s,e,sup,'Hydraulic',false,'Skip'),/recorded lock history/);
 D.setSourceApplicable(s,e,sup,'Electrical',false,'Not used');assert.throws(()=>D.applyLock(s,e,teo,'Electrical'),/Applicable/);
 D.setSourceApplicable(s,e,sup,'Electrical',true);D.applyLock(s,e,teo,'Electrical');
});
test('REQ-06/09: valid active isolation can be handed over; historical per-cycle completeness persists',()=>{
 const [s,e]=setup(at(5));const locks=isolation(s,e);D.advanceClock(s,at(6,10));
 const a=D.acknowledge(s,e,maya);assert.equal(a.locks.length,2);assert.equal(a.locks[0].applier,teo.name);
 assert.throws(()=>D.confirmGood(s,e,op),/Release/);assert.throws(()=>D.authorizeRelease(s,e,teo),/Shift Supervisor/);
 assert.throws(()=>D.authorizeRelease(s,e,sup),/Lock removal/);release(s,e);finish(s,e);
 assert.equal(locks[0].removedBy.name,maya.name);assert.ok(e.includedLotoHold);
});
test('F-02: production cannot precede release; equality is allowed',()=>{
 const [s,e]=setup(at(5));isolation(s,e);D.advanceClock(s,at(14));release(s,e);
 assert.throws(()=>D.confirmGood(s,e,op,at(12)),/cannot precede lock removal or authorized release/);
 D.confirmGood(s,e,op,at(14));assert.equal(e.firstGoodAt,at(14));
});
test('F-01/F-02: each relock cycle needs verification and invalidates release',()=>{
 const [s,e]=setup(at(5),'p6');isolation(s,e);release(s,e);const l=D.applyLock(s,e,teo,'Electrical');
 assert.equal(e.release,null);assert.equal(e.releases.length,1);D.removeLock(s,e,teo,l.id);
 assert.throws(()=>D.authorizeRelease(s,e,sup),/Zero-energy/);
});
test('F-03: new stop after good part is captured while reason/closure remain pending',()=>{
 const [s,e]=setup(at(6,55));D.advanceClock(s,at(7,10));D.confirmGood(s,e,op);D.advanceClock(s,at(7,25));
 const n=D.openEvent(s,'p17','sensor',teo);assert.notEqual(n.id,e.id);assert.equal(n.previousEventId,e.id);
 assert.equal(D.downtime(s,e),15);assert.equal(D.downtime(s,n),0);assert.equal(D.openEvent(s,'p17','sensor',teo),n);
 assert.equal(D.openRecords(s,'p17').length,2);assert.equal(D.activeFor(s,'p17'),n);
 code(s,e);D.closeEvent(s,e,teo);assert.equal(D.activeFor(s,'p17'),n);assert.equal(D.openFor(s,'p17'),n);
});
test('F-03/08: pending closeout participates in repeat classification independently of closure time',()=>{
 const [s,e]=setup();D.advanceClock(s,at(3,2));D.confirmGood(s,e,op);D.advanceClock(s,at(4));
 const n=D.openEvent(s,'p17','sensor',teo);code(s,n);code(s,e);assert.equal(e.reopenedBy,n.id);
 D.closeEvent(s,e,teo);assert.equal(D.verification(s,e),'Reopened – repeat fault');
});
test('REQ-04/05: photo-only entry, empty refusal, stamps and latest next-action summary',()=>{
 const [s,e]=setup();assert.throws(()=>D.addEntry(s,e,teo,{found:'  '}),/text or a photo/);
 const photo=D.addEntry(s,e,teo,{photo:'data:image/png;base64,AA=='});assert.equal(photo.at,s.now);assert.equal(photo.user.name,teo.name);
 D.addEntry(s,e,teo,{next:'Pressure test',tested:'Checked seal'});D.addEntry(s,e,maya,{found:'No leak'});
 assert.equal(D.summary(e).next,'Pressure test');assert.deepEqual(D.summary(e).tested,['Checked seal']);assert.equal(D.summary(e).last,maya.name);
});
test('F-04: overdue explicit handover persists across current-shift notes',()=>{
 const [s,e]=setup(at(5));D.advanceClock(s,at(6,29));assert.equal(D.handover(s,e).label,'Awaiting acknowledgment');
 D.advanceClock(s,at(6,30));assert.ok(D.handover(s,e).overdue);D.addEntry(s,e,maya,{found:'Starting work'});
 assert.equal(D.handover(s,e).label,'Not acknowledged');assert.equal(e.acknowledgments.length,0);
 assert.throws(()=>D.acknowledge(s,e,op),/Technician/);assert.throws(()=>D.acknowledge(s,e,teo),/current clock shift/);
 D.acknowledge(s,e,maya);assert.equal(D.handover(s,e).label,'Acknowledged');D.addEntry(s,e,maya,{next:'Inspect seal'});
 assert.equal(D.handover(s,e).label,'Acknowledged');D.advanceClock(s,at(14,30));assert.ok(D.handover(s,e).overdue);
});
test('F-04: critical isolation change requires reacknowledgment and retains previous snapshot',()=>{
 const [s,e]=setup(at(5),'p6');const [l]=isolation(s,e);D.advanceClock(s,at(6,10));D.acknowledge(s,e,maya);
 D.removeLock(s,e,maya,l.id);assert.equal(D.handover(s,e).label,'Reacknowledgment required');
 D.acknowledge(s,e,maya);assert.equal(e.acknowledgments.length,2);assert.equal(e.acknowledgments[0].locks.length,1);assert.equal(e.acknowledgments[1].locks.length,0);
});
test('REQ-07: dated midnight shifts and current-shift events have no inherited obligation',()=>{
 assert.equal(D.shiftAt(at(2)).start,at(22,0,14));const [s,e]=setup(at(6,31));assert.equal(D.handover(s,e).label,'Current shift');
});
test('REQ-08: full-shift boundaries and normal operating evidence',()=>{
 for(const [good,end] of [[at(3,2),at(14)],[at(6),at(14)],[at(6,1),at(22)],[at(22),at(6,0,16)]]){
 const [s,e]=setup(good);finish(s,e);D.advanceClock(s,end-1);assert.doesNotMatch(D.verification(s,e),/^Verified/);
 D.advanceClock(s,end);assert.match(D.verification(s,e),/^Verified – recorded full/);}
});
test('F-05: different-reason ongoing stop cannot establish a full operating shift',()=>{
 const [s,e]=setup(at(6));D.advanceClock(s,at(6,10));finish(s,e);D.advanceClock(s,at(7));
 const n=D.openEvent(s,'p17','sensor',teo);code(s,n,'Electrical/Heater');D.advanceClock(s,at(22,5));
 assert.equal(D.verificationEvidence(s,e).kind,'interrupted');assert.doesNotMatch(D.verification(s,e),/^Verified/);
 assert.match(D.verification(s,e),/No matching recurrence observed/);
});
test('F-05: unrelated stopped shift waits for resumption and next uninterrupted full shift',()=>{
 const [s,e]=setup(at(6));D.advanceClock(s,at(6,10));finish(s,e);D.advanceClock(s,at(7));
 const n=D.openEvent(s,'p17','sensor',teo);code(s,n,'Electrical/Heater');D.advanceClock(s,at(15));D.confirmGood(s,n,op);
 D.advanceClock(s,at(22));assert.doesNotMatch(D.verification(s,e),/^Verified/);D.advanceClock(s,at(6,0,16));
 assert.equal(D.verification(s,e),'Verified – recorded full Night shift');
});
test('F-05: matching recurrence after original interrupted deadline still reopens before evidence completes',()=>{
 const [s,e]=setup(at(6));D.advanceClock(s,at(6,10));finish(s,e);D.advanceClock(s,at(7));
 const n=D.openEvent(s,'p17','sensor',teo);code(s,n,'Electrical/Heater');D.advanceClock(s,at(15));D.confirmGood(s,n,op);
 D.advanceClock(s,at(23));const repeat=D.openEvent(s,'p17','sensor',teo);code(s,repeat);assert.equal(e.reopenedBy,repeat.id);
});
test('F-05: unknown classification stays pending; late matching reason retains stop time',()=>{
 const [s,e]=setup();D.advanceClock(s,at(3,2));finish(s,e);D.advanceClock(s,at(10,15));const n=D.openEvent(s,'p17','sensor',teo);
 D.advanceClock(s,at(15));assert.equal(D.verificationEvidence(s,e).kind,'pending');code(s,n);assert.equal(e.reopenedBy,n.id);assert.equal(n.repeatOf,e.id);
});
test('F-05: stop exactly at verification end does not invalidate completed operating shift',()=>{
 const [s,e]=setup();D.advanceClock(s,at(3,2));finish(s,e);D.advanceClock(s,at(14));const n=D.openEvent(s,'p17','sensor',teo);code(s,n);
 assert.equal(D.verification(s,e),'Verified – recorded full Day shift');assert.equal(e.reopenedBy,null);
});
test('F-05: correcting open reason recalculates repeat links without inventing operation',()=>{
 const [s,e]=setup();finish(s,e);D.advanceClock(s,at(7));const n=D.openEvent(s,'p17','sensor',teo);code(s,n);
 assert.ok(e.reopenedBy);code(s,n,'Mechanical');assert.equal(e.reopenedBy,null);assert.equal(n.repeatOf,null);
 D.advanceClock(s,at(15));assert.doesNotMatch(D.verification(s,e),/^Verified/);
});
test('REQ-01–09: closed mutation, role violations and backward clock remain refused',()=>{
 const [s,e]=setup();finish(s,e);assert.throws(()=>D.addEntry(s,e,teo,{next:'x'}),/read-only/);
 assert.throws(()=>code(s,e,'Other'),/read-only/);assert.throws(()=>D.advanceClock(s,s.now-1),/only advance/);
 const n=D.openEvent(s,'p6','manual',teo);assert.throws(()=>D.applyLock(s,n,op,'Electrical'),/Technician/);
 assert.throws(()=>D.confirmGood(s,n,teo),/Operator/);
});
