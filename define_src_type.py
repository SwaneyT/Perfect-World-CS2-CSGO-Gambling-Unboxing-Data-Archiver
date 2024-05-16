### DEFINE WHAT TYPE THE SRC IS... CAPSULE, CASE ETC ###


def defineSrcType(src):
    src = src.lower()
    ### PINS CAPSULE ###
    if "pins capsule" in src:
        src_type = "Pins Capsule"
    ### PATCH PACK ###
    elif "patch pack" in src:
        src_type = "Patch Pack"
    ### MUSIC KIT BOX ###
    elif "music kit box" in src or "StatTrak" and "box" in src:
        src_type = "Music Kit Box"
    ### GRAFITTI BOX ###
    elif "graffiti box" in src:
        src_type = "Graffiti Box"
    ### SOUVENIR PACKAGE ###
    elif "souvenir package" in src:
        src_type = "Souvenir Package"
    ### CASE ###
    elif any(substring in src for substring in["case", "x-ray p250 package"]):
        src_type = "Case"
    ### STICKER CAPSULE ###
    elif "collection package" in src:
        src_type = "Collection Package"
    elif any(substring in src for substring in["sticker capsule", "autograph capsule", "capsule", "2020 rmr", "dreamhack cluj-napoca 2015 challengers (foil)", "dreamhack cluj-napoca 2015 legends (foil)", "(holo-foil)"]):
        src_type = "Sticker Capsule"
    ### OTHER EDGE CASE SCENARIO ###
    else:
        src_type = "Other"

    return src_type