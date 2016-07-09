import UIKit
import Darwin

let pi = M_PI

@IBDesignable
public class SiriWaveformView: UIView {
    private var _phase: CGFloat = 0.0
    private var _amplitude: CGFloat = 0.0
    
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
        _phase += phaseShift
        _amplitude = fmax(level, idleAmplitude)
        setNeedsDisplay()
    }
    
    override public func drawRect(rect: CGRect) {
        let context = UIGraphicsGetCurrentContext()
        CGContextClearRect(context, bounds)
        
        backgroundColor?.set()
        CGContextFillRect(context, rect)
        
        for waveNumber in 0...numOfWaves {
            let context = UIGraphicsGetCurrentContext()
            
            CGContextSetLineWidth(context, (waveNumber == 0 ? primaryWaveLineWidth : secondaryWaveLineWidth))
            
            let halfHeight = CGRectGetHeight(bounds) / 2.0
            let width = CGRectGetWidth(bounds)
            let mid = width / 2.0
            
            let maxAmplitude = halfHeight - 4.0 // 4 corresponds to twice the stroke width
            let progress: CGFloat = 1.0 - CGFloat(waveNumber) / CGFloat(numOfWaves)
            let normedAmplitude = (1.5 * progress - 0.5) * amplitude
            let multiplier: CGFloat = 1.0
            waveColor.colorWithAlphaComponent(multiplier * CGColorGetAlpha(waveColor.CGColor)).set()
            
            var x: CGFloat = 0.0
            while x < width + density {
                let scaling = -pow(1 / mid * (x - mid), 2) + 1
                let tempCasting: CGFloat = 2.0 * CGFloat(pi) * CGFloat(x / width) * frequency + _phase
                let y = scaling * maxAmplitude * normedAmplitude * CGFloat(sinf(Float(tempCasting))) + halfHeight
                if x == 0 {
                    CGContextMoveToPoint(context, x, y)
                } else {
                    CGContextAddLineToPoint(context, x, y)
                }
                x += density
            }
            CGContextStrokePath(context)
        }
    }
}