import UIKit
import Darwin

let pi = M_PI

@IBDesignable
public class SiriWaveformView: UIView {
    private var _phase: CGFloat = 0.0
    private var _amplitude: CGFloat = 0.0
    private let maximumWaveCount = 32
    private let phaseCycle = CGFloat(2.0 * pi)
    private let maximumFrequency: CGFloat = 100.0
    private let maximumDensity: CGFloat = 100.0
    private let maximumLineWidth: CGFloat = 100.0
    
    @IBInspectable public var waveColor: UIColor = UIColor.blackColor()
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
    
    public func updateWithLevel(level: CGFloat) {
        let safePhaseShift = normalizedValue(phaseShift, minimum: -phaseCycle, maximum: phaseCycle, fallback: 0.0)
        _phase = normalizedPhase(_phase + safePhaseShift)
        let normalizedLevel = normalizedUnitValue(level)
        let normalizedIdleAmplitude = normalizedUnitValue(idleAmplitude)
        _amplitude = max(normalizedLevel, normalizedIdleAmplitude)
        setNeedsDisplay()
    }

    private func normalizedUnitValue(value: CGFloat) -> CGFloat {
        return normalizedValue(value, minimum: 0.0, maximum: 1.0, fallback: 0.0)
    }

    private func normalizedValue(value: CGFloat, minimum: CGFloat, maximum: CGFloat, fallback: CGFloat) -> CGFloat {
        guard value == value else { return fallback }
        return min(max(value, minimum), maximum)
    }

    private func normalizedPhase(phase: CGFloat) -> CGFloat {
        let wrappedPhase = CGFloat(fmod(Double(phase), Double(phaseCycle)))
        return wrappedPhase >= 0.0 ? wrappedPhase : wrappedPhase + phaseCycle
    }
    
    override public func drawRect(rect: CGRect) {
        guard let context = UIGraphicsGetCurrentContext() else { return }
        let width = CGRectGetWidth(bounds)
        let height = CGRectGetHeight(bounds)
        guard width > 0.0 && height > 0.0 else { return }

        CGContextClearRect(context, bounds)
        
        backgroundColor?.set()
        CGContextFillRect(context, rect)

        let waveCount = min(max(1, numOfWaves), maximumWaveCount)
        let step = normalizedValue(density, minimum: 1.0, maximum: maximumDensity, fallback: 4.0)
        let drawFrequency = normalizedValue(frequency, minimum: -maximumFrequency, maximum: maximumFrequency, fallback: 1.5)
        let primaryLineWidth = normalizedValue(primaryWaveLineWidth, minimum: 0.0, maximum: maximumLineWidth, fallback: 2.0)
        let secondaryLineWidth = normalizedValue(secondaryWaveLineWidth, minimum: 0.0, maximum: maximumLineWidth, fallback: 3.0)
        
        for waveNumber in 0..<waveCount {
            CGContextSetLineWidth(context, (waveNumber == 0 ? primaryLineWidth : secondaryLineWidth))
            
            let halfHeight = height / 2.0
            let mid = width / 2.0
            
            let maxAmplitude = max(halfHeight - 4.0, 0.0) // 4 corresponds to twice the stroke width
            let progress: CGFloat = 1.0 - CGFloat(waveNumber) / CGFloat(waveCount)
            let normedAmplitude = (1.5 * progress - 0.5) * amplitude
            let multiplier: CGFloat = 1.0
            waveColor.colorWithAlphaComponent(multiplier * CGColorGetAlpha(waveColor.CGColor)).set()
            
            var x: CGFloat = 0.0
            while x < width + step {
                let scaling = -pow(1 / mid * (x - mid), 2) + 1
                let tempCasting: CGFloat = 2.0 * CGFloat(pi) * CGFloat(x / width) * drawFrequency + _phase
                let y = scaling * maxAmplitude * normedAmplitude * CGFloat(sinf(Float(tempCasting))) + halfHeight
                if x == 0 {
                    CGContextMoveToPoint(context, x, y)
                } else {
                    CGContextAddLineToPoint(context, x, y)
                }
                x += step
            }
            CGContextStrokePath(context)
        }
    }
}
