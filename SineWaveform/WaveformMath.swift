import Foundation

enum WaveformMath {
    static func normalizedValue(
        _ value: CGFloat,
        minimum: CGFloat,
        maximum: CGFloat,
        fallback: CGFloat
    ) -> CGFloat {
        guard value == value else { return fallback }
        return min(max(value, minimum), maximum)
    }

    static func normalizedUnitValue(_ value: CGFloat) -> CGFloat {
        return normalizedValue(value, minimum: 0.0, maximum: 1.0, fallback: 0.0)
    }

    static func normalizedPhase(_ phase: CGFloat, cycle: CGFloat) -> CGFloat {
        let wrappedPhase = phase.truncatingRemainder(dividingBy: cycle)
        return wrappedPhase >= 0.0 ? wrappedPhase : wrappedPhase + cycle
    }

    static func sampleStep(
        width: CGFloat,
        step: CGFloat,
        maximumSampleIntervalCount: Int
    ) -> CGFloat {
        return max(step, width / CGFloat(maximumSampleIntervalCount))
    }

    static func sampleX(
        index: Int,
        accumulatedX: CGFloat,
        width: CGFloat,
        maximumSampleIntervalCount: Int
    ) -> CGFloat {
        return index == maximumSampleIntervalCount ? width : min(accumulatedX, width)
    }

    static func waveformScaling(sampleX: CGFloat, midpoint: CGFloat) -> CGFloat {
        let normalizedX = (sampleX - midpoint) / midpoint
        return -(normalizedX * normalizedX) + 1.0
    }
}
