.PHONY: build check lint test verify

PYTHON ?= python3
RUBY ?= ruby
SWIFTC ?= swiftc
XCODEBUILD ?= xcodebuild
TMPDIR ?= /tmp
XCODEBUILD_DERIVED_DATA_PATH ?= $(abspath $(TMPDIR)/sinewaveform-derived-data)
override ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

lint:
	$(RUBY) -c "$(ROOT)/SineWaveform.podspec"
	$(PYTHON) "$(ROOT)/scripts/check-sinewaveform-source.py" --mode package

test:
	$(PYTHON) "$(ROOT)/scripts/check-sinewaveform-source.py" --mode waveform
	@if command -v "$(SWIFTC)" >/dev/null 2>&1; then \
		SWIFTC="$(SWIFTC)" "$(ROOT)/scripts/run-waveform-math-tests.sh"; \
	else \
		echo "swiftc not found; executable waveform math tests skipped"; \
	fi

build: lint
	@if command -v "$(XCODEBUILD)" >/dev/null 2>&1; then \
		"$(XCODEBUILD)" -project "$(ROOT)/SineWaveform.xcodeproj" -scheme SineWaveform -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' -derivedDataPath "$(XCODEBUILD_DERIVED_DATA_PATH)" CODE_SIGNING_ALLOWED=NO build; \
	else \
		echo "xcodebuild not found; static package checks completed"; \
	fi

verify: lint test build

check: verify
