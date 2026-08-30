from utils.official_warning_service import (
    get_latest_warning_for_testing,
    get_warned_areas_from_warning
)

warning = get_latest_warning_for_testing(
    "Mahaweli Ganga"
)

print("TEST WARNING:")
print(warning)

if warning:

    areas = get_warned_areas_from_warning(
        warning
    )

    print("\nEXTRACTED AREAS:")

    for area in areas:
        print("-", area)

else:
    print("No historical warning found.")