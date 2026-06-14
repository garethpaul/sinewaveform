.PHONY: build check lint test verify

PYTHON ?= python3
RUBY ?= ruby
XCODEBUILD ?= xcodebuild
override ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

lint:
	$(RUBY) -c "$(ROOT)/SineWaveform.podspec"
	$(PYTHON) "$(ROOT)/scripts/check-sinewaveform-source.py" --mode package

test:
	$(PYTHON) "$(ROOT)/scripts/check-sinewaveform-source.py" --mode waveform

build: lint
	@if command -v "$(XCODEBUILD)" >/dev/null 2>&1; then \
		"$(XCODEBUILD)" -project "$(ROOT)/SineWaveform.xcodeproj" -target SineWaveform -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' CODE_SIGNING_ALLOWED=NO build; \
	else \
		echo "xcodebuild not found; static package checks completed"; \
	fi

verify: lint test build

check: verify
