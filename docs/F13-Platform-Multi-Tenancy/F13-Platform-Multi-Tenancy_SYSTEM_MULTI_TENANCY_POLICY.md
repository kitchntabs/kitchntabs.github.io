---
layout: default
title: F13-Platform-Multi-Tenancy SYSTEM MULTI TENANCY POLICY
---

# SYSTEM MULTI TENANCY POLICY

## OVERVIEW

### Examples:
- TenancyAdmin can create resource without tenant_ids
- Created resource appears in list for TenancyAdmin
- Resource is associated with all tenancy tenants by default if not tenant_ids provided
- TenancyAdmin can create resource with specific tenant_ids, then created resource is associated only with specified tenants
- TenancyAdmin can update resource tenant_ids
- TenantAdmin/User can create and see their resources
- for all cases the tenancy_id must be resolved automatically from the user performing the operation.
- if no tenant_ids provided we will assume all the current tenants of the tenancy. 
- SystemAdmin has full control (must specify tenant_ids or tenancy_id)

## STANDARD RESOURCE POLICY:

Models should in general implement the standard multi-tenant authorization policy.

e.g: domain/app/Policies/ECommerce/{Model}Policy.php

manage() - Authorizes based on:
- SystemAdmin → always allowed
- TenancyAdmin → check tenancy_id match OR tenants pivot
- TenantAdmin → check legacy tenant_id OR tenants pivot
- delete() - Uses same logic as manage

Note: domain/app/Providers/AuthServiceProvider.php must register the implemented policy: 

## Controller implementation

should implement authorize() calls in {Model}Controller.php:

_update() → $this->authorize('manage', $item)
_delete() → $this->authorize('delete', $item)