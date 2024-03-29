# This file is generated by gyp; do not edit.

include $(CLEAR_VARS)

LOCAL_MODULE_CLASS := GYP
LOCAL_MODULE := third_party_WebKit_Source_devtools_frontend_protocol_sources_gyp
LOCAL_MODULE_STEM := frontend_protocol_sources
LOCAL_MODULE_SUFFIX := .stamp
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_TARGET_ARCH := $(TARGET_$(GYP_VAR_PREFIX)ARCH)
gyp_intermediate_dir := $(call local-intermediates-dir,,$(GYP_VAR_PREFIX))
gyp_shared_intermediate_dir := $(call intermediates-dir-for,GYP,shared,,,$(GYP_VAR_PREFIX))

# Make sure our deps are built first.
GYP_TARGET_DEPENDENCIES :=

### Rules for action "generateInspectorProtocolFrontendSources":
$(gyp_shared_intermediate_dir)/blink/devtools/InspectorBackendCommands.js: gyp_local_path := $(LOCAL_PATH)
$(gyp_shared_intermediate_dir)/blink/devtools/InspectorBackendCommands.js: gyp_var_prefix := $(GYP_VAR_PREFIX)
$(gyp_shared_intermediate_dir)/blink/devtools/InspectorBackendCommands.js: gyp_intermediate_dir := $(abspath $(gyp_intermediate_dir))
$(gyp_shared_intermediate_dir)/blink/devtools/InspectorBackendCommands.js: gyp_shared_intermediate_dir := $(abspath $(gyp_shared_intermediate_dir))
$(gyp_shared_intermediate_dir)/blink/devtools/InspectorBackendCommands.js: export PATH := $(subst $(ANDROID_BUILD_PATHS),,$(PATH))
$(gyp_shared_intermediate_dir)/blink/devtools/InspectorBackendCommands.js: $(LOCAL_PATH)/third_party/WebKit/Source/devtools/scripts/CodeGeneratorFrontend.py $(LOCAL_PATH)/third_party/WebKit/Source/devtools/protocol.json $(GYP_TARGET_DEPENDENCIES)
	@echo "Gyp action: Generating Inspector protocol frontend sources from protocol.json ($@)"
	$(hide)cd $(gyp_local_path)/third_party/WebKit/Source/devtools; mkdir -p $(gyp_shared_intermediate_dir)/blink/devtools; python scripts/CodeGeneratorFrontend.py protocol.json --output_js_dir "$(gyp_shared_intermediate_dir)/blink/devtools"



GYP_GENERATED_OUTPUTS := \
	$(gyp_shared_intermediate_dir)/blink/devtools/InspectorBackendCommands.js

# Make sure our deps and generated files are built first.
LOCAL_ADDITIONAL_DEPENDENCIES := $(GYP_TARGET_DEPENDENCIES) $(GYP_GENERATED_OUTPUTS)

### Rules for final target.
# Add target alias to "gyp_all_modules" target.
.PHONY: gyp_all_modules
gyp_all_modules: third_party_WebKit_Source_devtools_frontend_protocol_sources_gyp

# Alias gyp target name.
.PHONY: frontend_protocol_sources
frontend_protocol_sources: third_party_WebKit_Source_devtools_frontend_protocol_sources_gyp

LOCAL_MODULE_PATH := $(PRODUCT_OUT)/gyp_stamp
LOCAL_UNINSTALLABLE_MODULE := true
LOCAL_2ND_ARCH_VAR_PREFIX := $(GYP_VAR_PREFIX)

include $(BUILD_SYSTEM)/base_rules.mk

$(LOCAL_BUILT_MODULE): $(LOCAL_ADDITIONAL_DEPENDENCIES)
	$(hide) echo "Gyp timestamp: $@"
	$(hide) mkdir -p $(dir $@)
	$(hide) touch $@

LOCAL_2ND_ARCH_VAR_PREFIX :=
