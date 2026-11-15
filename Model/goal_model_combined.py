"""
Combined goal model: Teo Salinas (night-shift technician), Angela Novak (maintenance /
reliability manager) and Rob Kessler (EHS, safety and compliance).

Built by merging goal_model_Teo.py (G-1..G-39), goal_model_Angela.py (G-40..G-74) and
goal_model_Rob.py (G-75..G-114). Goal IDs are kept from the individual models so every goal
traces back to its source; one new goal (G-115) joins the three stakeholder trees.

Running this file prints the Mermaid diagram definition and writes the view link to mermaid.txt.

----------------------------------------------------------------------------------------------
REDUNDANCIES - duplicate goals merged (removed ID -> retained ID, retained goal re-written)
----------------------------------------------------------------------------------------------
  G-6   (Teo)    PressIsolated If PressDown
        -> G-81 (Rob) EquipmentLockedOut If ServiceRequiredOrPressDown.
           Teo's isolation step before a repair is Rob's lockout/tagout; G-81 now sits in both
           Teo's repair milestones (G-2) and Rob's energy-control goal (G-78).
  G-33  (Teo)    FoundDoneAndWatchItemsRecorded
        -> G-65 (Angela) OpenRepairStateRecordedWhileOpen: machine condition, isolation status,
           what was found, work done, parts, tests, temporary repairs, next action and
           what to watch.
  G-34  (Teo)    Reduce[RepeatedChecksAfterShiftChange]
        -> G-45 (Angela) Avoid[RepairRestartedOrChecksRepeated If ShiftChangesDuringRepair].
  G-64  (Angela) VerbalHandoffWithIncomingShiftLead
        -> G-29 (Teo) FaceToFaceHandoverWithIncomingShift If PressDownOrNeedsWatching
           (point to the machine, repeat back; with the incoming technician or shift lead).
  G-66  (Angela) OpenRepairsAndNextActionVisibleByMachineAndShift
        -> G-10 (Teo) OpenRepairStatusAndNextActionShownAtPressByShift (also who worked on it
           and what was already tested).
  G-67  (Angela) Increase[RepairTraceabilityForCustomerAudits]
        -> G-77 (Rob) AuditReadyMaintenanceAndSafetyRecords (regulatory inspections and
           customer audits).
  G-72  (Angela) Minimize[TechnicianEntryEffortDuringBreakdown]
        -> G-35 (Teo) Minimize[TabletEntryEffortAndInterferenceDuringBreakdown].
  G-74  (Angela) EventOpenedByTechnician If Not SensorDetectsStop
        -> G-105 (Rob) ProblemReportedManually If PersonObservesProblem (covers stops and
           abnormal behaviour that sensors miss, e.g., Teo's offline presses).
  G-98  (Rob)    CompleteRecordRetrievedAsOne If InspectionRequested
        -> G-58 (Angela) CompleteMachineRecordRetrievedAsOneWithinOneMinute (repair, downtime,
           reason codes, parts, PM findings, LOTO and safety entries).
  G-107 (Rob)    SensorDetectionAttachedToRecord
        -> G-106 (Rob) ReportCreatedWithSensorEvidence If SensorFlagsAbnormalBehavior.

  Enriched (not a merge): G-1 (Teo) now reads CriticalPressesProducingThroughShift, adding
  Angela's "keeping the critical machines running" [Angela 01:50:53].

----------------------------------------------------------------------------------------------
CONFLICTS (ConflictLink in the diagram)
----------------------------------------------------------------------------------------------
  C-1  G-55 Avoid[EventClosed If Not ReasonCodeAndTimesRecorded]  (Angela)
       vs G-35 Minimize[TabletEntryEffortAndInterferenceDuringBreakdown] (Teo + Angela).
       Angela states both sides herself [01:53:42]. Unstated condition: required fields
       block closing an event, never opening it or starting isolation (see G-37).
  C-2  G-40 Reduce[UnplannedDowntimeOnCriticalMachines] (Angela)
       vs G-79 WorkStoppedAndAreaSecured If AbnormalMachineBehavior (Rob).
       Each warned about the other: Angela says Rob "may prioritize caution over uptime"
       [02:11:14]; Rob says "make sure safety requirements aren't watered down to keep
       production moving" [02:40:52]. Resolution: safety holds take priority; the downtime
       they cause is recorded under a safety reason code rather than counted against the
       repair.
  C-3  G-70 Avoid[AlertSent If MachineInPlannedMaintenance] (Angela)
       vs G-92 OperatorAndSupervisorAlertedFirst If UnsafeCondition (Rob).
       People are at the machine during planned maintenance, which is when an unsafe-
       condition alert matters most. Resolution: G-70 suppresses only production/condition
       alerts; safety alerts are never suppressed.
  C-4  G-54 ReasonCodeSelectedFromQuickList - "not just free-text" (Angela)
       vs G-36 RepairLoggedByQuickNotePhotoOrVoice (Teo).
       Teo on Angela: "she'll want everything in neat boxes" [Teo 01:35:58]. Resolution: a coded
       field is required; photo/voice notes supplement it.
  C-5  G-50 EventDataCaptured If NetworkInterrupted - sync later (Angela)
       vs G-97 Avoid[SilentOverwriteOfSafetyCriticalEntry] (Rob).
       Later sync can overwrite or re-time an entry. Resolution: append-only sync that keeps
       the device timestamp and the change history.
  C-6  G-96 CompleteSafetyEventRecordCaptured (Rob)
       vs G-80 Minimize[TabletDistractionNearMovingEquipment] (Rob).
       Rob's own tension: many names and timestamps vs. no distraction [02:37:55, 02:31:46].

----------------------------------------------------------------------------------------------
INCONSISTENCIES (resolved by an explicit condition; no conflict link)
----------------------------------------------------------------------------------------------
  I-1  Sensor coverage. Angela assumes the sensor gives the stop time (G-51, G-53); Teo says
       some 1990s presses are offline with no sensors [Teo 01:35:26]. Resolved by the
       conditions on G-51 / G-14 / G-24, the manual cases G-105 and G-15, and G-38.
  I-2  When is a repair "done"? For Angela, downtime ends at the first good part (G-53);
       for Teo "fixed means it ran a full shift without me" (G-19). Both are kept: G-53 ends
       the downtime clock, G-19 / G-20 close or reopen the repair after the next shift.
  I-3  Handover. Angela calls verbal handoff "more reliable than paperwork" [01:59:11] yet
       prefers a system record [01:59:45]; Teo's team moved to face-to-face after a missed
       note [Teo 01:24:21]. Kept as the OR-refinement of G-4.
  I-4  Voice notes (Teo, G-36) vs. noisy floor where technicians "can't easily hear prompts"
       (Angela, G-73). Not a conflict of goals but a feasibility risk for G-36.

----------------------------------------------------------------------------------------------
Agent names were harmonised: Teo's "NightTechnician" and Angela's "Technician" are
"Technician"; Rob's "AuthorizedTechnician" is kept for lockout/tagout tasks.
TACIT goals (not stated in any transcript) are highlighted yellow.
"""
from pathlib import Path

from goalmodeling.schema import *

YELLOW = "fill:#fff59d"
TECH = "Technician"
AUTH = "AuthorizedTechnician"
TABLET = "MaintenanceTablet"


def by(name, software=False):
    """Responsibility link from a leaf goal to a single agent."""
    kind = AgentType.SOFTWARE_AGENT if software else AgentType.ENVIRONMENT_AGENT
    return [PerformanceLink(Agent(name, kind), None)]


def sw():
    return by(TABLET, True)


def build():
    # =====================================================================================
    # SHARED LEAVES AND SUB-GOALS (used under more than one stakeholder's branch)
    # =====================================================================================
    # Lockout/tagout - Rob [02:27:46]; Teo's isolation step G-6 merged here [Teo 01:17:49, 01:33:23]
    g83 = AchieveGoal("G-83: AllHazardousEnergySourcesIsolated", by(AUTH), leaf=True)
    g84 = AchieveGoal("G-84: PersonalLockAndTagApplied", by(AUTH), leaf=True)
    g85 = AchieveGoal("G-85: ZeroEnergyVerified <b>If</b> LocksApplied", by(AUTH), leaf=True)
    # G-81 MERGED with G-6 (Teo)
    g81 = AchieveGoal("G-81: EquipmentLockedOut <b>If</b> ServiceRequiredOrPressDown", None,
                      [Refinement(False, [g83, g84, g85], "P1")])

    # G-10 MERGED with G-66 (Angela) - Teo [01:33:55, 01:34:20]; Angela [01:58:37]
    g10 = AchieveGoal("G-10: OpenRepairStatusAndNextActionShownAtPressByShift", sw(), leaf=True)
    # G-65 MERGED with G-33 (Teo) - Angela [01:59:45, 02:00:20]; Teo [01:23:14, 01:21:42]
    g65 = MaintainGoal("G-65: OpenRepairStateRecordedWhileOpen", by("OutgoingTechnician"), leaf=True)

    # G-58 MERGED with G-98 (Rob) - Angela [02:02:24]; Rob [02:37:55]
    g58 = AchieveGoal("G-58: CompleteMachineRecordRetrievedAsOneWithinOneMinute", sw(), leaf=True)
    # G-59 Angela [01:57:22, 01:50:53]
    g59 = AchieveGoal("G-59: MTBFReportedByMachineAndFailureMode", sw(), leaf=True)
    # G-54 Angela [01:53:42, 01:51:50]
    g54 = AchieveGoal("G-54: ReasonCodeSelectedFromQuickList", by(TECH), leaf=True)
    # G-48 Angela [01:51:50]
    g48 = MaintainGoal("G-48: RepairHistoryShowsWhoAndWhen", sw(), leaf=True)

    # G-105 MERGED with G-74 (Angela) - Rob [02:30:45]; Angela case of stops sensors miss
    g105 = AchieveGoal("G-105: ProblemReportedManually <b>If</b> PersonObservesProblem",
                       by("Operator"), leaf=True)
    # G-106 MERGED with G-107 (Rob) - Rob [02:30:45, 02:29:59]
    g106 = AchieveGoal("G-106: ReportCreatedWithSensorEvidence <b>If</b> SensorFlagsAbnormalBehavior",
                       sw(), leaf=True)

    # =====================================================================================
    # PRODUCTION BRANCH (Teo + Angela)
    # =====================================================================================
    # ---- G-2 restore a down press (Teo) ----
    g11 = AchieveGoal("G-11: PriorTestsCheckedBeforeTroubleshooting", by(TECH), leaf=True)  # Teo 01:17:49
    g5 = AchieveGoal("G-5: PriorWorkReviewed <b>If</b> PressDown", None,                     # Teo 01:16:40
                     [Refinement(False, [g10, g11], "H5")])

    g14 = AchieveGoal("G-14: AlarmHistoryAndSensorTrendShown <b>If</b> PressHasSensors",   # Teo 01:33:55
                      sw(), leaf=True)
    g15 = AchieveGoal("G-15: ObservationsRecordedManually <b>If Not</b> PressHasSensors",  # Teo 01:35:26
                      by(TECH), leaf=True)
    dp_sensors = DomainProperty("EachPress HasSensors <b>Or</b> IsOfflineWithoutSensors", leaf=True)
    g12 = AchieveGoal("G-12: FaultEvidenceAvailable", None,                                  # TACIT
                      [Refinement(True, [g14, g15, dp_sensors], "P3")])
    g13 = AchieveGoal("G-13: ReadingComparedWithPressNormalTrend", by(TECH), leaf=True)     # Teo 01:30:13
    g7 = AchieveGoal("G-7: FaultDiagnosed", None, [Refinement(False, [g12, g13], "H4")])

    g16 = AchieveGoal("G-16: SparePartBinLocationShown", sw(), leaf=True)                   # Teo 01:34:20
    g17 = AchieveGoal("G-17: FaultyComponentReplaced", by(TECH), leaf=True)                 # Teo 01:17:49
    g8 = AchieveGoal("G-8: FaultRepaired", None, [Refinement(False, [g16, g17], "H7")])

    g18 = AchieveGoal("G-18: TrialCyclesRunAndWatched", by(TECH), leaf=True)                # Teo 01:22:24
    g19 = AchieveGoal("G-19: RepairClosedAsFixed <b>If</b> NoRepeatFaultDuringNextShift",   # TACIT
                      sw(), leaf=True)
    g20 = AchieveGoal("G-20: RepairReopened <b>If</b> RepeatFaultDuringNextShift",          # TACIT
                      sw(), leaf=True)
    g9 = AchieveGoal("G-9: RepairVerified", None, [Refinement(False, [g18, g19, g20], "H10")])

    # G-2 Teo [01:16:40, 01:34:20]; isolation milestone is now Rob's lockout G-81
    g2 = AchieveGoal("G-2: PressRestoredQuickly <b>If</b> PressDown", None,
                     [Refinement(False, [g5, g81, g7, g8, g9], "P1")])

    # ---- G-3 catch failures before alarms (Teo) ----
    g24 = AchieveGoal("G-24: DriftFromPressBaselineFlagged <b>If</b> PressHasSensors",      # TACIT
                      sw(), leaf=True)
    g25 = AchieveGoal("G-25: AbnormalSoundOrFeelNoticed", by(TECH), leaf=True)              # Teo 01:31:13
    g21 = AchieveGoal("G-21: EarlyWarningSignDetected", None,                                # Teo 01:28:27
                      [Refinement(False, [g24, g25], "P6")])
    g22 = AchieveGoal("G-22: PressStoppedAndInspected <b>If</b> WarningSignDetected",       # Teo 01:27:19
                      by(TECH), leaf=True)
    g26 = AchieveGoal("G-26: WarningPatternRecordedForPress", by(TECH), leaf=True)          # Teo 01:31:45
    g27 = AchieveGoal("G-27: WarningPatternsShownWithPressHistory", sw(), leaf=True)       # TACIT
    g28 = AchieveGoal("G-28: NewTechnicianCoachedAtPress", by(TECH), leaf=True)             # Teo 01:32:17
    g23 = MaintainGoal("G-23: PressSpecificWarningKnowledgeShared", None,                    # Teo 01:28:27
                       [Refinement(False, [g26, g27], "H6"),
                        Refinement(False, [g28], "H6")])
    g3 = AvoidGoal("G-3: PressFailure <b>If</b> EarlyWarningSignPresent", None,              # Teo 01:26:52
                   [Refinement(False, [g21, g22, g23], "H4")])

    # ---- G-41 reliable event data (Angela) ----
    g51 = AchieveGoal("G-51: EventOpenedAutomatically <b>If</b> SensorDetectsStop",         # Angela 02:05:28
                      sw(), leaf=True)
    g52 = AchieveGoal("G-52: FirstGoodPartConfirmed <b>If</b> ProductionResumes",           # Angela 01:54:08
                      by("Operator"), leaf=True)
    g53 = MaintainGoal("G-53: DowntimeClockRunning <b>If</b> EventOpen <b>And Not</b> FirstGoodPartConfirmed",
                       sw(), leaf=True)                                                      # Angela 02:05:28
    g46 = AchieveGoal("G-46: DowntimeMeasuredStopToFirstGoodPart", None,                     # Angela 01:51:50
                      [Refinement(False, [g51, g105, g52, g53], "P6")])

    g55 = AvoidGoal("G-55: EventClosed <b>If Not</b> ReasonCodeAndTimesRecorded",          # Angela 01:53:42
                    sw(), leaf=True)
    g47 = AchieveGoal("G-47: EventClosedWithReasonCode <b>If</b> RepairComplete", None,      # Angela 01:53:42
                      [Refinement(False, [g54, g55], "P4")])

    g56 = AchieveGoal("G-56: InspectionReadingsEnteredAgainstChecklist", by(TECH), leaf=True)  # Angela 01:55:18
    g57 = AchieveGoal("G-57: OutOfToleranceFlaggedAndLinkedToFollowUp", sw(), leaf=True)       # Angela 01:57:57
    g49 = AchieveGoal("G-49: PMFindingsRecordedAgainstChecklist", None,
                      [Refinement(False, [g56, g57], "H5")])

    g50 = MaintainGoal("G-50: EventDataCaptured <b>If</b> NetworkInterrupted", sw(), leaf=True)  # Angela 02:08:07
    g41 = MaintainGoal("G-41: ReliableMaintenanceEventData", None,                               # Angela 01:51:19
                       [Refinement(False, [g46, g47, g48, g49, g50], "P5")])

    # ---- G-42 repeat failures (Angela) ----
    g60 = AchieveGoal("G-60: RootCauseOrOneOffDecided", by("MaintenanceManager"), leaf=True)    # Angela 02:01:50
    g42 = AchieveGoal("G-42: RootCauseDecided <b>If</b> RepeatFailure", None,
                      [Refinement(False, [g58, g59, g60], "H7")])

    # ---- G-43 PM intervals (Angela) ----
    g61 = AchieveGoal("G-61: PMFrequencyTightened <b>If</b> CriticalMachineDegradesBeforeInterval",
                      by("MaintenanceManager"), leaf=True)                                   # Angela 01:56:40
    g62 = AchieveGoal("G-62: PMIntervalLengthenedUnderControlledRevision <b>If</b> EquipmentStable",
                      by("MaintenanceManager"), leaf=True)                                   # Angela 01:56:40
    g43 = MaintainGoal("G-43: PMIntervalMatchesMachineCondition", None,
                       [Refinement(False, [g61, g62], "P2")])

    # ---- G-45 shift handover (Teo + Angela) ----
    g31 = AchieveGoal("G-31: TestsAndChangesExplainedAtMachine", by("OutgoingTechnician"), leaf=True)  # Teo 01:24:21
    g32 = AchieveGoal("G-32: TakeoverRepeatedBack", by("IncomingTechnician"), leaf=True)              # Teo 01:24:21
    # G-29 MERGED with G-64 (Angela) - Teo [01:24:21]; Angela [01:58:37]
    g29 = AchieveGoal("G-29: FaceToFaceHandoverWithIncomingShift <b>If</b> PressDownOrNeedsWatching", None,
                      [Refinement(False, [g31, g32], "H11")])
    g30 = AchieveGoal("G-30: HandoverRecordedAndShownAtPress", None,                          # Teo 01:21:42
                      [Refinement(False, [g65, g10], "H4")])
    g4 = AchieveGoal("G-4: RepairStatusHandedOverToNextShift", None,                           # Teo 01:21:59
                     [Refinement(False, [g29], "H6"),
                      Refinement(False, [g30], "H6")])
    # G-45 MERGED with G-34 (Teo) - Angela [02:00:20]; Teo [01:21:59]
    g45 = AvoidGoal("G-45: RepairRestartedOrChecksRepeated <b>If</b> ShiftChangesDuringRepair", None,
                    [Refinement(False, [g4], "H4")])

    # ---- G-68 actionable alerts (Angela) ----
    g69 = AchieveGoal("G-69: AlertWithSeverityAndNextActionSent <b>If</b> LimitCrossedOrCriticalStop",
                      sw(), leaf=True)                                                       # Angela 02:06:05
    g70 = AvoidGoal("G-70: AlertSent <b>If</b> MachineInPlannedMaintenance", sw(), leaf=True)   # Angela 02:06:05
    g71 = AvoidGoal("G-71: RepeatedAlertsForMinorFluctuation", sw(), leaf=True)                # Angela 02:06:05
    g68 = AchieveGoal("G-68: ActionableAlertSent <b>If</b> ConditionNeedsAction", None,
                      [Refinement(False, [g69, g70, g71], "H10")])

    # ---- G-40 / G-44 / G-1 ----
    g40 = SoftGoal("Reduce[G-40: UnplannedDowntimeOnCriticalMachines]", None,                  # Angela 01:50:53
                   [Refinement(False, [g2, g3, g41, g42, g43, g45, g68], "H4")])
    g63 = AchieveGoal("G-63: PMScheduledInPlannedChangeover", by("MaintenanceManager"), leaf=True)  # Angela 01:54:45
    g44 = AchieveGoal("G-44: MaintenancePlannedAroundProductionOrders", None,                  # Angela 01:50:53
                      [Refinement(False, [g59, g63], "H4")])
    # G-1 ENRICHED with Angela's "keeping the critical machines running" - Teo [01:34:49]
    g1 = MaintainGoal("G-1: CriticalPressesProducingThroughShift", None,
                      [Refinement(False, [g40, g44], "H4")])

    # =====================================================================================
    # SAFETY AND COMPLIANCE BRANCH (Rob)
    # =====================================================================================
    g86 = AchieveGoal("G-86: HazardCorrectedAndInspected", by(AUTH), leaf=True)              # Rob 02:36:59
    g87 = AchieveGoal("G-87: ReleaseAuthorizedAndRecorded", by("ShiftSupervisor"), leaf=True)  # Rob 02:27:46
    g88 = AvoidGoal("G-88: EquipmentReleased <b>If Not</b> LockRemovalAndReleaseRecorded",   # Rob 02:27:11
                    sw(), leaf=True)
    g82 = AchieveGoal("G-82: EquipmentReleasedSafely <b>If</b> ServiceComplete", None,
                      [Refinement(False, [g86, g87, g88], "P4")])
    g78 = MaintainGoal("G-78: HazardousEnergyControlledDuringService", None,                  # Rob 02:26:34
                       [Refinement(False, [g81, g82], "H9")])

    g92 = AchieveGoal("G-92: OperatorAndSupervisorAlertedFirst <b>If</b> UnsafeCondition",    # Rob 02:35:41
                      sw(), leaf=True)
    g93 = AchieveGoal("G-93: EHSNotifiedImmediately <b>If</b> SeriousUnsafeCondition",       # Rob 02:36:23
                      sw(), leaf=True)
    g89 = AchieveGoal("G-89: UnsafeConditionAlertRouted <b>If</b> SensorDetectsUnsafeCondition", None,
                      [Refinement(False, [g92, g93], "P2")])
    g90 = AchieveGoal("G-90: EquipmentStoppedAndPeopleKeptOut <b>If</b> UnsafeConditionAlerted",  # Rob 02:36:59
                      by("Operator"), leaf=True)
    g91 = AchieveGoal("G-91: AreaVerifiedSafe <b>If</b> WorkToResume", by(AUTH), leaf=True)  # Rob 02:36:23
    g79 = AchieveGoal("G-79: WorkStoppedAndAreaSecured <b>If</b> AbnormalMachineBehavior", None,  # Rob 02:27:11
                      [Refinement(False, [g89, g90, g91], "P7")])

    g94 = AchieveGoal("G-94: StopWorkConfirmedWithSingleAction", sw(), leaf=True)            # TACIT
    g95 = AvoidGoal("G-95: DetailedEntryPrompted <b>If Not</b> AreaSecured", sw(), leaf=True)  # TACIT
    g80 = SoftGoal("Minimize[G-80: TabletDistractionNearMovingEquipment]", None,             # Rob 02:31:46
                   [Refinement(False, [g94, g95], "H6")])
    g76 = AvoidGoal("G-76: InjuryDuringMaintenanceWork", None,                                # Rob 02:25:41
                    [Refinement(False, [g78, g79, g80], "H4")])

    g101 = AchieveGoal("G-101: ProblemReported", None,                                        # Rob 02:30:45
                       [Refinement(False, [g105], "H4"),
                        Refinement(False, [g106], "H4")])
    g102 = AchieveGoal("G-102: LOTODetailRecordedPerEnergySource", by(AUTH), leaf=True)      # Rob 02:34:27
    g108 = AchieveGoal("G-108: TechnicianObservationRecorded", by(AUTH), leaf=True)          # Rob 02:29:59
    g109 = AchieveGoal("G-109: StopWorkDecisionMakerRecorded", by("ShiftSupervisor"), leaf=True)  # Rob 02:29:59
    g103 = AchieveGoal("G-103: StopWorkEvidenceRecorded", None,                               # Rob 02:31:46
                       [Refinement(False, [g106, g108, g109], "H5")])
    g104 = AchieveGoal("G-104: HazardAssessmentAndCorrectiveActionRecorded", by(AUTH), leaf=True)  # Rob 02:37:55
    g96 = AchieveGoal("G-96: CompleteSafetyEventRecordCaptured", None,                        # Rob 02:37:55
                      [Refinement(False, [g101, g102, g103, g104], "P5")])

    g97 = AvoidGoal("G-97: SilentOverwriteOfSafetyCriticalEntry", sw(), leaf=True)           # Rob 02:37:55
    g110 = AchieveGoal("G-110: NearMissReportSubmitted <b>If</b> NearMissOccurs", by(TECH), leaf=True)  # Rob 02:31:46
    g111 = AchieveGoal("G-111: EHSNotified <b>If</b> NearMissReportOpenNear24Hours", sw(), leaf=True)   # TACIT
    g99 = AchieveGoal("G-99: NearMissReportedWithin24Hours <b>If</b> NearMissOccurs", None,
                      [Refinement(False, [g110, g111], "H11")])
    g112 = AchieveGoal("G-112: SpillReportOpenedSeparately <b>If</b> SpillFlaggedOnRepair",   # TACIT
                       sw(), leaf=True)
    g113 = AchieveGoal("G-113: ExposureAndCleanupRecorded", by("EHSOfficer"), leaf=True)     # Rob 02:38:33
    g100 = AchieveGoal("G-100: EnvironmentalReportFiledSeparately <b>If</b> ChemicalSpill", None,
                       [Refinement(False, [g112, g113], "H11")])
    g114 = AchieveGoal("G-114: MissingRequiredSafetyFieldFlagged <b>If</b> RecordIncomplete",  # TACIT
                       sw(), leaf=True)
    # G-77 MERGED with G-67 (Angela) - Rob [02:25:41]; Angela [01:59:11]
    g77 = MaintainGoal("G-77: AuditReadyMaintenanceAndSafetyRecords", None,
                       [Refinement(False, [g96, g97, g58, g48, g65, g99, g100, g114], "H3")])

    g75 = MaintainGoal("G-75: SafeAndCompliantMaintenanceWork", None,                       # TACIT (H12)
                       [Refinement(False, [g76, g77], "H12")])

    # =====================================================================================
    # USABILITY BRANCH (Teo + Angela)
    # =====================================================================================
    g36 = AchieveGoal("G-36: RepairLoggedByQuickNotePhotoOrVoice", sw(), leaf=True)          # Teo 01:32:52
    g37 = AvoidGoal("G-37: RequiredFieldsBlockingIsolation <b>If</b> PressDown", sw(), leaf=True)  # Teo 01:33:23
    g38 = AvoidGoal("G-38: MissingSensorDataTreatedAsFault <b>If</b> PressOffline", sw(), leaf=True)  # Teo 01:35:26
    g39 = AchieveGoal("G-39: PressRecordOpenedWithoutSearching", sw(), leaf=True)            # Teo 01:33:23
    g73 = AchieveGoal("G-73: EntriesUsableWithGlovesAndInNoise", sw(), leaf=True)            # Angela 02:07:37
    # G-35 MERGED with G-72 (Angela) - Teo [01:34:49]; Angela [02:10:08, 02:07:37]
    g35 = SoftGoal("Minimize[G-35: TabletEntryEffortAndInterferenceDuringBreakdown]", None,
                   [Refinement(False, [g36, g37, g38, g39, g54, g73], "H3")])

    # =====================================================================================
    # ROOT - G-115 TACIT (H12): joins production (Teo, Angela), safety/compliance (Rob)
    # and usability (Teo, Angela). Angela [02:10:08] "practical enough for technicians ...
    # while still giving me complete, auditable data"; Rob [02:41:18] "production can wait".
    # =====================================================================================
    g115 = MaintainGoal("G-115: SafeProductiveAndAuditableMaintenance", None,
                        [Refinement(False, [g75, g1, g35], "H12")])

    # =====================================================================================
    # OBSTACLES (H8) - carried over from the individual models
    # =====================================================================================
    o_tricks = Obstacle("TechnicianWithholdsPersonalTricksFromRecord", annotation="H8")          # Teo 01:24:54
    o_missed = Obstacle("HandoverNoteMissedByIncomingShift", annotation="H8")                    # Teo 01:23:40
    o_notebook = Obstacle("TechnicianRevertsToPaperNotebook", annotation="H8")                   # Teo 01:32:52
    o_net = Obstacle("TabletLosesConnectivity", annotation="H8")                                 # Angela 02:08:07
    o_skip = Obstacle("ReasonCodeSkippedToRestoreProduction", annotation="H8")                   # Angela 01:53:42
    o_gap = Obstacle("MissingSignatureOrLOTODetailUnnoticedUntilInspection", annotation="H8")    # Rob 02:33:11
    o_copies = Obstacle("ConflictingLocalCopiesOfSafetyRecords", annotation="H8")                # Rob 02:32:36

    links = [
        ObstructionLink(g26, o_tricks), ResolutionLink(g28, o_tricks),
        ObstructionLink(g4, o_missed), ResolutionLink(g29, o_missed),
        ObstructionLink(g30, o_notebook), ResolutionLink(g36, o_notebook),
        ObstructionLink(g41, o_net), ResolutionLink(g50, o_net),
        ObstructionLink(g47, o_skip), ResolutionLink(g55, o_skip),
        ObstructionLink(g96, o_gap), ResolutionLink(g114, o_gap),
        ObstructionLink(g58, o_copies), ResolutionLink(g97, o_copies),
        # Conflicts C-1 .. C-6 (see module docstring)
        ConflictLink(g55, g35),
        ConflictLink(g40, g79),
        ConflictLink(g70, g92),
        ConflictLink(g54, g36),
        ConflictLink(g50, g97),
        ConflictLink(g96, g80),
    ]
    tacit = [g12, g19, g20, g24, g27, g75, g94, g95, g111, g112, g114, g115]
    return [g115], links, tacit


def render(roots, links, tacit):
    output = generate_graph(roots, links)
    output += "".join(f"style {g.get_node_id()} {YELLOW}\n" for g in tacit)
    return output


if __name__ == "__main__":
    output = render(*build())
    link = generate_pako_link(output)
    print(output)
    print(link)
    Path(__file__).with_name("mermaid.txt").write_text(link + "\n", encoding="utf-8")
