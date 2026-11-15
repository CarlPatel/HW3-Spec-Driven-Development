"""
Goal model for Angela Novak (maintenance / reliability manager; uptime and data).
Source: transcript-261026-2218.csv (timestamps below are 2026-10-27, UTC, HH:MM:SS).

Conventions
- Goal IDs G-40 .. G-74 (IDs are unique across all three stakeholder models).
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
    # ---------------- Reliable event data (G-41 branch) ----------------
    # G-51 [02:05:28] "automatically tie the sensor-detected stop to the maintenance event"
    g51 = AchieveGoal("G-51: EventOpenedAutomatically <b>If</b> SensorDetectsStop",
                      by("MaintenanceTablet", True), leaf=True)
    # G-74 TACIT: case the sensor misses (e.g., operator-noticed stop); converse case of G-51.
    g74 = AchieveGoal("G-74: EventOpenedByTechnician <b>If Not</b> SensorDetectsStop",
                      by("Technician"), leaf=True)
    # G-52 [01:54:08] "the first-good-part time came from the operator's notes and production confirmation"
    g52 = AchieveGoal("G-52: FirstGoodPartConfirmed <b>If</b> ProductionResumes",
                      by("Operator"), leaf=True)
    # G-53 [02:05:28] "keep the downtime clock running until the first good part is confirmed"
    g53 = MaintainGoal("G-53: DowntimeClockRunning <b>If</b> EventOpen <b>And Not</b> FirstGoodPartConfirmed",
                       by("MaintenanceTablet", True), leaf=True)
    # G-46 [01:51:50] "Downtime has to be measured in minutes, from the stop until the first good part"
    #      P6: the software cannot monitor "first good part"; the operator must confirm it.
    g46 = AchieveGoal("G-46: DowntimeMeasuredStopToFirstGoodPart", None,
                      [Refinement(False, [g51, g74, g52, g53], "P6")])

    # G-54 [01:53:42] "keeping the choices quick enough not to delay the technician";
    #      [01:51:50] "tied to a reason code - not just a technician's free-text comment"
    g54 = AchieveGoal("G-54: ReasonCodeSelectedFromQuickList",
                      by("Technician"), leaf=True)
    # G-55 [01:53:42] "require a reason code and capture the stop and first-good-part times
    #       before the event can be closed"
    g55 = AvoidGoal("G-55: EventClosed <b>If Not</b> ReasonCodeAndTimesRecorded",
                    by("MaintenanceTablet", True), leaf=True)
    # G-47 [01:53:42] Press 17 "closed with the technical notes but without selecting the reason code"
    #      P4: guard (reason code and times recorded) introduced before closure.
    g47 = AchieveGoal("G-47: EventClosedWithReasonCode <b>If</b> RepairComplete", None,
                      [Refinement(False, [g54, g55], "P4")])

    # G-48 [01:51:50] "repair history to show who did the work and when, so the records hold up over time"
    g48 = MaintainGoal("G-48: RepairHistoryShowsWhoAndWhen",
                       by("MaintenanceTablet", True), leaf=True)

    # G-56 [01:55:18] "records inspection readings against the checklist"
    g56 = AchieveGoal("G-56: InspectionReadingsEnteredAgainstChecklist",
                      by("Technician"), leaf=True)
    # G-57 [01:57:57] "flag out-of-tolerance results, and link them to a follow-up repair or root cause"
    g57 = AchieveGoal("G-57: OutOfToleranceFlaggedAndLinkedToFollowUp",
                      by("MaintenanceTablet", True), leaf=True)
    # G-49 [01:57:57] "The system should capture those readings against the machine's checklist"
    g49 = AchieveGoal("G-49: PMFindingsRecordedAgainstChecklist", None,
                      [Refinement(False, [g56, g57], "H5")])

    # G-50 [02:08:07] "tolerate brief network interruptions and synchronize later"
    g50 = MaintainGoal("G-50: EventDataCaptured <b>If</b> NetworkInterrupted",
                       by("MaintenanceTablet", True), leaf=True)

    # G-41 [01:51:19] "Reliable data is complete, consistent, and tied to the machine and the actual event"
    #      P5: the conjunction (complete AND consistent AND tied to the event) is split per concern.
    g41 = MaintainGoal("G-41: ReliableMaintenanceEventData", None,
                       [Refinement(False, [g46, g47, g48, g49, g50], "P5")])

    # ---------------- Repeat failures and planning ----------------
    # G-58 [02:02:24] "the complete repair history should be available in under a minute"
    g58 = AchieveGoal("G-58: CompleteMachineHistoryShownWithinOneMinute",
                      by("MaintenanceTablet", True), leaf=True)
    # G-59 [01:57:22] "I use it by machine and failure mode, not as one plant-wide number"
    #      [01:50:53] "reliable data on which machines fail most"
    g59 = AchieveGoal("G-59: MTBFReportedByMachineAndFailureMode",
                      by("MaintenanceTablet", True), leaf=True)
    # G-60 [02:01:50] "deciding whether a repeat failure is a root cause or a one-off"
    g60 = AchieveGoal("G-60: RootCauseOrOneOffDecided",
                      by("MaintenanceManager"), leaf=True)
    # G-42 [02:01:50] / [02:02:24] reviewing a repeat failure
    g42 = AchieveGoal("G-42: RootCauseDecided <b>If</b> RepeatFailure", None,
                      [Refinement(False, [g58, g59, g60], "H7")])

    # G-61 / G-62 [01:56:40] "if a critical machine shows degradation before the scheduled interval,
    #      we tighten the PM frequency, while stable equipment may move to a longer interval
    #      under controlled revision"
    g61 = AchieveGoal("G-61: PMFrequencyTightened <b>If</b> CriticalMachineDegradesBeforeInterval",
                      by("MaintenanceManager"), leaf=True)
    g62 = AchieveGoal("G-62: PMIntervalLengthenedUnderControlledRevision <b>If</b> EquipmentStable",
                      by("MaintenanceManager"), leaf=True)
    # G-43 [01:56:40] "The interval is based on the OEM service interval, our failure-history data,
    #      and condition-based indicators"
    g43 = MaintainGoal("G-43: PMIntervalMatchesMachineCondition", None,
                       [Refinement(False, [g61, g62], "P2")])

    # G-63 [01:54:45] "we performed preventive maintenance on Injection Molder 8 during a planned changeover"
    g63 = AchieveGoal("G-63: PMScheduledInPlannedChangeover",
                      by("MaintenanceManager"), leaf=True)
    # G-44 [01:50:53] "so we can plan maintenance around production orders"
    g44 = AchieveGoal("G-44: MaintenancePlannedAroundProductionOrders", None,
                      [Refinement(False, [g59, g63], "H4")])

    # ---------------- Shift handoff ----------------
    # G-64 [01:58:37] "then discusses it with the incoming shift lead"
    g64 = AchieveGoal("G-64: VerbalHandoffWithIncomingShiftLead",
                      by("OutgoingTechnician"), leaf=True)
    # G-65 [01:59:45] "capture the machine condition, isolation status, work completed, and next
    #       action while the repair is still open"; [02:00:20] the temporary seal was not recorded
    g65 = MaintainGoal("G-65: OpenRepairStateRecordedWhileOpen",
                       by("OutgoingTechnician"), leaf=True)
    # G-66 [01:58:37] "I need the open repair and its next action to be immediately visible by machine and shift"
    g66 = AchieveGoal("G-66: OpenRepairsAndNextActionVisibleByMachineAndShift",
                      by("MaintenanceTablet", True), leaf=True)
    # G-45 [02:00:20] "the day shift didn't know that and started troubleshooting from the beginning"
    #      OR-refinement (H6): verbal handoff (good context, not auditable) vs. system record
    #      (auditable; Angela's stated preference at [01:59:45]).
    g45 = AvoidGoal("G-45: RepairRestartedFromScratch <b>If</b> ShiftChangesDuringRepair", None,
                    [Refinement(False, [g64], "H6"),
                     Refinement(False, [g65, g66], "H6")])

    # ---------------- Alerts ----------------
    # G-69 [02:06:05] "a pressure trend crossing a defined limit or a critical machine stopping
    #       unexpectedly ... include the machine, severity, likely condition, and recommended next action"
    g69 = AchieveGoal("G-69: AlertWithSeverityAndNextActionSent <b>If</b> LimitCrossedOrCriticalStop",
                      by("MaintenanceTablet", True), leaf=True)
    # G-70 [02:06:05] "avoid ... sending alerts when the machine is intentionally down for planned maintenance"
    g70 = AvoidGoal("G-70: AlertSent <b>If</b> MachineInPlannedMaintenance",
                    by("MaintenanceTablet", True), leaf=True)
    # G-71 [02:06:05] "avoid repeating every minor fluctuation"
    g71 = AvoidGoal("G-71: RepeatedAlertsForMinorFluctuation",
                    by("MaintenanceTablet", True), leaf=True)
    # G-68 [02:06:05] "An alert is useful when it indicates a condition that needs action"
    #      H10: converse of the conditional alert goal (no alert when no action is needed).
    g68 = AchieveGoal("G-68: ActionableAlertSent <b>If</b> ConditionNeedsAction", None,
                      [Refinement(False, [g69, g70, g71], "H10")])

    # ---------------- Roots ----------------
    # G-40 [01:50:53] "Keeping the critical machines running and reducing unplanned downtime"
    #      [01:52:25] "sustained reduction in unplanned downtime minutes, fewer repeat failures,
    #      and improved mean time between failures"
    g40 = SoftGoal("Reduce[G-40: UnplannedDowntimeOnCriticalMachines]", None,
                   [Refinement(False, [g41, g42, g43, g44, g45, g68], "H4")])

    # G-67 [01:59:11] "every repair has to be traceable for customer audits"
    g67 = SoftGoal("Increase[G-67: RepairTraceabilityForCustomerAudits]", None,
                   [Refinement(False, [g48, g65], "H6")])

    # G-73 [02:07:37] "dirty or wet gloves, and being in a noisy area where technicians can't easily hear prompts"
    g73 = AchieveGoal("G-73: EntriesUsableWithGlovesAndInNoise",
                      by("MaintenanceTablet", True), leaf=True)
    # G-72 [02:10:08] "practical enough for technicians to use during a live breakdown";
    #      [02:07:37] "can't stop to type a long explanation while a machine is down"
    g72 = SoftGoal("Minimize[G-72: TechnicianEntryEffortDuringBreakdown]", None,
                   [Refinement(False, [g54, g73], "H3")])

    # ---------------- Obstacles (H8) and conflicts ----------------
    # O [02:08:07] "a technician can lose the record or delay the repair when the tablet can't reach the system"
    o_net = Obstacle("TabletLosesConnectivity", annotation="H8")
    # O [01:53:42] "Teo's priority was getting Press 17 producing again, so the repair was closed
    #   ... without selecting the reason code"
    o_skip = Obstacle("ReasonCodeSkippedToRestoreProduction", annotation="H8")

    links = [
        ObstructionLink(g41, o_net),
        ResolutionLink(g50, o_net),
        ObstructionLink(g47, o_skip),
        ResolutionLink(g55, o_skip),
        # Angela's own tension: required fields before closure (G-55) vs. minimal entry
        # effort during a breakdown (G-72). Unstated condition: required at closure, not while down.
        ConflictLink(g55, g72),
    ]
    tacit = [g74]
    return [g40, g67, g72], links, tacit


def render(roots, links, tacit):
    output = generate_graph(roots, links)
    output += "".join(f"style {g.get_node_id()} {YELLOW}\n" for g in tacit)
    return output


if __name__ == "__main__":
    output = render(*build())
    print(output)
    print(generate_pako_link(output))
