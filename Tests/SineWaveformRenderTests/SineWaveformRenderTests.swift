import CoreGraphics
import UIKit
import XCTest
@testable import SineWaveform

@MainActor
final class SineWaveformRenderTests: XCTestCase {
    func testDefaultViewUsesNonopaqueCompositing() {
        let view = SiriWaveformView(frame: CGRect(x: 0, y: 0, width: 40, height: 20))

        XCTAssertFalse(view.isOpaque)
    }

    func testDecodedViewUsesNonopaqueCompositing() throws {
        let original = SiriWaveformView(frame: CGRect(x: 0, y: 0, width: 40, height: 20))
        original.isOpaque = true
        let archive = try NSKeyedArchiver.archivedData(withRootObject: original, requiringSecureCoding: false)
        let decoded = try XCTUnwrap(NSKeyedUnarchiver.unarchiveTopLevelObjectWithData(archive) as? SiriWaveformView)

        XCTAssertFalse(decoded.isOpaque)
    }

    func testNilBackgroundLeavesRenderedPixelTransparent() throws {
        let view = SiriWaveformView(frame: CGRect(x: 0, y: 0, width: 40, height: 20))
        view.backgroundColor = nil
        view.waveColor = .clear

        let image = render(view)

        XCTAssertEqual(try alpha(at: CGPoint(x: 20, y: 10), in: image), 0)
    }

    func testTranslucentBackgroundIsCompositedOnce() throws {
        let view = SiriWaveformView(frame: CGRect(x: 0, y: 0, width: 40, height: 20))
        view.backgroundColor = UIColor(red: 1, green: 0, blue: 0, alpha: 0.5)
        view.waveColor = .clear

        let renderedAlpha = try alpha(at: CGPoint(x: 20, y: 10), in: render(view))

        XCTAssertEqual(Int(renderedAlpha), 128, accuracy: 2)
    }

    private func render(_ view: UIView) -> UIImage {
        let format = UIGraphicsImageRendererFormat()
        format.opaque = false
        format.scale = 1
        return UIGraphicsImageRenderer(size: view.bounds.size, format: format).image { context in
            view.layer.render(in: context.cgContext)
        }
    }

    private func alpha(at point: CGPoint, in image: UIImage) throws -> UInt8 {
        let cgImage = try XCTUnwrap(image.cgImage)
        let crop = try XCTUnwrap(cgImage.cropping(to: CGRect(origin: point, size: CGSize(width: 1, height: 1))))
        var pixel = [UInt8](repeating: 0, count: 4)
        let context = try XCTUnwrap(CGContext(
            data: &pixel,
            width: 1,
            height: 1,
            bitsPerComponent: 8,
            bytesPerRow: 4,
            space: CGColorSpaceCreateDeviceRGB(),
            bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue
        ))
        context.draw(crop, in: CGRect(x: 0, y: 0, width: 1, height: 1))
        return pixel[3]
    }
}
