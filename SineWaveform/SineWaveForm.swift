import UIKit
import Darwin

let pi = Double.pi

@IBDesignable
public class SiriWaveformView: UIView {
    private var _phase: CGFloat = 0.0
    private var _amplitude: CGFloat = 0.0
    private let maximumWaveCount = 32
    private let phaseCycle = CGFloat(2.0 * pi)
    private let maximumFrequency: CGFloat = 100.0
    private let maximumDensity: CGFloat = 100.0
    private let maximumLineWidth: CGFloat = 100.0
    private let maximumSamplePointCount = 4096
    
    @IBInspectable public var waveColor: UIColor = UIColor.black
    @IBInspectable public var numOfWaves = 7
    @IBInspectable public var primaryWaveLineWidth: CGFloat = 2.0
    @IBInspectable public var secondaryWaveLineWidth: CGFloat = 3.0
    @IBInspectable public var idleAmplitude: CGFloat = 0.01
    @IBInspectable public var frequency: CGFloat = 1.5
    @IBInspectable public var density: CGFloat = 4
    @IBInspectable public var phaseShift: CGFloat = -0.15
    
    @IBInspectable public var amplitude: CGFloat {
        get {
            return _amplitude
        }
    }

    public override init(frame: CGRect) {
        super.init(frame: frame)
        isOpaque = false
    }

    public required init?(coder: NSCoder) {
        super.init(coder: coder)
        isOpaque = false
    }
    
    public func updateWithLevel(_ level: CGFloat) {
        let safePhaseShift = normalizedValue(phaseShift, minimum: -phaseCycle, maximum: phaseCycle, fallback: -0.15)
        _phase = normalizedPhase(_phase + safePhaseShift)
        let normalizedLevel = normalizedUnitValue(level)
        let normalizedIdleAmplitude = normalizedValue(idleAmplitude, minimum: 0.0, maximum: 1.0, fallback: 0.01)
        _amplitude = max(normalizedLevel, normalizedIdleAmplitude)
        setNeedsDisplay()
    }

    private func normalizedUnitValue(_ value: CGFloat) -> CGFloat {
        return WaveformMath.normalizedUnitValue(value)
    }

    private func normalizedValue(_ value: CGFloat, minimum: CGFloat, maximum: CGFloat, fallback: CGFloat) -> CGFloat {
        return WaveformMath.normalizedValue(value, minimum: minimum, maximum: maximum, fallback: fallback)
    }

    private func normalizedPhase(_ phase: CGFloat) -> CGFloat {
        return WaveformMath.normalizedPhase(phase, cycle: phaseCycle)
    }
    
    override public func draw(_ rect: CGRect) {
        guard let context = UIGraphicsGetCurrentContext() else { return }
        let width = bounds.width
        let height = bounds.height
        guard width.isFinite && height.isFinite && width > 0.0 && height > 0.0 else { return }
        let midpoint = width / 2.0
        guard midpoint > 0.0 else { return }

        context.clear(bounds)

        if let backgroundColor = backgroundColor {
            context.setFillColor(backgroundColor.cgColor)
            context.fill(rect)
        }

        let waveCount = min(max(1, numOfWaves), maximumWaveCount)
        let step = normalizedValue(density, minimum: 1.0, maximum: maximumDensity, fallback: 4.0)
        let maximumSampleIntervalCount = maximumSamplePointCount - 1
        let sampleStep = WaveformMath.sampleStep(
            width: width,
            step: step,
            maximumSampleIntervalCount: maximumSampleIntervalCount
        )
        let drawFrequency = normalizedValue(frequency, minimum: -maximumFrequency, maximum: maximumFrequency, fallback: 1.5)
        let primaryLineWidth = normalizedValue(primaryWaveLineWidth, minimum: 0.0, maximum: maximumLineWidth, fallback: 2.0)
        let secondaryLineWidth = normalizedValue(secondaryWaveLineWidth, minimum: 0.0, maximum: maximumLineWidth, fallback: 3.0)
        
        for waveNumber in 0..<waveCount {
            context.setLineWidth(waveNumber == 0 ? primaryLineWidth : secondaryLineWidth)
            
            let halfHeight = height / 2.0
            
            let maxAmplitude = max(halfHeight - 4.0, 0.0) // 4 corresponds to twice the stroke width
            let progress: CGFloat = 1.0 - CGFloat(waveNumber) / CGFloat(waveCount)
            let normedAmplitude = (1.5 * progress - 0.5) * amplitude
            let multiplier: CGFloat = 1.0
            waveColor.withAlphaComponent(multiplier * waveColor.cgColor.alpha).set()
            
            var x: CGFloat = 0.0
            var sampleIndex = 0
            while true {
                let sampleX = WaveformMath.sampleX(
                    index: sampleIndex,
                    accumulatedX: x,
                    width: width,
                    maximumSampleIntervalCount: maximumSampleIntervalCount
                )
                let scaling = WaveformMath.waveformScaling(sampleX: sampleX, midpoint: midpoint)
                let tempCasting: CGFloat = 2.0 * CGFloat(pi) * CGFloat(sampleX / width) * drawFrequency + _phase
                let y = scaling * maxAmplitude * normedAmplitude * sin(tempCasting) + halfHeight
                if sampleX == 0 {
                    context.move(to: CGPoint(x: sampleX, y: y))
                } else {
                    context.addLine(to: CGPoint(x: sampleX, y: y))
                }
                if sampleX == width { break }
                sampleIndex += 1
                x += sampleStep
            }
            context.strokePath()
        }
    }
}
