.DEFAULT_GOAL := check
.PHONY: __repository-make-authority build check contract-test lint root-test test verify
.SECONDEXPANSION:

override SHELL := /bin/sh
override .SHELLFLAGS := -c
override PYTHONDONTWRITEBYTECODE := 1
export PYTHONDONTWRITEBYTECODE
ifneq ($(filter command line,$(origin MAKEFLAGS)),)
$(error MAKEFLAGS must not be overridden for repository verification)
endif
override REPOSITORY_MAKE_FIRST_FLAGS := $(firstword $(MAKEFLAGS))
ifneq ($(filter -%,$(REPOSITORY_MAKE_FIRST_FLAGS)),)
override REPOSITORY_MAKE_FIRST_FLAGS :=
endif
override REPOSITORY_MAKE_SHORT_FLAGS := $(REPOSITORY_MAKE_FIRST_FLAGS) $(filter-out --%,$(filter -%,$(MAKEFLAGS)))
ifneq ($(findstring n,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(findstring t,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(findstring q,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(findstring i,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(filter --just-print --dry-run --recon --touch --question --ignore-errors,$(MAKEFLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(strip $(MAKEFILES)),)
$(error MAKEFILES must be empty; repository verification requires this Makefile to be loaded alone)
endif
override MAKEFILES :=
ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
override ROOT := $(shell path='$(subst ','"'"',$(value MAKEFILE_LIST))'; path=$$(printf '%s' "$$path" | /usr/bin/sed 's/^ //'); [ -f "$$path" ] || exit 1; directory=$$(/usr/bin/dirname -- "$$path"); CDPATH= cd -- "$$directory" && /bin/pwd -P)
export ROOT
ifeq ($(strip $(ROOT)),)
$(error repository Makefile path could not be resolved)
endif
override PYTHON := $(ROOT)/scripts/run-python.sh
override RUBY := $(ROOT)/scripts/run-ruby.sh
override SWIFTC := $(ROOT)/scripts/run-swiftc.sh
override XCODEBUILD := $(ROOT)/scripts/run-xcodebuild.sh
override TMPDIR := /tmp
override XCODEBUILD_DERIVED_DATA_PATH := $(TMPDIR)/sinewaveform-derived-data
override XCODETEST_DERIVED_DATA_PATH := $(TMPDIR)/sinewaveform-render-tests-derived-data
export PYTHON RUBY SWIFTC XCODEBUILD TMPDIR XCODEBUILD_DERIVED_DATA_PATH XCODETEST_DERIVED_DATA_PATH

build check contract-test lint root-test test verify: $$(if $$(filter file,$$(origin MAKEFILE_LIST)),,$$(error MAKEFILE_LIST must not be overridden))
build check contract-test lint root-test test verify: $$(if $$(shell path=$$$$(/usr/bin/printf '%s' '$$(subst ','"'"',$$(MAKEFILE_LIST))' | /usr/bin/sed 's/^ //') && [ -f "$$$$path" ] && /usr/bin/printf '%s' ok),,$$(error repository Makefile must be loaded alone))
build check contract-test lint root-test test verify: __repository-make-authority

__repository-make-authority::
	@:

lint:
	"$$RUBY" -c "$$ROOT/SineWaveform.podspec"
	"$$PYTHON" "$$ROOT/scripts/check-sinewaveform-source.py" --mode package

test:
	"$$PYTHON" "$$ROOT/scripts/check-sinewaveform-source.py" --mode waveform
	@if "$$SWIFTC" --available; then \
		"$$ROOT/scripts/run-waveform-math-tests.sh"; \
	else \
		echo "swiftc not found; executable waveform math tests skipped"; \
	fi
	@if "$$XCODEBUILD" --available; then \
		"$$ROOT/scripts/run-ios-render-tests.sh"; \
	else \
		echo "xcodebuild not found; iOS rendering tests skipped"; \
	fi

contract-test:
	"$$PYTHON" -m unittest discover -s "$$ROOT/Tests/ContractCheckerTests" -p 'test_*.py'

build: lint
	@if "$$XCODEBUILD" --available; then \
		"$$XCODEBUILD" -project "$$ROOT/SineWaveform.xcodeproj" -scheme SineWaveform -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' -derivedDataPath "$$XCODEBUILD_DERIVED_DATA_PATH" CODE_SIGNING_ALLOWED=NO build; \
	else \
		echo "xcodebuild not found; static package checks completed"; \
	fi

root-test:
	/bin/sh "$$ROOT/scripts/test-makefile-root.sh"

verify: root-test lint contract-test test build

check: verify
