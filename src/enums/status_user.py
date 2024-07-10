import enum


class Status(enum.Enum):
    registered = "6205cf9436aee7ccb42779ac5e69bd3f"
    active = "4d3d769b812b6faa6b76e1a8abaece2d"


class SubStatus(enum.Enum):
    registration = "0f98b7f230f3c91292f0de4c99e263f2"
    application_form = "fb6a31c11343f5c9dfc87543585956c1"
    free = "b24ce0cd392a5b0b8dedc66c25213594"
    hunty_pro = "f5eaac978aab4071819528431afa79f0"


class TypeUser:
    hunty = 1


class StageId:
    subscription_cancelled = "677254dfe1924978b329a53f6ca44772"
    alternate_form_hunty_pro = "e011473eb70e48abbb875880a2e53728"
    application_form_alternate_forms = "8eea2abf3f4ce60123c0aea07a30387e"
    failed_payment = "588ed4a8507c4381a3a3bff3d91c4160"
    active_subscription = "409d4e6652184b7a8de50b014694df7b"
