# Changelog

## [v1.0.1] 

- Initial release

## [v1.0.2] 

- Fix synchronous client behaviour for delete_loadbalancer() endpoint
- Add get_label() endpoint

## [v1.0.3] 

- Add storage_clone() endpoint
- Add get_deleted_loadbalancers() endpoint
- Add renew_paas_service_credentials() endpoint
- Remove deprecated create_label() and delete_label() endpoints

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

## [v1.1.1] 

- Add missing information in changelog
- Fix readme

## [v1.1.2] 

- Make loadbalancer_update() parameters non-required
