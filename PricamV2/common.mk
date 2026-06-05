JAMESDSP_PATH := vendor/Pricamera

# Soong Namespace
PRODUCT_SOONG_NAMESPACES += \
   $(PriCamera_PATH)

PRODUCT_PACKAGES += \
    PriCamera \
    libBSTFaceDetction \
    libBSTSingleAIDoc \
    libBstStick2D \
    libjniBstAiDoc \
    libjniBstSticker \
    libjni_bstbeauty \
    libjni_bstfilter \
    libjni_bstportrait \
    libjni_uvpanorama \
    libopencv_java4

