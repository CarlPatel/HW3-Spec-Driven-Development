"""
Goal model for Rob Kessler (EHS - environment, health and safety; compliance).
Source: transcript-261026-2245.csv (timestamps below are 2026-10-27, UTC, HH:MM:SS).

Conventions
- Goal IDs G-75 .. G-114 (IDs are unique across all three stakeholder models).
- Goal label = Type[G-n: Name]. Conditions use "<b>If</b> [condition]".
- Refinement annotations carry only the heuristic (H3-H12) or pattern (P1-P7) code.
- Leaf goals are bold and assigned to exactly one agent.
- TACIT goals (not stated in the transcript; added by refinement or my own
  interpretation) are listed in TACIT and highlighted yellow in the diagram.
"""
from goalmodeling.schema import *

YELLOW = "fill:#fff59d"


def by(name, software=False):
    """Responsibility link from a leaf goal to a single agent."""
    kind = AgentType.SOFTWARE_AGENT if software else AgentType.ENVIRONMENT_AGENT
    return [PerformanceLink(Agent(name, kind), None)]


def build():
    # ================= Avoid injury (G-76 branch) =================
    # --- Lockout/tagout: apply (G-81) and its converse, release (G-82) ---
    # G-83..G-85 [02:27:46] "isolating every hazardous-energy source, applying a personal lock and tag,
    #            and verifying zero energy before work starts"
    g83 = AchieveGoal("G-83: AllHazardousEnergySourcesIsolated",
                      by("AuthorizedTechnician"), leaf=True)
    g84 = AchieveGoal("G-84: PersonalLockAndTagApplied",
                      by("AuthorizedTechnician"), leaf=True)
    g85 = AchieveGoal("G-85: ZeroEnergyVerified <b>If</b> LocksApplied",
                      by("AuthorizedTechnician"), leaf=True)
    # G-81 [02:27:46] lockout before work starts; milestones in the order Rob gave them.
    g81 = AchieveGoal("G-81: EquipmentLockedOut <b>If</b> ServiceRequired", None,
                      [Refinement(False, [g83, g84, g85], "P1")])

    # G-86 [02:36:59] "work only resumes after the hazard is corrected"
    g86 = AchieveGoal("G-86: HazardCorrectedAndInspected",
                      by("AuthorizedTechnician"), leaf=True)
    # G-87 [02:27:46] "who authorized and performed the release"
    #      Agent choice (shift supervisor) is my interpretation; Rob did not name the authorizer.
    g87 = AchieveGoal("G-87: ReleaseAuthorizedAndRecorded",
                      by("ShiftSupervisor"), leaf=True)
    # G-88 [02:27:11] "only released it after the proper lockout/tagout information was recorded"
    g88 = AvoidGoal("G-88: EquipmentReleased <b>If Not</b> LockRemovalAndReleaseRecorded",
                    by("MaintenanceTablet", True), leaf=True)
    # G-82 [02:36:59] "the responsible person records that the area and equipment were released safely"
    #      P4: guard (hazard corrected, release recorded) introduced before release.
    g82 = AchieveGoal("G-82: EquipmentReleasedSafely <b>If</b> ServiceComplete", None,
                      [Refinement(False, [g86, g87, g88], "P4")])

    # G-78 [02:26:34] "one failure in lockout/tagout can cause a life-changing injury"
    #      H9: converse of "locked out" (G-81) is "released safely" (G-82).
    g78 = MaintainGoal("G-78: HazardousEnergyControlledDuringService", None,
                       [Refinement(False, [g81, g82], "H9")])

    # --- Stop work on abnormal behaviour ---
    # G-92 [02:35:41] "The operator and the shift supervisor should be alerted first"
    g92 = AchieveGoal("G-92: OperatorAndSupervisorAlertedFirst <b>If</b> UnsafeCondition",
                      by("MaintenanceTablet", True), leaf=True)
    # G-93 [02:36:23] "I need immediate notification when the condition could seriously endanger someone"
    g93 = AchieveGoal("G-93: EHSNotifiedImmediately <b>If</b> SeriousUnsafeCondition",
                      by("MaintenanceTablet", True), leaf=True)
    # G-89 [02:35:41] answer to the interviewer's question on who is alerted when sensor data show an
    #      unsafe condition: "The operator and the shift supervisor should be alerted first ... I should be
    #      notified at once as well when it's a serious or potentially unsafe condition"
    #      P2: case-driven (any unsafe condition vs. serious unsafe condition) with different targets.
    g89 = AchieveGoal("G-89: UnsafeConditionAlertRouted <b>If</b> SensorDetectsUnsafeCondition", None,
                      [Refinement(False, [g92, g93], "P2")])
    # G-90 [02:36:59] "the operator stops the equipment and keeps people out of the area"
    g90 = AchieveGoal("G-90: EquipmentStoppedAndPeopleKeptOut <b>If</b> UnsafeConditionAlerted",
                      by("Operator"), leaf=True)
    # G-91 [02:36:23] "A sensor alarm alone isn't enough; someone still has to verify the area is safe"
    g91 = AchieveGoal("G-91: AreaVerifiedSafe <b>If</b> WorkToResume",
                      by("AuthorizedTechnician"), leaf=True)
    # G-79 [02:27:11] "we stopped the work and had the area made safe before anyone continued"
    #      P7: the software cannot control people approaching the machine, so the goal is
    #      split into an alert it controls and actions the operator/technician control.
    g79 = AchieveGoal("G-79: WorkStoppedAndAreaSecured <b>If</b> AbnormalMachineBehavior", None,
                      [Refinement(False, [g89, g90, g91], "P7")])

    # --- No distraction ---
    # G-94 TACIT: my interpretation of [02:40:05] "capture verification that work stopped ...
    #      without distracting operators" - one action, details added later.
    g94 = AchieveGoal("G-94: StopWorkConfirmedWithSingleAction",
                      by("MaintenanceTablet", True), leaf=True)
    # G-95 TACIT: detailed entry deferred until the area is secured.
    g95 = AvoidGoal("G-95: DetailedEntryPrompted <b>If Not</b> AreaSecured",
                    by("MaintenanceTablet", True), leaf=True)
    # G-80 [02:31:46] "Maintenance staff need to stay focused around moving equipment, so tablets
    #      can't become another distraction on the floor"
    #      H6: con of putting records on a tablet (distraction) yields this soft goal.
    g80 = SoftGoal("Minimize[G-80: TabletDistractionNearMovingEquipment]", None,
                   [Refinement(False, [g94, g95], "H6")])

    # G-76 [02:25:41] "My top priority is zero injuries during maintenance work."
    g76 = AvoidGoal("G-76: InjuryDuringMaintenanceWork", None,
                    [Refinement(False, [g78, g79, g80], "H4")])

    # ================= Audit-ready records (G-77 branch) =================
    # G-105 [02:30:45] "usually the operator tells their supervisor or puts in a maintenance request"
    g105 = AchieveGoal("G-105: MaintenanceRequestSubmitted <b>If</b> OperatorObservesProblem",
                       by("Operator"), leaf=True)
    # G-106 [02:30:45] "the machine sensors may flag abnormal vibration, temperature, or cycle behavior"
    #       [02:29:59] "That combination triggered a maintenance report"
    g106 = AchieveGoal("G-106: ReportCreatedWithSensorReadings <b>If</b> SensorFlagsAbnormalBehavior",
                       by("MaintenanceTablet", True), leaf=True)
    # G-101 [02:30:45] "the report identifies the equipment, what was observed, when it happened,
    #       and whether anyone stopped work"; [02:35:03] information needed at report time.
    #       OR-refinement: reported by a person or by the sensors.
    g101 = AchieveGoal("G-101: ProblemReported", None,
                       [Refinement(False, [g105], "H4"),
                        Refinement(False, [g106], "H4")])

    # G-102 [02:34:27] "which hazardous-energy sources were isolated, who applied each lock and tag,
    #       and the date and time"; [02:40:05] "who applied and released each lock and when"
    g102 = AchieveGoal("G-102: LOTODetailRecordedPerEnergySource",
                       by("AuthorizedTechnician"), leaf=True)

    # G-107..G-109 [02:29:59] "I want the record to show what the sensor detected, what the technician
    #              observed, and who made the decision to stop work."
    g107 = AchieveGoal("G-107: SensorDetectionAttachedToRecord",
                       by("MaintenanceTablet", True), leaf=True)
    g108 = AchieveGoal("G-108: TechnicianObservationRecorded",
                       by("AuthorizedTechnician"), leaf=True)
    g109 = AchieveGoal("G-109: StopWorkDecisionMakerRecorded",
                       by("ShiftSupervisor"), leaf=True)
    # G-103 [02:31:46] "I also want evidence that work was stopped when the machine behaved abnormally"
    g103 = AchieveGoal("G-103: StopWorkEvidenceRecorded", None,
                       [Refinement(False, [g107, g108, g109], "H5")])

    # G-104 [02:37:55] "hazard assessment, corrective action, inspection findings"
    g104 = AchieveGoal("G-104: HazardAssessmentAndCorrectiveActionRecorded",
                       by("AuthorizedTechnician"), leaf=True)

    # G-96 [02:37:55] what a record needs to include to be relied on during inspection
    #      P5: one large "complete record" goal split into its independent parts.
    g96 = AchieveGoal("G-96: CompleteSafetyEventRecordCaptured", None,
                      [Refinement(False, [g101, g102, g103, g104], "P5")])

    # G-97 [02:37:55] "a clear history of changes so nobody can quietly overwrite a safety-critical entry"
    g97 = AvoidGoal("G-97: SilentOverwriteOfSafetyCriticalEntry",
                    by("MaintenanceTablet", True), leaf=True)
    # G-98 [02:37:55] "easy to retrieve as one complete record during an inspection"
    g98 = AchieveGoal("G-98: CompleteRecordRetrievedAsOne <b>If</b> InspectionRequested",
                      by("MaintenanceTablet", True), leaf=True)

    # G-110 [02:31:46] "Near misses have to be reported within 24 hours even when nobody is hurt"
    g110 = AchieveGoal("G-110: NearMissReportSubmitted <b>If</b> NearMissOccurs",
                       by("Technician"), leaf=True)
    # G-111 TACIT: reminder so the 24-hour deadline is not missed.
    g111 = AchieveGoal("G-111: EHSNotified <b>If</b> NearMissReportOpenNear24Hours",
                       by("MaintenanceTablet", True), leaf=True)
    # G-99 [02:31:46] / [02:40:05] "near misses must be reported within 24 hours"
    g99 = AchieveGoal("G-99: NearMissReportedWithin24Hours <b>If</b> NearMissOccurs", None,
                      [Refinement(False, [g110, g111], "H11")])

    # G-112 TACIT: system opens a separate report rather than burying it in the repair notes.
    g112 = AchieveGoal("G-112: SpillReportOpenedSeparately <b>If</b> SpillFlaggedOnRepair",
                       by("MaintenanceTablet", True), leaf=True)
    # G-113 [02:38:33] "otherwise we lose track of exposure, cleanup, and compliance"
    g113 = AchieveGoal("G-113: ExposureAndCleanupRecorded",
                       by("EHSOfficer"), leaf=True)
    # G-100 [02:38:33] "If there's a chemical spill, that needs to be treated as a separate
    #       environmental report, not buried in the equipment repair notes"
    g100 = AchieveGoal("G-100: EnvironmentalReportFiledSeparately <b>If</b> ChemicalSpill", None,
                       [Refinement(False, [g112, g113], "H11")])

    # G-114 TACIT: resolution of the obstacle below; grounded in [02:33:46]
    #       "no single owner checking it all in real time"
    g114 = AchieveGoal("G-114: MissingRequiredSafetyFieldFlagged <b>If</b> RecordIncomplete",
                       by("MaintenanceTablet", True), leaf=True)

    # G-77 [02:25:41] "complete, reliable safety records for every inspection, so we can prove
    #      the work was done properly"; H3: instantiates the information, integrity and
    #      environmental-compliance goal categories.
    g77 = MaintainGoal("G-77: AuditReadySafetyRecords", None,
                       [Refinement(False, [g96, g97, g98, g99, g100, g114], "H3")])

    # ================= Root =================
    # G-75 TACIT: H12 abstraction joining Rob's two stated priorities at [02:25:41].
    g75 = MaintainGoal("G-75: SafeAndCompliantMaintenanceWork", None,
                       [Refinement(False, [g76, g77], "H12")])

    # ================= Obstacles (H8) and conflicts =================
    # O [02:33:11] "A missing signature, mismatched time, or incomplete lockout detail can undermine
    #   the whole inspection record, and I may not discover it until the inspector is standing there."
    o_gap = Obstacle("MissingSignatureOrLOTODetailUnnoticedUntilInspection", annotation="H8")
    # O [02:32:36] "Supervisors sometimes keep local copies, which creates version-control problems."
    o_copies = Obstacle("ConflictingLocalCopiesOfSafetyRecords", annotation="H8")

    links = [
        ObstructionLink(g96, o_gap),
        ResolutionLink(g114, o_gap),
        ObstructionLink(g98, o_copies),
        ResolutionLink(g97, o_copies),
        # Rob's own tension: names and timestamps of everyone who stopped, worked on, verified and
        # released (G-96) vs. no tablet distraction near moving equipment (G-80).
        ConflictLink(g96, g80),
    ]
    tacit = [g75, g94, g95, g111, g112, g114]
    return [g75], links, tacit


def render(roots, links, tacit):
    output = generate_graph(roots, links)
    output += "".join(f"style {g.get_node_id()} {YELLOW}\n" for g in tacit)
    return output


if __name__ == "__main__":
    output = render(*build())
    print(output)
    print(generate_pako_link(output))
