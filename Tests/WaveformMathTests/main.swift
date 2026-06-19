import Foundation

private let nonce = CommandLine.arguments[1]
private let forceFailure = CommandLine.arguments[2] == "force-failure"
private var assertionCount = 0
private var failureCount = 0

private func expectEqual(
    _ identifier: String,
    _ actual: CGFloat,
    _ expected: CGFloat,
    accuracy: CGFloat = 0.000_001,
    _ message: String
) {
    assertionCount += 1
    if !actual.isFinite || abs(actual - expected) > accuracy {
        failureCount += 1
        fputs("ASSERT \(nonce) \(identifier) FAIL: \(message): expected \(expected), got \(actual)\n", stderr)
        return
    }
    print("ASSERT \(nonce) \(identifier) PASS")
}

expectEqual(
    "nan-fallback",
    WaveformMath.normalizedValue(.nan, minimum: -1.0, maximum: 1.0, fallback: 0.25),
    forceFailure ? 0.50 : 0.25,
    "NaN uses the caller-provided fallback"
)
expectEqual(
    "positive-infinity",
    WaveformMath.normalizedValue(.infinity, minimum: -1.0, maximum: 1.0, fallback: 0.0),
    1.0,
    "positive infinity clamps to the maximum"
)
expectEqual(
    "negative-infinity",
    WaveformMath.normalizedValue(-.infinity, minimum: -1.0, maximum: 1.0, fallback: 0.0),
    -1.0,
    "negative infinity clamps to the minimum"
)
expectEqual("unit-lower-bound", WaveformMath.normalizedUnitValue(-0.5), 0.0, "unit values clamp below zero")
expectEqual("unit-upper-bound", WaveformMath.normalizedUnitValue(1.5), 1.0, "unit values clamp above one")

let phaseCycle = CGFloat(2.0 * Double.pi)
expectEqual(
    "positive-phase-wrap",
    WaveformMath.normalizedPhase(phaseCycle + 0.5, cycle: phaseCycle),
    0.5,
    "positive phase wraps into one cycle"
)
expectEqual(
    "negative-phase-wrap",
    WaveformMath.normalizedPhase(-0.5, cycle: phaseCycle),
    phaseCycle - 0.5,
    "negative phase wraps into one cycle"
)

expectEqual(
    "wide-sample-step",
    WaveformMath.sampleStep(width: 8190.0, step: 1.0, maximumSampleIntervalCount: 4095),
    2.0,
    "wide views increase the step to preserve the sample budget"
)
expectEqual(
    "normal-sample-step",
    WaveformMath.sampleStep(width: 100.0, step: 4.0, maximumSampleIntervalCount: 4095),
    4.0,
    "normal widths retain the configured step"
)
expectEqual(
    "interior-sample",
    WaveformMath.sampleX(index: 7, accumulatedX: 28.0, width: 100.0, maximumSampleIntervalCount: 4095),
    28.0,
    "interior samples retain their accumulated coordinate"
)
expectEqual(
    "right-edge-sample",
    WaveformMath.sampleX(index: 4095, accumulatedX: 8190.0, width: 8191.0, maximumSampleIntervalCount: 4095),
    8191.0,
    "the final budgeted sample lands exactly on the right edge"
)
expectEqual(
    "overshoot-clamp",
    WaveformMath.sampleX(index: 50, accumulatedX: 105.0, width: 100.0, maximumSampleIntervalCount: 4095),
    100.0,
    "overshooting samples clamp to the right edge"
)
expectEqual(
    "left-edge-envelope",
    WaveformMath.waveformScaling(sampleX: 0.0, midpoint: .leastNonzeroMagnitude),
    0.0,
    "tiny nonzero midpoints retain a finite left-edge envelope"
)
expectEqual(
    "center-envelope",
    WaveformMath.waveformScaling(sampleX: .leastNonzeroMagnitude, midpoint: .leastNonzeroMagnitude),
    1.0,
    "tiny nonzero midpoints retain the center envelope peak"
)
expectEqual(
    "right-edge-envelope",
    WaveformMath.waveformScaling(
        sampleX: .leastNonzeroMagnitude * 2.0,
        midpoint: .leastNonzeroMagnitude
    ),
    0.0,
    "tiny nonzero midpoints retain a finite right-edge envelope"
)

guard assertionCount == 15 else {
    fputs("ASSERT \(nonce) COUNT FAIL: expected 15, got \(assertionCount)\n", stderr)
    exit(2)
}
guard failureCount == 0 else {
    exit(1)
}

print("COMPLETE \(nonce) \(assertionCount)")
