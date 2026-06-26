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

    func testBackgroundLevelUpdateHandsOffToMainThread() {
        let view = SiriWaveformView(frame: CGRect(x: 0, y: 0, width: 40, height: 20))
        let backgroundReturned = DispatchSemaphore(value: 0)

        view.updateWithLevel(0.25)
        XCTAssertEqual(view.amplitude, 0.25)

        DispatchQueue.global().async {
            view.updateWithLevel(0.75)
            backgroundReturned.signal()
        }

        XCTAssertEqual(backgroundReturned.wait(timeout: .now() + 1), .success)
        XCTAssertEqual(view.amplitude, 0.25)

        let updateApplied = expectation(description: "main-thread waveform update applied")
        DispatchQueue.main.async {
            XCTAssertEqual(view.amplitude, 0.75)
            updateApplied.fulfill()
        }
        wait(for: [updateApplied], timeout: 1)
    }

    func testRenderingPropertiesInvalidateDisplay() {
        let view = SiriWaveformView(frame: CGRect(x: 0, y: 0, width: 40, height: 20))
        let mutations: [(String, (SiriWaveformView) -> Void)] = [
            ("waveColor", { $0.waveColor = .red }),
            ("numOfWaves", { $0.numOfWaves = 3 }),
            ("primaryWaveLineWidth", { $0.primaryWaveLineWidth = 4 }),
            ("secondaryWaveLineWidth", { $0.secondaryWaveLineWidth = 5 }),
            ("frequency", { $0.frequency = 2 }),
            ("density", { $0.density = 2 }),
        ]

        for (property, mutate) in mutations {
            view.layer.display()
            XCTAssertFalse(view.layer.needsDisplay(), property)

            mutate(view)

            XCTAssertTrue(view.layer.needsDisplay(), property)
        }
    }

    func testIdleWaveformStaysInCenterPixelBand() throws {
        let view = waveformFixture()

        let idleBounds = try XCTUnwrap(alphaBounds(in: render(view)))

        XCTAssertGreaterThan(idleBounds.width, 75)
        XCTAssertGreaterThanOrEqual(idleBounds.minY, 18)
        XCTAssertLessThanOrEqual(idleBounds.maxY, 22)
    }

    func testActiveWaveformOccupiesUpperAndLowerPixelBands() throws {
        let view = waveformFixture()
        view.updateWithLevel(1)

        let image = render(view)
        let activeBounds = try XCTUnwrap(alphaBounds(in: image))

        XCTAssertLessThan(activeBounds.minY, 12)
        XCTAssertGreaterThan(activeBounds.maxY, 28)
        XCTAssertEqual(try alpha(at: CGPoint(x: 0, y: 0), in: image), 0)
        XCTAssertEqual(try alpha(at: CGPoint(x: 79, y: 0), in: image), 0)
        XCTAssertEqual(try alpha(at: CGPoint(x: 0, y: 39), in: image), 0)
        XCTAssertEqual(try alpha(at: CGPoint(x: 79, y: 39), in: image), 0)
    }

    private func waveformFixture() -> SiriWaveformView {
        let view = SiriWaveformView(frame: CGRect(x: 0, y: 0, width: 80, height: 40))
        view.backgroundColor = nil
        view.waveColor = .black
        view.numOfWaves = 1
        view.primaryWaveLineWidth = 2
        view.secondaryWaveLineWidth = 2
        view.frequency = 1
        view.density = 1
        view.phaseShift = 0
        return view
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

    private func alphaBounds(in image: UIImage) throws -> CGRect? {
        let cgImage = try XCTUnwrap(image.cgImage)
        let width = cgImage.width
        let height = cgImage.height
        let bytesPerPixel = 4
        var pixels = [UInt8](repeating: 0, count: width * height * bytesPerPixel)
        let context = try XCTUnwrap(CGContext(
            data: &pixels,
            width: width,
            height: height,
            bitsPerComponent: 8,
            bytesPerRow: width * bytesPerPixel,
            space: CGColorSpaceCreateDeviceRGB(),
            bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue
        ))
        context.draw(cgImage, in: CGRect(
            x: 0,
            y: 0,
            width: CGFloat(width),
            height: CGFloat(height)
        ))

        var minimumX = width
        var minimumY = height
        var maximumX = -1
        var maximumY = -1
        for y in 0..<height {
            for x in 0..<width where pixels[(y * width + x) * bytesPerPixel + 3] != 0 {
                minimumX = min(minimumX, x)
                minimumY = min(minimumY, y)
                maximumX = max(maximumX, x)
                maximumY = max(maximumY, y)
            }
        }
        guard maximumX >= minimumX, maximumY >= minimumY else { return nil }
        return CGRect(
            x: CGFloat(minimumX),
            y: CGFloat(minimumY),
            width: CGFloat(maximumX - minimumX + 1),
            height: CGFloat(maximumY - minimumY + 1)
        )
    }
}
