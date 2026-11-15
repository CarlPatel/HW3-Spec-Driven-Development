"""Interview-derived goals. Evidence keys resolve to timestamped source utterances.

IDs are globally unique across individual models. The combined model retains the
canonical ID when merging duplicates; ALIASES records every retired ID.
AI-generated draft, November 4, 2026. Review against the supplied interviews.
"""

GOALS = {}


def g(n, stakeholder, kind, category, text, evidence, agent=None, inferred=False):
    GOALS[f"G-{n}"] = dict(id=f"G-{n}", stakeholder=stakeholder, kind=kind,
        category=category, text=text, evidence=evidence.split(), agent=agent,
        inferred=inferred)


# T0 = initial Teo interview; T1/T2 = Teo follow-ups; A = Angela; R = Rob.
# Evidence references are the stakeholder's UTC speech timestamp, not an
# interviewer's suggestion. These are paraphrases, never verbatim quotations.
g(1,'Teo','Soft','non-functional','Reduce production lost while diagnosing and repairing press faults','T0@01:04:46.785 T2@01:34:41.523')
g(2,'Teo','Soft','non-functional','Minimize effort and interruption when recording work on a noisy floor with gloves','T0@01:00:17.854 T1@01:17:43.870 T2@01:35:01.447')
g(3,'Teo','Achieve','functional','Mechanic obtains evidence to distinguish a heater fault from other faults','T0@00:59:52.304 T2@01:30:04.038')
g(4,'Teo','Achieve','functional','Tablet displays live actual temperature, setpoint, and normal range for the selected press','T0@01:00:17.854 T1@01:15:07.221','Maintenance system')
g(5,'Teo','Achieve','functional','Mechanic compares temperature, part quality, and heater cycling before diagnosing the fault','T0@00:59:52.304 T1@01:14:44.345','Mechanic')
g(6,'Teo','Achieve','functional','Shared repair record explains the fault, intervention, and verification for the next shift','T2@01:31:36.166 T2@01:34:15.324')
g(7,'Teo','Achieve','functional','Repair record identifies the asset, fault symptoms, and last fault code','T2@01:31:05.537 T2@01:32:31.268','Mechanic')
g(8,'Teo','Achieve','functional','Repair record contains actual temperature and setpoint','T0@01:04:05.776 T2@01:31:05.537','Mechanic')
g(9,'Teo','Achieve','functional','Repair record states tests, corrective action, installed part number, and verification result','T0@01:04:05.776 T2@01:31:05.537 T2@01:32:31.268','Mechanic')
g(10,'Teo','Achieve','functional','Fault and change are captured before the mechanic moves on','T1@01:15:57.589 T1@01:17:43.870','Mechanic')
g(11,'Teo','Achieve','functional','Mechanic attaches quick evidence without typing the entire account','T0@01:00:17.854 T1@01:15:07.221')
g(12,'Teo','Achieve','functional','Mechanic attaches a photo of the finding','T0@01:00:17.854','Mechanic')
g(13,'Teo','Achieve','functional','Mechanic attaches a short voice note of the finding','T0@01:00:17.854','Mechanic')
g(14,'Teo','Achieve','functional','Mechanic retrieves earlier troubleshooting to avoid repeating checks','T0@01:02:46.799 T2@01:31:36.166')
g(15,'Teo','Achieve','functional','Mechanic reads the shift handoff and open fault history','T0@01:02:46.799 T2@01:31:36.166','Mechanic')
g(16,'Teo','Achieve','functional','Mechanic retrieves closed work orders and recorded part numbers from CMMS','T0@01:03:15.310','Mechanic')
g(17,'Teo','Achieve','functional','Mechanic locates a suitable replacement part without hunting through bins','T2@01:32:31.268')
g(18,'Teo','Achieve','functional','Parts view provides exact part number, stock quantity, crib location, and approved substitutes','T2@01:32:31.268','Maintenance system')
g(19,'Teo','Achieve','functional','Press repair includes isolation confirmation, corrective work, and a verification run','T2@01:30:30.890')
g(20,'Teo','Maintain','non-functional','Press is stopped and lockout/tagout is confirmed before the mechanic opens equipment','T2@01:30:30.890','Mechanic')
g(21,'Teo','Achieve','functional','Tablet records the confirmed safety check at the machine','T2@01:30:30.890','Mechanic')
g(22,'Teo','Achieve','functional','Mechanic checks connections, replaces the weak band, and verifies stable temperature and good parts','T2@01:30:30.890 T2@01:33:22.867','Mechanic')
g(23,'Teo','Avoid','non-functional','Machine-specific personal working knowledge becomes company property by default','T2@01:31:05.537')
g(24,'Teo','Maintain','non-functional','Personal notes remain private unless the mechanic explicitly selects content to share','T2@01:31:05.537','Maintenance system',True)

g(25,'Angela','Soft','non-functional','Improve maintenance and production decisions using accurate facts across shifts','A@13:33:54.358 A@13:37:46.015')
g(26,'Angela','Achieve','functional','Incoming supervisor receives an unambiguous machine and open-work handover','A@13:34:52.902')
g(27,'Angela','Achieve','functional','Shift view shows machine status, work ownership, restoration estimate, and production impact','A@13:33:54.358 A@13:34:52.902','Maintenance system')
g(28,'Angela','Achieve','functional','Handover links downtime event, alarms, diagnosis, corrective action, and reason code','A@13:34:52.902','Maintenance system')
g(29,'Angela','Achieve','functional','Outgoing and incoming supervisors agree what to monitor and when to escalate','A@13:34:52.902','Shift supervisor')
g(30,'Angela','Maintain','non-functional','Completed maintenance records contain a reason and accurate downtime minutes','A@13:32:47.328 A@13:33:20.301')
g(31,'Angela','Maintain','functional','Work-order completion requires a reason code','A@13:33:20.301','Maintenance system')
g(32,'Angela','Achieve','functional','Supervisor sees missing reason codes and other required fields immediately','A@13:33:20.301 A@13:33:54.358','Maintenance system')
g(33,'Angela','Achieve','functional','Supervisor verifies downtime minutes against machine stop and first good part times','A@13:33:20.301','Shift supervisor')
g(34,'Angela','Achieve','functional','Supervisor identifies critical machines from bottleneck, backup, cell, downtime, and quality impact','A@13:31:57.701','Shift supervisor')
g(35,'Angela','Achieve','functional','Unresolved maintenance issues receive an escalation when required','A@13:35:19.832')
g(36,'Angela','Achieve','functional','Issue is escalated if [restoration target exceeded, critical equipment affected, or safety or quality at risk]','A@13:35:19.832','Shift supervisor')
g(37,'Angela','Achieve','functional','Escalation record identifies owner, time, reason, and next action','A@13:35:19.832','Shift supervisor')
g(38,'Angela','Maintain','non-functional','Equipment is released only with complete safety documentation and release authority','A@13:35:53.834 A@13:36:11.712')
g(39,'Angela','Achieve','functional','Repair record contains lockout/tagout status, hazard assessment, and release authority','A@13:35:53.834','Mechanic')
g(40,'Angela','Achieve','functional','Safety-part repair is traceable to failure mode, technician, parts, action, inspection, and restart approver','A@13:35:53.834','Maintenance system')
g(41,'Angela','Maintain','non-functional','Safety hold remains if [required release documentation is incomplete], despite production pressure','A@13:36:11.712 A@13:36:49.533','Shift supervisor')
g(42,'Angela','Achieve','functional','Supervisor assigns an owner to each missing release item and sees the hold clearly','A@13:37:14.563','Shift supervisor')
g(43,'Angela','Soft','non-functional','Reduce production waiting for maintenance restoration','A@13:34:16.376 A@13:36:49.533','Production supervisor')
g(44,'Angela','Achieve','functional','Equipment and shift view ties downtime, root cause, ownership, and impact across all three shifts','A@13:37:46.015 A@13:38:09.416','Maintenance system')
g(45,'Angela','Avoid','non-functional','Personnel are penalized for stopping an unsafe restart in accordance with procedure','A@13:37:14.563','Plant management')

g(46,'Rob','Soft','non-functional','Minimize maintenance injuries and demonstrate safe work during inspections','R@17:29:34.313 R@17:47:27.669')
g(47,'Rob','Maintain','non-functional','Hazard controls and release records are verified before equipment returns to service','R@17:31:15.628 R@17:33:39.894')
g(48,'Rob','Achieve','functional','Safety coordinator assesses hazard, active alarms, isolation, and applicable work permits','R@17:30:09.217 R@17:32:26.552','Safety coordinator')
g(49,'Rob','Achieve','functional','Isolation record states equipment, isolation points, each lock applier, date/time, and release authorizer and performer','R@17:44:38.682','Mechanic')
g(50,'Rob','Achieve','functional','Return-to-service authorization and technician/supervisor acknowledgments are recorded before release','R@17:31:15.628 R@17:44:38.682','Shift supervisor')
g(51,'Rob','Achieve','functional','Supervisor validates hazard controls before closeout','R@17:31:15.628','Shift supervisor')
g(52,'Rob','Maintain','non-functional','Equipment stays unreleased if [isolation, alarm, permit, or hazard fields are blank or a hazard is unresolved]','R@17:33:39.894 R@17:50:15.782','Shift supervisor')
g(53,'Rob','Achieve','functional','Incoming supervisor acknowledges a digital handoff with all critical fields completed','R@17:33:39.894','Shift supervisor')
g(54,'Rob','Achieve','functional','Work order retains permits, photos, alarm information, replaced parts, and release decision','R@17:33:12.862 R@17:44:38.682','Maintenance system')
g(55,'Rob','Maintain','non-functional','Record corrections preserve who changed what and when','R@17:44:38.682 R@17:49:15.529','Maintenance system')
g(56,'Rob','Achieve','functional','Inspector can retrieve complete equipment maintenance and safety history without chasing people','R@17:47:27.669')
g(57,'Rob','Maintain','functional','Maintenance, permit, handoff, and sensor records include a consistent equipment identifier and time window','R@17:48:39.537','Maintenance system')
g(58,'Rob','Achieve','functional','Equipment record joins maintenance, isolation, alarms, permits, and corrective-action history','R@17:48:39.537','Maintenance system')
g(59,'Rob','Maintain','non-functional','Records remain readable and retrievable for the inspection period despite retirement or staff changes','R@17:49:15.529','Maintenance system')
g(60,'Rob','Achieve','functional','Safety coordinator exports inspectable records without granting access to the entire operating system','R@17:49:15.529','Safety coordinator')
g(61,'Rob','Achieve','functional','Near misses are recorded, acknowledged, reviewed, and followed through','R@17:45:20.933 R@17:46:57.049')
g(62,'Rob','Achieve','functional','Named reporter records what happened, where, when, and who within 24 hours of a near miss','R@17:34:09.701 R@17:45:20.933 R@17:45:57.392','Reporter')
g(63,'Rob','Achieve','functional','Supervisor acknowledges a near-miss report before its 24-hour deadline','R@17:45:20.933','Shift supervisor')
g(64,'Rob','Achieve','functional','Safety review considers facts and controls without punishing the reporter for speaking up','R@17:46:28.516','Safety coordinator')
g(65,'Rob','Achieve','functional','Corrective action has a named owner and verified completion','R@17:46:57.049','Safety coordinator')
g(66,'Rob','Achieve','functional','Separate environmental report is created if [a chemical spill occurs during maintenance]','R@17:34:09.701 R@17:44:38.682','Reporter')
g(67,'Rob','Avoid','non-functional','Tablet use distracts personnel around moving machinery','R@17:34:09.701','Mechanic')
g(68,'Rob','Maintain','non-functional','Safety-critical controls remain prominent and distinguishable from general maintenance notes','R@17:49:43.711 R@17:50:37.717','Maintenance system')
g(69,'Rob','Achieve','functional','Work is stopped and hazard documented if [an alarm indicates a hazard requiring investigation]','R@17:30:42.356 R@17:32:26.552','Shift supervisor')
g(70,'Rob','Achieve','functional','Safety coordinator reviews recurring alarms and failure modes for shutdown, action, or inspection','R@17:30:09.217 R@17:32:26.552','Safety coordinator')

# Explicit design interpretations: these are yellow in every generated view.
g(71,'Combined','Soft','non-functional','Improve safe maintenance continuity with usable, reliable cross-shift records','T2@01:34:41.523 A@13:37:46.015 R@17:29:34.313',inferred=True)
g(72,'Teo','Maintain','non-functional','Mechanic confirms voice-note content before it is published to the shared repair record','T0@01:00:17.854','Mechanic',True)
g(73,'Combined','Maintain','non-functional','A release request is rejected and missing items shown if [the safety-release checks are not all satisfied]','A@13:36:11.712 R@17:33:39.894','Maintenance system',True)
g(74,'Combined','Maintain','non-functional','Capture uses a safe stationary interaction point if [machinery is moving nearby]','R@17:34:09.701 T1@01:17:43.870','Mechanic',True)
g(75,'Combined','Achieve','functional','System flags missing or stale telemetry if [a current temperature reading cannot be obtained]','T0@01:00:17.854','Maintenance system',True)
g(76,'Combined','Achieve','functional','Required shared repair facts are recorded without automatically copying personal notebook content','T2@01:31:05.537 R@17:44:38.682','Mechanic',True)
g(77,'Combined','Achieve','functional','Safety coordinator configures the applicable inspection retention period before records are scheduled for disposal','R@17:49:15.529','Safety coordinator',True)

# (parent, [children], heuristic/pattern code, complete).
# Separate refinement objects of one parent are OR alternatives. Members of
# one refinement are AND-conjuncts. Most real-world/soft refinements are partial.
TEO = [
 (1,[3,6,14,17,19],'H4',False), (2,[10,11],'H6',False),
 (3,[4,5],'H5',False), (6,[7,8,9],'P5',False),
 (11,[12],'P2',True), (11,[13,72],'P2',True),
 (14,[15,16],'P5',False), (17,[18],'H11',False),
 (19,[20,21,22],'P1',False), (23,[24],'H8',False),
]
ANGELA = [
 (25,[26,30,34,35,38,44],'H3',False),
 (26,[27,28,29],'P5',False), (30,[31,32,33],'H4',False),
 (35,[36,37],'H11',True), (38,[39,40,41,42],'P4',False),
]
ROB = [
 (46,[47,56,61,66,67,68,69,70],'H7',False),
 (47,[48,49,50,51,52,53,54],'H5',False),
 (56,[57,58,55,59,60],'P5',False),
 (61,[62,63,64,65],'P1',False),
]

# Manual duplicate reconciliation. Keep the ID on the right, and retain all
# original evidence. This is NOT string matching or automatic deduplication.
ALIASES = {'G-43':'G-1', 'G-28':'G-6', 'G-47':'G-38', 'G-52':'G-41'}
MERGED_TEXT = {
 'G-1': 'Reduce production lost while diagnosing, repairing, and restoring faulty equipment',
 'G-6': 'Shared handover links asset fault, downtime, alarms, diagnosis, corrective action, reason code, parts, and verification',
 'G-38': 'Hazard controls and complete safety records are verified and release is authorized before equipment returns to service',
 'G-41': 'Equipment stays on hold if [release documentation or isolation, alarm, permit, or hazard fields are incomplete, or hazards remain unresolved]',
}

COMBINED_EXTRA = [
 (71,[1,2,25,46,23],'H12',False),
 (3,[75],'P6',False),
 (38,[73],'H8',False),
 (67,[74],'H4',False),
 (23,[76],'H5',False),
 (59,[77],'H4',False),
]

# These are conditional tensions rather than a claim that safety and speed
# are inherently incompatible. See review/analysis.md for conditions/mitigations.
CONFLICTS = [('G-2','G-38'), ('G-2','G-67'), ('G-23','G-6')]
