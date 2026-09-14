# Odoo 18 Vehicle Rental Module (nti_vehicle_rental)

## Module Objective
This module is developed for managing daily vehicle rentals (cars, motorcycles, and trucks) for PT Neural Technologies Indonesia. It provides comprehensive features including fleet management, automated pricing calculations, state workflow transitions, and strict business validation rules.

## Models Included
- **rental.vehicle**: Master data for managing vehicle profiles, license plates, daily rates, and availability statuses.
- **rental.order**: Transactional model handling customer rentals, duration calculations, total amounts, and lifecycle approvals.

## Status Workflow
- **Rental Order Lifecycle**: Draft -> Confirmed -> Ongoing -> Returned (with a Cancellation option from Draft or Confirmed).
- **Vehicle Status**: Available, Rented, Maintenance.

## Installation & Testing
1. Clone or place the `nti_vehicle_rental` folder into your Odoo addons directory.
2. Update the Odoo Apps list and install the `nti_vehicle_rental` module.
3. Execute automated unit tests using the following command:
   ```bash
   odoo -d <database_name> -i nti_vehicle_rental --test-enable --stop-after-init