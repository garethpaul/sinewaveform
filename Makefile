.PHONY: build check lint test verify

PYTHON ?= python3
RUBY ?= ruby
XCODEBUILD ?= xcodebuild

lint:
	$(RUBY) -c SineWaveform.podspec
	$(PYTHON) scripts/check-sinewaveform-source.py --mode package

test:
	$(PYTHON) scripts/check-sinewaveform-source.py --mode waveform

build: lint
	@if command -v "$(XCODEBUILD)" >/dev/null 2>&1; then \
		"$(XCODEBUILD)" -project SineWaveform.xcodeproj -target SineWaveform -sdk iphonesimulator CODE_SIGNING_ALLOWED=NO build; \
	else \
		echo "xcodebuild not found; static package checks completed"; \
	fi

verify: lint test build

check: verify
