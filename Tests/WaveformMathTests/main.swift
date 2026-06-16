import Foundation

private var failureCount = 0

private func expectEqual(
    _ actual: CGFloat,
    _ expected: CGFloat,
    accuracy: CGFloat = 0.000_001,
    _ message: String
) {
    if !actual.isFinite || abs(actual - expected) > accuracy {
        failureCount += 1
        fputs("FAIL: \(message): expected \(expected), got \(actual)\n", stderr)
    }
}

expectEqual(
    WaveformMath.normalizedValue(.nan, minimum: -1.0, maximum: 1.0, fallback: 0.25),
    0.25,
    "NaN uses the caller-provided fallback"
)
expectEqual(
    WaveformMath.normalizedValue(.infinity, minimum: -1.0, maximum: 1.0, fallback: 0.0),
    1.0,
    "positive infinity clamps to the maximum"
)
expectEqual(
    WaveformMath.normalizedValue(-.infinity, minimum: -1.0, maximum: 1.0, fallback: 0.0),
    -1.0,
    "negative infinity clamps to the minimum"
)
expectEqual(WaveformMath.normalizedUnitValue(-0.5), 0.0, "unit values clamp below zero")
expectEqual(WaveformMath.normalizedUnitValue(1.5), 1.0, "unit values clamp above one")

let phaseCycle = CGFloat(2.0 * Double.pi)
expectEqual(
    WaveformMath.normalizedPhase(phaseCycle + 0.5, cycle: phaseCycle),
    0.5,
    "positive phase wraps into one cycle"
)
expectEqual(
    WaveformMath.normalizedPhase(-0.5, cycle: phaseCycle),
    phaseCycle - 0.5,
    "negative phase wraps into one cycle"
)

expectEqual(
    WaveformMath.sampleStep(width: 8190.0, step: 1.0, maximumSampleIntervalCount: 4095),
    2.0,
    "wide views increase the step to preserve the sample budget"
)
expectEqual(
    WaveformMath.sampleStep(width: 100.0, step: 4.0, maximumSampleIntervalCount: 4095),
    4.0,
    "normal widths retain the configured step"
)
expectEqual(
    WaveformMath.sampleX(index: 7, accumulatedX: 28.0, width: 100.0, maximumSampleIntervalCount: 4095),
    28.0,
    "interior samples retain their accumulated coordinate"
)
expectEqual(
    WaveformMath.sampleX(index: 4095, accumulatedX: 8190.0, width: 8191.0, maximumSampleIntervalCount: 4095),
    8191.0,
    "the final budgeted sample lands exactly on the right edge"
)
expectEqual(
    WaveformMath.sampleX(index: 50, accumulatedX: 105.0, width: 100.0, maximumSampleIntervalCount: 4095),
    100.0,
    "overshooting samples clamp to the right edge"
)

if failureCount > 0 {
    exit(1)
}

print("WaveformMath behavioral tests passed")
