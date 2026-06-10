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
    
    public func updateWithLevel(_ level: CGFloat) {
        let safePhaseShift = normalizedValue(phaseShift, minimum: -phaseCycle, maximum: phaseCycle, fallback: -0.15)
        _phase = normalizedPhase(_phase + safePhaseShift)
        let normalizedLevel = normalizedUnitValue(level)
        let normalizedIdleAmplitude = normalizedValue(idleAmplitude, minimum: 0.0, maximum: 1.0, fallback: 0.01)
        _amplitude = max(normalizedLevel, normalizedIdleAmplitude)
        setNeedsDisplay()
    }

    private func normalizedUnitValue(_ value: CGFloat) -> CGFloat {
        return normalizedValue(value, minimum: 0.0, maximum: 1.0, fallback: 0.0)
    }

    private func normalizedValue(_ value: CGFloat, minimum: CGFloat, maximum: CGFloat, fallback: CGFloat) -> CGFloat {
        guard value == value else { return fallback }
        return min(max(value, minimum), maximum)
    }

    private func normalizedPhase(_ phase: CGFloat) -> CGFloat {
        let wrappedPhase = CGFloat(fmod(Double(phase), Double(phaseCycle)))
        return wrappedPhase >= 0.0 ? wrappedPhase : wrappedPhase + phaseCycle
    }
    
    override public func draw(_ rect: CGRect) {
        guard let context = UIGraphicsGetCurrentContext() else { return }
        let width = bounds.width
        let height = bounds.height
        guard width > 0.0 && height > 0.0 else { return }

        context.clear(bounds)
        
        backgroundColor?.set()
        context.fill(rect)

        let waveCount = min(max(1, numOfWaves), maximumWaveCount)
        let step = normalizedValue(density, minimum: 1.0, maximum: maximumDensity, fallback: 4.0)
        let drawFrequency = normalizedValue(frequency, minimum: -maximumFrequency, maximum: maximumFrequency, fallback: 1.5)
        let primaryLineWidth = normalizedValue(primaryWaveLineWidth, minimum: 0.0, maximum: maximumLineWidth, fallback: 2.0)
        let secondaryLineWidth = normalizedValue(secondaryWaveLineWidth, minimum: 0.0, maximum: maximumLineWidth, fallback: 3.0)
        
        for waveNumber in 0..<waveCount {
            context.setLineWidth(waveNumber == 0 ? primaryLineWidth : secondaryLineWidth)
            
            let halfHeight = height / 2.0
            let mid = width / 2.0
            
            let maxAmplitude = max(halfHeight - 4.0, 0.0) // 4 corresponds to twice the stroke width
            let progress: CGFloat = 1.0 - CGFloat(waveNumber) / CGFloat(waveCount)
            let normedAmplitude = (1.5 * progress - 0.5) * amplitude
            let multiplier: CGFloat = 1.0
            waveColor.withAlphaComponent(multiplier * waveColor.cgColor.alpha).set()
            
            var x: CGFloat = 0.0
            while x < width + step {
                let scaling = -pow(1 / mid * (x - mid), 2) + 1
                let tempCasting: CGFloat = 2.0 * CGFloat(pi) * CGFloat(x / width) * drawFrequency + _phase
                let y = scaling * maxAmplitude * normedAmplitude * sin(tempCasting) + halfHeight
                if x == 0 {
                    context.move(to: CGPoint(x: x, y: y))
                } else {
                    context.addLine(to: CGPoint(x: x, y: y))
                }
                x += step
            }
            context.strokePath()
        }
    }
}
