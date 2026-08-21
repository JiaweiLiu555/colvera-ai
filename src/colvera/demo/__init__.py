"""Synthetic, non-clinical fixtures for the Colvera product demonstration.

The demo layer deliberately has no model inference.  It gives the product UI a
stable, structured data source while the approved longitudinal-cohort workflow
is still separate in :mod:`colvera.longitudinal`.
"""

from .patient import DemoPatient, DemoVisit, get_demo_manifest, get_demo_patient, get_demo_patients

__all__ = ["DemoPatient", "DemoVisit", "get_demo_manifest", "get_demo_patient", "get_demo_patients"]
