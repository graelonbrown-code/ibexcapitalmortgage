# State data used on state pages.
# districts: federal bankruptcy court districts in the state (stable; verify before launch).
# fed_choice: state lets filers choose federal exemptions instead of state ones
#   (from general knowledge — have the bankruptcy attorney confirm before launch).
# region: used only to vary copy.

STATES = [
    ("Alabama", "AL", ["Northern", "Middle", "Southern"], False, "South"),
    ("Alaska", "AK", [], True, "West"),
    ("Arizona", "AZ", [], False, "West"),
    ("Arkansas", "AR", ["Eastern", "Western"], True, "South"),
    ("California", "CA", ["Northern", "Eastern", "Central", "Southern"], False, "West"),
    ("Colorado", "CO", [], False, "West"),
    ("Connecticut", "CT", [], True, "Northeast"),
    ("Delaware", "DE", [], False, "Northeast"),
    ("Florida", "FL", ["Northern", "Middle", "Southern"], False, "South"),
    ("Georgia", "GA", ["Northern", "Middle", "Southern"], False, "South"),
    ("Hawaii", "HI", [], True, "West"),
    ("Idaho", "ID", [], False, "West"),
    ("Illinois", "IL", ["Northern", "Central", "Southern"], False, "Midwest"),
    ("Indiana", "IN", ["Northern", "Southern"], False, "Midwest"),
    ("Iowa", "IA", ["Northern", "Southern"], False, "Midwest"),
    ("Kansas", "KS", [], False, "Midwest"),
    ("Kentucky", "KY", ["Eastern", "Western"], True, "South"),
    ("Louisiana", "LA", ["Eastern", "Middle", "Western"], False, "South"),
    ("Maine", "ME", [], False, "Northeast"),
    ("Maryland", "MD", [], False, "Northeast"),
    ("Massachusetts", "MA", [], True, "Northeast"),
    ("Michigan", "MI", ["Eastern", "Western"], True, "Midwest"),
    ("Minnesota", "MN", [], True, "Midwest"),
    ("Mississippi", "MS", ["Northern", "Southern"], False, "South"),
    ("Missouri", "MO", ["Eastern", "Western"], False, "Midwest"),
    ("Montana", "MT", [], False, "West"),
    ("Nebraska", "NE", [], False, "Midwest"),
    ("Nevada", "NV", [], False, "West"),
    ("New Hampshire", "NH", [], True, "Northeast"),
    ("New Jersey", "NJ", [], True, "Northeast"),
    ("New Mexico", "NM", [], True, "West"),
    ("New York", "NY", ["Northern", "Southern", "Eastern", "Western"], True, "Northeast"),
    ("North Carolina", "NC", ["Eastern", "Middle", "Western"], False, "South"),
    ("North Dakota", "ND", [], False, "Midwest"),
    ("Ohio", "OH", ["Northern", "Southern"], False, "Midwest"),
    ("Oklahoma", "OK", ["Northern", "Eastern", "Western"], False, "South"),
    ("Oregon", "OR", [], True, "West"),
    ("Pennsylvania", "PA", ["Eastern", "Middle", "Western"], True, "Northeast"),
    ("Rhode Island", "RI", [], True, "Northeast"),
    ("South Carolina", "SC", [], False, "South"),
    ("South Dakota", "SD", [], False, "Midwest"),
    ("Tennessee", "TN", ["Eastern", "Middle", "Western"], False, "South"),
    ("Texas", "TX", ["Northern", "Southern", "Eastern", "Western"], True, "South"),
    ("Utah", "UT", [], False, "West"),
    ("Vermont", "VT", [], True, "Northeast"),
    ("Virginia", "VA", ["Eastern", "Western"], False, "South"),
    ("Washington", "WA", ["Eastern", "Western"], True, "West"),
    ("West Virginia", "WV", ["Northern", "Southern"], False, "South"),
    ("Wisconsin", "WI", ["Eastern", "Western"], True, "Midwest"),
    ("Wyoming", "WY", [], False, "West"),
]


def slug(name):
    return name.lower().replace(" ", "-")
