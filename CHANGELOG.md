# Changelog

## [v2.2.0]
- Supporting a user_data in server for system configuration on first boot

## [v2.1.0]
- Fixing version

## [v1.1.6]
- Modify the link to example

## [v1.1.5] 

- Add get_certificates()
- Add create_certificate()
- Add get_certificate()
- Add delete_certificate()
- Add project_level_usage_get()
- Add project_level_server_usage_get()
- Add project_level_distributed_storage_usage_get()
- Add project_level_rocket_storage_usage_get()
- Add project_level_storage_backup_usage_get()
- Add project_level_snapshot_usage_get()
- Add project_level_template_usage_get()
- Add project_level_isoimage_usage_get()
- Add project_level_ip_usage_get()
- Add project_level_loadbalancer_usage_get()
- Add project_level_paas_service_usage_get()
- Add contract_level_usage_get()
- Add contract_level_server_usage_get()
- Add contract_level_distributed_storage_usage_get()
- Add contract_level_rocket_storage_usage_get()
- Add contract_level_storage_backup_usage_get()
- Add contract_level_snapshot_usage_get()
- Add contract_level_template_usage_get()
- Add contract_level_isoimage_usage_get()
- Add contract_level_ip_usage_get()
- Add contract_level_loadbalancer_usage_get()
- Add contract_level_paas_service_usage_get()
- Add get_network_pinned_servers()
- Add update_network_pinned_server()
- Add delete_network_pinned_server()
- Update create_access_key() -> Accept comment as a request parameter
- Fixed polling method in create_paas_security_zone()
- Fixed polling method in get_paas_security_zone()
- Fixed polling method in get_paas_security_zones()
- Fixed polling method in update_paas_security_zone()
- Fixed polling method in update_paas_security_zone()
- Fixed get_buckets() response
- Removed get_location_ips()
- Removed get_location_isoimages()
- Removed get_location_networks()
- Removed get_location_servers()
- Removed get_location_snapshots()
- Removed get_location_storages()
- Removed get_location_templates()

## [v1.1.4] 

- Add create_location()
- Add delete_location()
- Add update_location()
- Update paas_service_update() endpoint to include optional paas_service_template_uuid

## [v1.1.3] 

- Fix missing depecrated require parameter in loadbalancer_update() schema


## [v1.1.2] 

- Make loadbalancer_update() parameters non-required

## [v1.1.1] 

- Add missing information in changelog
- Fix readme

## [v1.1.0] 

- Add get_storage_backups()
- Add delete_storage_backup()
- Add rollback_storage_backup()
- Add get_storage_backup_schedules()
- Add create_storage_backup_schedule()
- Add get_storage_backup_schedule()
- Add delete_storage_backup_schedule()
- Add update_storage_backup_schedule()
- Replace get_marketplace_templates() with get_marketplace_applications()
- Replace get_marketplace_template() with get_marketplace_application()
- Replace create_marketplace_template() with create_marketplace_application()
- Replace update_marketplace_template() with update_marketplace_application()
- Replace delete_marketplace_template() with delete_marketplace_application()
- Replace get_marketplace_template_events() with get_marketplace_application_events()
- Update credential attributes in paas_service_add() endpoint

## [v1.0.3] 

- Add storage_clone() endpoint
- Add get_deleted_loadbalancers() endpoint
- Add renew_paas_service_credentials() endpoint
- Remove deprecated create_label() and delete_label() endpoints

## [v1.0.2] 

- Fix synchronous client behaviour for delete_loadbalancer() endpoint
- Add get_label() endpoint

## [v1.0.1] 

- Initial release

