"""
Goal model for Teo Salinas (night-shift maintenance technician).
Source: transcript-261026-2138.csv (timestamps below are 2026-10-27, UTC, HH:MM:SS).

Conventions
- Goal IDs G-1 .. G-39 (IDs are unique across all three stakeholder models).
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
    # ---------------- Diagnose and repair (G-2 branch) ----------------
    # G-10 [01:33:55] "see the handover and machine history right at the press"
    #      [01:34:20] "see whether a problem is still open or already handled, and who worked on it"
    g10 = AchieveGoal("G-10: HandoverHistoryAndOpenStatusShownAtPress",
                      by("MaintenanceTablet", True), leaf=True)
    # G-11 [01:17:49] "I'd want to see what day shift already tested ... before I start tearing into it"
    g11 = AchieveGoal("G-11: PriorTestsCheckedBeforeTroubleshooting",
                      by("NightTechnician"), leaf=True)
    # G-5 [01:16:40] handover "tells me what the day shift saw and what they already tried"
    g5 = AchieveGoal("G-5: PriorWorkReviewed <b>If</b> PressDown", None,
                     [Refinement(False, [g10, g11], "H5")])

    # G-6 [01:33:23] "I need to get the safety confirmation done and get to the fault first"
    #     [01:17:49] "I isolated Press 7"
    g6 = AchieveGoal("G-6: PressIsolated <b>If</b> PressDown",
                     by("NightTechnician"), leaf=True)

    # G-14 [01:33:55] "check the sensor trend"; [01:30:13] "I start with the alarm history"
    g14 = AchieveGoal("G-14: AlarmHistoryAndSensorTrendShown <b>If</b> PressHasSensors",
                      by("MaintenanceTablet", True), leaf=True)
    # G-15 [01:35:26] "Some of those 1990s presses are offline and have no sensors,
    #       so I need to record what I saw and did"
    g15 = AchieveGoal("G-15: ObservationsRecordedManually <b>If Not</b> PressHasSensors",
                      by("NightTechnician"), leaf=True)
    # Domain property [01:35:26]: some presses are offline with no sensors.
    dp_sensors = DomainProperty("EachPress HasSensors <b>Or</b> IsOfflineWithoutSensors", leaf=True)
    # G-12 TACIT: intermediate goal introduced by the decomposition-by-case pattern.
    g12 = AchieveGoal("G-12: FaultEvidenceAvailable", None,
                      [Refinement(True, [g14, g15, dp_sensors], "P3")])
    # G-13 [01:30:13] "I compare it to the normal trend, not just one number"
    #      [01:31:13] "I compare the reading with what that particular press normally does"
    g13 = AchieveGoal("G-13: ReadingComparedWithPressNormalTrend",
                      by("NightTechnician"), leaf=True)
    # G-7 [01:30:13] troubleshooting sequence; [01:19:23] Press 12 diagnosis
    g7 = AchieveGoal("G-7: FaultDiagnosed", None,
                     [Refinement(False, [g12, g13], "H4")])

    # G-16 [01:34:20] "part search to show the actual bin or crib location, not just a stock number"
    g16 = AchieveGoal("G-16: SparePartBinLocationShown",
                      by("MaintenanceTablet", True), leaf=True)
    # G-17 [01:17:49] "swapped in the usual spare"; [01:19:23] "replaced it, bled the line"
    g17 = AchieveGoal("G-17: FaultyComponentReplaced",
                      by("NightTechnician"), leaf=True)
    # G-8 [01:17:49] repair of Press 7; [01:19:23] repair of Press 12
    g8 = AchieveGoal("G-8: FaultRepaired", None,
                     [Refinement(False, [g16, g17], "H7")])

    # G-18 [01:22:24] "I run a few cycles and listen for anything changing"
    g18 = AchieveGoal("G-18: TrialCyclesRunAndWatched",
                      by("NightTechnician"), leaf=True)
    # G-19 TACIT: my interpretation of [01:34:49] "Fixed means it ran a full shift without me."
    g19 = AchieveGoal("G-19: RepairClosedAsFixed <b>If</b> NoRepeatFaultDuringNextShift",
                      by("MaintenanceTablet", True), leaf=True)
    # G-20 TACIT: converse of the conditional goal G-19 (H10).
    g20 = AchieveGoal("G-20: RepairReopened <b>If</b> RepeatFaultDuringNextShift",
                      by("MaintenanceTablet", True), leaf=True)
    # G-9 [01:21:24] "watched it for a while and made sure it was holding"
    g9 = AchieveGoal("G-9: RepairVerified", None,
                     [Refinement(False, [g18, g19, g20], "H10")])

    # G-2 [01:16:40] "that can get a press running a lot sooner"; [01:34:49] "the floor doesn't wait"
    #     Milestones follow Teo's own sequence: review, isolate, diagnose, repair, verify.
    g2 = AchieveGoal("G-2: PressRestoredQuickly <b>If</b> PressDown", None,
                     [Refinement(False, [g5, g6, g7, g8, g9], "P1")])

    # ---------------- Catch failures before alarms (G-3 branch) ----------------
    # G-24 TACIT: system flags slow drift that has not yet triggered an alarm.
    #      Grounded in [01:29:05] "not enough for an alarm, but the temperature was creeping every cycle"
    g24 = AchieveGoal("G-24: DriftFromPressBaselineFlagged <b>If</b> PressHasSensors",
                      by("MaintenanceTablet", True), leaf=True)
    # G-25 [01:31:13] "A machine can sound or feel wrong before the sensor shows it"
    g25 = AchieveGoal("G-25: AbnormalSoundOrFeelNoticed",
                      by("NightTechnician"), leaf=True)
    # G-21 [01:28:27] "knowing the machines' warning signs before they become alarms"
    #      P6: sounds and feel cannot be monitored by the software, so detection is split into
    #      a software-monitorable part (sensor drift) and a technician-monitorable part.
    g21 = AchieveGoal("G-21: EarlyWarningSignDetected", None,
                      [Refinement(False, [g24, g25], "P6")])
    # G-22 [01:27:19] "I stopped Press 3, isolated it, and pulled the return-line filter"
    #      [01:29:05] "we shut it down and replaced it before it caused a bad shot"
    g22 = AchieveGoal("G-22: PressStoppedAndInspected <b>If</b> WarningSignDetected",
                      by("NightTechnician"), leaf=True)

    # G-26 [01:31:45] "I write down patterns that repeat - what the press sounded like,
    #       what the readings were doing, and what I found"
    g26 = AchieveGoal("G-26: WarningPatternRecordedForPress",
                      by("NightTechnician"), leaf=True)
    # G-27 TACIT: patterns shown with that press's history (extends G-10's history at the press).
    g27 = AchieveGoal("G-27: WarningPatternsShownWithPressHistory",
                      by("MaintenanceTablet", True), leaf=True)
    # G-28 [01:32:17] "I'd have him stand with me through a cycle and listen to the machine"
    g28 = AchieveGoal("G-28: NewTechnicianCoachedAtPress",
                      by("NightTechnician"), leaf=True)
    # G-23 [01:28:27] "that knowledge is mostly in people's heads or notebooks"
    #      OR-refinement: record it in the system, or pass it on by coaching (H6 pros/cons:
    #      a record persists but loses what is learned by ear; coaching keeps it but does not scale).
    g23 = MaintainGoal("G-23: PressSpecificWarningKnowledgeShared", None,
                       [Refinement(False, [g26, g27], "H6"),
                        Refinement(False, [g28], "H6")])

    # G-3 [01:26:52] Press 3 "if we'd kept running, it would've turned into a pressure failure"
    g3 = AvoidGoal("G-3: PressFailure <b>If</b> EarlyWarningSignPresent", None,
                   [Refinement(False, [g21, g22, g23], "H4")])

    # ---------------- Shift handover (G-34 branch) ----------------
    # G-31 / G-32 [01:24:21] "The outgoing tech points to the machine, says what was tested and
    #       changed, and the incoming tech repeats back what he's taking over."
    g31 = AchieveGoal("G-31: TestsAndChangesExplainedAtMachine",
                      by("OutgoingTechnician"), leaf=True)
    g32 = AchieveGoal("G-32: TakeoverRepeatedBack",
                      by("IncomingTechnician"), leaf=True)
    # G-29 [01:24:21] "face-to-face handover for anything that leaves a press down or needs watching"
    g29 = AchieveGoal("G-29: FaceToFaceHandoverDone <b>If</b> PressDownOrNeedsWatching", None,
                      [Refinement(False, [g31, g32], "H11")])
    # G-33 [01:23:14] "I write down what was found, what was done, and what the next shift needs to watch"
    g33 = AchieveGoal("G-33: FoundDoneAndWatchItemsRecorded",
                      by("OutgoingTechnician"), leaf=True)
    # G-30 [01:21:42] "A handover note: the strainer was replaced, the line bled, and they should watch..."
    g30 = AchieveGoal("G-30: HandoverRecordedAndShownAtPress", None,
                      [Refinement(False, [g33, g10], "H4")])
    # G-4 [01:21:59] "the next shift needs to know what changed and what could still go wrong"
    #     OR-refinement: face-to-face handover vs. recorded handover (H6).
    g4 = AchieveGoal("G-4: RepairStatusHandedOverToNextShift", None,
                     [Refinement(False, [g29], "H6"),
                      Refinement(False, [g30], "H6")])
    # G-34 [01:21:59] "Otherwise they start from zero and may repeat the same checks."
    g34 = SoftGoal("Reduce[G-34: RepeatedChecksAfterShiftChange]", None,
                   [Refinement(False, [g4], "H4")])

    # ---------------- Root ----------------
    # G-1 [01:34:49] "Fixed means it ran a full shift without me." (H12: abstracted to the plant's
    #     production purpose, the system boundary for Teo's concerns)
    g1 = MaintainGoal("G-1: PressesProducingThroughShift", None,
                      [Refinement(False, [g2, g3, g34], "H12")])

    # ---------------- Usability root (non-functional) ----------------
    # G-36 [01:32:52] "If I can't quickly add a photo or a short voice note, I'll ... go back to my notebook"
    g36 = AchieveGoal("G-36: RepairLoggedByQuickNotePhotoOrVoice",
                      by("MaintenanceTablet", True), leaf=True)
    # G-37 [01:33:23] "log every little detail before I can start isolating it, that's a problem"
    g37 = AvoidGoal("G-37: RequiredFieldsBlockingIsolation <b>If</b> PressDown",
                    by("MaintenanceTablet", True), leaf=True)
    # G-38 [01:35:26] "without the system treating missing data like a fault"
    g38 = AvoidGoal("G-38: MissingSensorDataTreatedAsFault <b>If</b> PressOffline",
                    by("MaintenanceTablet", True), leaf=True)
    # G-39 [01:33:23] "If I have to hunt for the machine, wait for a sensor page to load..."
    g39 = AchieveGoal("G-39: PressRecordOpenedWithoutSearching",
                      by("MaintenanceTablet", True), leaf=True)
    # G-35 [01:34:49] "don't make us fight the tablet while a press is down"
    g35 = SoftGoal("Minimize[G-35: TabletInterferenceDuringRepair]", None,
                   [Refinement(False, [g36, g37, g38, g39], "H3")])

    # ---------------- Obstacles (H8) ----------------
    # O [01:24:54] "I'm careful about putting my best tricks into a company record"
    o_tricks = Obstacle("TechnicianWithholdsPersonalTricksFromRecord", annotation="H8")
    # O [01:23:40] "Press 12's strainer replacement got missed once"
    o_missed = Obstacle("HandoverNoteMissedByIncomingShift", annotation="H8")
    # O [01:32:52] "I'll put it in my pocket and go back to my notebook"
    o_notebook = Obstacle("TechnicianRevertsToPaperNotebook", annotation="H8")

    links = [
        ObstructionLink(g26, o_tricks),
        ResolutionLink(g28, o_tricks),
        ObstructionLink(g4, o_missed),
        ResolutionLink(g29, o_missed),
        ObstructionLink(g30, o_notebook),
        ResolutionLink(g36, o_notebook),
    ]
    tacit = [g12, g19, g20, g24, g27]
    return [g1, g35], links, tacit


def render(roots, links, tacit):
    output = generate_graph(roots, links)
    output += "".join(f"style {g.get_node_id()} {YELLOW}\n" for g in tacit)
    return output


if __name__ == "__main__":
    output = render(*build())
    print(output)
    print(generate_pako_link(output))
