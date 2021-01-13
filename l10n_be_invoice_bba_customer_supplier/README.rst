.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

====================================================================
Customer and Supplier invoices with Belgian structured communication
====================================================================

This module is an alternative to the 'l10n_be_invoice_bba' module of the standard addons.

Difference with this module:

- Support for Customer and Supplier invoices with digits check.

- Payment reference type

  On an invoice the 'reference_type' field can be set to 'bba' to enforce the use of the
  Belgian structured communication.

  By doing so automated processing of bank statements and outgoing payments can be
  optimised for performance, matching and transaction integrity.

- Configurable per partner

  The communication type and algorithm can be configured on the partner records thereby allowing
  to use other payment references for e.g. foreign customers or customise the payment reference for
  different customer segments.

- Localisation module

  This module has no dependancy on a localisation module (no dependancy on 'l10n_be')
  and hence can be installed with other localisation modules.

- Customisation capabilities

  The code has been designed to facilitate customisation by IT specialists with Odoo programming skills,
  e.g. to avoid duplicate structured communications (on customer invoices, sale orders, ...)
  or to use your own algorithm.

Known issues / Roadmap
======================

- Move to 'reference_type' field to a generic module to be used as a building block for Belgian
  as well as other (e.g. ISO 11649) structured communication type.

- Add migration script to migrate the reference type fields used for this purpose
  in previous versions
