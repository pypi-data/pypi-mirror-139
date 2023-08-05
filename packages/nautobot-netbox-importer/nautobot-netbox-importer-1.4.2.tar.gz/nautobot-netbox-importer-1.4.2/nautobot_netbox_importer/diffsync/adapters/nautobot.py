"""DiffSync adapter for Nautobot database."""

from uuid import UUID

from diffsync import DiffSync
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRel
from django.db import models
import structlog

from nautobot_netbox_importer.diffsync.models.abstract import NautobotBaseModel
from nautobot_netbox_importer.utils import ProgressBar
from .abstract import N2NDiffSync


IGNORED_FIELD_CLASSES = (GenericRel, GenericForeignKey, models.ManyToManyRel, models.ManyToOneRel)
"""Field types that will appear in record._meta.get_fields() but can be generally ignored.

The `*Rel` models are reverse-lookup relations and are not "real" fields on the model.

We handle GenericForeignKeys by managing their component `content_type` and `id` fields separately.
"""


class NautobotDiffSync(N2NDiffSync):
    """DiffSync adapter integrating with the Nautobot database."""

    logger = structlog.get_logger()

    def __init__(self, *args, bypass_data_validation=False, **kwargs):
        """Initialization of a NautobotDiffSync adapater instance."""
        super().__init__(*args, **kwargs)
        self.bypass_data_validation = bypass_data_validation

    def load_model(self, diffsync_model, record):  # pylint: disable=too-many-branches
        """Instantiate the given DiffSync model class from the given Django record."""
        data = {}

        # Iterate over all model fields on the Django record
        for field in record._meta.get_fields(include_hidden=True):
            if any(isinstance(field, ignored_class) for ignored_class in IGNORED_FIELD_CLASSES):
                continue

            # Get the value of this field from Django
            try:
                value = field.value_from_object(record)
            except AttributeError as exc:
                self.logger.error(f"Unable to get value_from_object for {record} {field}: {exc}")
                continue

            if field.name not in diffsync_model.fk_associations():
                # Field is a simple data type (str, int, bool) and can be used as-is with no modifications
                data[field.name] = value
                continue

            # If we got here, the field is some sort of foreign-key reference(s).
            if not value:
                # It's a null or empty list reference though, so we don't need to do anything special with it.
                data[field.name] = value
                continue

            # What's the name of the model that this is a reference to?
            target_name = diffsync_model.fk_associations()[field.name]

            if target_name == "status":
                data[field.name] = {"slug": self.status.nautobot_model().objects.get(pk=value).slug}
                continue

            # Special case: for generic foreign keys, the target_name is actually the name of
            # another field on this record that describes the content-type of this foreign key id.
            # We flag this by starting the target_name string with a '*', as if this were C or something.
            if target_name.startswith("*"):
                target_content_type_field = target_name[1:]
                target_content_type = getattr(record, target_content_type_field)
                target_name = target_content_type.model

            try:
                # Get the DiffSync model class that we know by the given target_name
                target_class = getattr(self, target_name)
            except AttributeError:
                self.logger.error("Unknown/unrecognized class name!", name=target_name)
                data[field.name] = None
                continue

            if isinstance(value, list):
                # This field is a one-to-many or many-to-many field, a list of object references.
                if issubclass(target_class, NautobotBaseModel):
                    # Replace each object reference with its appropriate primary key value
                    data[field.name] = [foreign_record.pk for foreign_record in value]
                else:
                    # Since the PKs of these built-in Django models may differ between NetBox and Nautobot,
                    # e.g., ContentTypes, replace each reference with the natural key (not PK) of the referenced model.
                    data[field.name] = [
                        self.get_by_pk(target_name, foreign_record.pk).get_identifiers() for foreign_record in value
                    ]
            elif isinstance(value, UUID):
                # Standard Nautobot UUID foreign-key reference, no transformation needed.
                data[field.name] = value
            elif isinstance(value, int):
                # Reference to a built-in model by its integer primary key.
                # Since this may not be the same value between NetBox and Nautobot (e.g., ContentType references)
                # replace the PK with the natural keys of the referenced model.
                data[field.name] = self.get_by_pk(target_name, value).get_identifiers()
            else:
                self.logger.error(f"Invalid PK value {value}")
                data[field.name] = None

        data["pk"] = record.pk
        return self.make_model(diffsync_model, data)

    def load(self):
        """Load all available and relevant data from Nautobot in the appropriate sequence."""
        self.logger.info("Loading data from Nautobot into DiffSync...")
        for modelname in ("contenttype", "permission", "status", *self.top_level):
            diffsync_model = getattr(self, modelname)
            if diffsync_model.nautobot_model().objects.exists():
                for instance in ProgressBar(
                    diffsync_model.nautobot_model().objects.all(),
                    total=diffsync_model.nautobot_model().objects.count(),
                    desc=f"{modelname:<25}",  # len("consoleserverporttemplate")
                    verbosity=self.verbosity,
                ):
                    self.load_model(diffsync_model, instance)

        self.logger.info("Data loading from Nautobot complete.")

    def restore_required_custom_fields(self, source: DiffSync):
        """Post-synchronization cleanup function to restore any 'required=True' custom field records."""
        self.logger.debug("Restoring the 'required=True' flag on any such custom fields")
        for source_customfield in source.get_all(source.customfield):
            if source_customfield.actual_required:
                # Update both the local DiffSync record (so that on the second-pass resync we again reset required=False)
                # and the Nautobot record (so that the end state is correct)
                self.get(self.customfield, source_customfield.get_unique_id()).update({"required": True})

    def sync_complete(self, source: DiffSync, *args, **kwargs):
        """Callback invoked after completing a sync operation in which changes occurred."""
        # During the sync, we intentionally marked all custom fields as "required=False"
        # so that we could sync records that predated the creation of said custom fields.
        # Now that we've updated all records that might contain custom field data,
        # only now can we re-mark any "required" custom fields as such.
        self.restore_required_custom_fields(source)

        return super().sync_complete(source, *args, **kwargs)
