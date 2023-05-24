from fhir.resources.identifier import Identifier
from fhir.resources.humanname import HumanName
from fhir.resources.bundle import Bundle
from fhir.resources.composition import Composition
from fhir.resources.resource import Resource
from fhir.resources.meta import Meta
from datetime import datetime

bundle = Bundle(type="document")
# Set the patient identifier
identifier = Identifier()
identifier.system = "https://example.hospital.com/pr"
identifier.value = "12345"
bundle.identifier = identifier
time_now = datetime.now().astimezone(tz=None).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
print(type(time_now))
meta = Meta(versionId=1, lastUpdated=datetime.now())
bundle.meta = meta
bundle.timestamp = datetime.now()

bundle.entry = []
bundle.type = "document"
bundle_json = bundle.json()
print(bundle_json)
