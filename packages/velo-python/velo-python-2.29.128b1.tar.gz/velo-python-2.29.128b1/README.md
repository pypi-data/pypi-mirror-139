# Python client for Velo
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![npm version](https://badge.fury.io/py/velo-python.svg)](https://badge.fury.io/py/velo-python) [![CircleCI](https://circleci.com/gh/velopaymentsapi/velo-python.svg?style=svg)](https://circleci.com/gh/velopaymentsapi/velo-python)
This library provides a Python client that simplifies interactions with the Velo Payments API. For full details covering the API visit our docs at [Velo Payments APIs](https://apidocs.velopayments.com). Note: some of the Velo API calls which require authorization via an access token, see the full docs on how to configure.
Throughout this document and the Velo platform the following terms are used:

* **Payor.** An entity (typically a corporation) which wishes to pay funds to one or more payees via a payout.
* **Payee.** The recipient of funds paid out by a payor.
* **Payment.** A single transfer of funds from a payor to a payee.
* **Payout.** A batch of Payments, typically used by a payor to logically group payments (e.g. by business day). Technically there need be no relationship between the payments in a payout - a single payout can contain payments to multiple payees and/or multiple payments to a single payee.
* **Sandbox.** An integration environment provided by Velo Payments which offers a similar API experience to the production environment, but all funding and payment events are simulated, along with many other services such as OFAC sanctions list checking.

## Overview

The Velo Payments API allows a payor to perform a number of operations. The following is a list of the main capabilities in a natural order of execution:

* Authenticate with the Velo platform
* Maintain a collection of payees
* Query the payor’s current balance of funds within the platform and perform additional funding
* Issue payments to payees
* Query the platform for a history of those payments

This document describes the main concepts and APIs required to get up and running with the Velo Payments platform. It is not an exhaustive API reference. For that, please see the separate Velo Payments API Reference.

## API Considerations

The Velo Payments API is REST based and uses the JSON format for requests and responses.

Most calls are secured using OAuth 2 security and require a valid authentication access token for successful operation. See the Authentication section for details.

Where a dynamic value is required in the examples below, the {token} format is used, suggesting that the caller needs to supply the appropriate value of the token in question (without including the { or } characters).

Where curl examples are given, the –d @filename.json approach is used, indicating that the request body should be placed into a file named filename.json in the current directory. Each of the curl examples in this document should be considered a single line on the command-line, regardless of how they appear in print.

## Authenticating with the Velo Platform

Once Velo backoffice staff have added your organization as a payor within the Velo platform sandbox, they will create you a payor Id, an API key and an API secret and share these with you in a secure manner.

You will need to use these values to authenticate with the Velo platform in order to gain access to the APIs. The steps to take are explained in the following:

create a string comprising the API key (e.g. 44a9537d-d55d-4b47-8082-14061c2bcdd8) and API secret (e.g. c396b26b-137a-44fd-87f5-34631f8fd529) with a colon between them. E.g. 44a9537d-d55d-4b47-8082-14061c2bcdd8:c396b26b-137a-44fd-87f5-34631f8fd529

base64 encode this string. E.g.: NDRhOTUzN2QtZDU1ZC00YjQ3LTgwODItMTQwNjFjMmJjZGQ4OmMzOTZiMjZiLTEzN2EtNDRmZC04N2Y1LTM0NjMxZjhmZDUyOQ==

create an HTTP **Authorization** header with the value set to e.g. Basic NDRhOTUzN2QtZDU1ZC00YjQ3LTgwODItMTQwNjFjMmJjZGQ4OmMzOTZiMjZiLTEzN2EtNDRmZC04N2Y1LTM0NjMxZjhmZDUyOQ==

perform the Velo authentication REST call using the HTTP header created above e.g. via curl:

```
  curl -X POST \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Basic NDRhOTUzN2QtZDU1ZC00YjQ3LTgwODItMTQwNjFjMmJjZGQ4OmMzOTZiMjZiLTEzN2EtNDRmZC04N2Y1LTM0NjMxZjhmZDUyOQ==\" \\
  'https://api.sandbox.velopayments.com/v1/authenticate?grant_type=client_credentials'
```

If successful, this call will result in a **200** HTTP status code and a response body such as:

```
  {
    \"access_token\":\"19f6bafd-93fd-4747-b229-00507bbc991f\",
    \"token_type\":\"bearer\",
    \"expires_in\":1799,
    \"scope\":\"...\"
  }
```
## API access following authentication
Following successful authentication, the value of the access_token field in the response (indicated in green above) should then be presented with all subsequent API calls to allow the Velo platform to validate that the caller is authenticated.

This is achieved by setting the HTTP Authorization header with the value set to e.g. Bearer 19f6bafd-93fd-4747-b229-00507bbc991f such as the curl example below:

```
  -H \"Authorization: Bearer 19f6bafd-93fd-4747-b229-00507bbc991f \"
```

If you make other Velo API calls which require authorization but the Authorization header is missing or invalid then you will get a **401** HTTP status response.


This Python package is automatically generated by the [OpenAPI Generator](https://openapi-generator.tech) project:

- API version: 2.29.128
- Package version: 2.29.128
- Build package: org.openapitools.codegen.languages.PythonClientCodegen

## Requirements.

Python >=3.6

## Installation & Usage
### pip install

If the python package is hosted on a repository, you can install directly using:

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import velo_payments
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import velo_payments
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python

import time
import velo_payments
from pprint import pprint
from velo_payments.api import countries_api
from velo_payments.model.inline_response401 import InlineResponse401
from velo_payments.model.payment_channel_rules_response import PaymentChannelRulesResponse
from velo_payments.model.supported_countries_response import SupportedCountriesResponse
from velo_payments.model.supported_countries_response_v2 import SupportedCountriesResponseV2
# Defining the host is optional and defaults to https://api.sandbox.velopayments.com
# See configuration.py for a list of all supported configuration parameters.
configuration = velo_payments.Configuration(
    host = "https://api.sandbox.velopayments.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure OAuth2 access token for authorization: OAuth2
configuration = velo_payments.Configuration(
    host = "https://api.sandbox.velopayments.com"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'


# Enter a context with an instance of the API client
with velo_payments.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = countries_api.CountriesApi(api_client)
    
    try:
        # List Payment Channel Country Rules
        api_response = api_instance.list_payment_channel_rules_v1()
        pprint(api_response)
    except velo_payments.ApiException as e:
        print("Exception when calling CountriesApi->list_payment_channel_rules_v1: %s\n" % e)
```

## Documentation for API Endpoints

All URIs are relative to *https://api.sandbox.velopayments.com*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*CountriesApi* | [**list_payment_channel_rules_v1**](docs/CountriesApi.md#list_payment_channel_rules_v1) | **GET** /v1/paymentChannelRules | List Payment Channel Country Rules
*CountriesApi* | [**list_supported_countries_v1**](docs/CountriesApi.md#list_supported_countries_v1) | **GET** /v1/supportedCountries | List Supported Countries
*CountriesApi* | [**list_supported_countries_v2**](docs/CountriesApi.md#list_supported_countries_v2) | **GET** /v2/supportedCountries | List Supported Countries
*CurrenciesApi* | [**list_supported_currencies_v2**](docs/CurrenciesApi.md#list_supported_currencies_v2) | **GET** /v2/currencies | List Supported Currencies
*FundingManagerApi* | [**create_ach_funding_request**](docs/FundingManagerApi.md#create_ach_funding_request) | **POST** /v1/sourceAccounts/{sourceAccountId}/achFundingRequest | Create Funding Request
*FundingManagerApi* | [**create_funding_request**](docs/FundingManagerApi.md#create_funding_request) | **POST** /v2/sourceAccounts/{sourceAccountId}/fundingRequest | Create Funding Request
*FundingManagerApi* | [**create_funding_request_v3**](docs/FundingManagerApi.md#create_funding_request_v3) | **POST** /v3/sourceAccounts/{sourceAccountId}/fundingRequest | Create Funding Request
*FundingManagerApi* | [**get_funding_account**](docs/FundingManagerApi.md#get_funding_account) | **GET** /v1/fundingAccounts/{fundingAccountId} | Get Funding Account
*FundingManagerApi* | [**get_funding_account_v2**](docs/FundingManagerApi.md#get_funding_account_v2) | **GET** /v2/fundingAccounts/{fundingAccountId} | Get Funding Account
*FundingManagerApi* | [**get_funding_accounts**](docs/FundingManagerApi.md#get_funding_accounts) | **GET** /v1/fundingAccounts | Get Funding Accounts
*FundingManagerApi* | [**get_funding_accounts_v2**](docs/FundingManagerApi.md#get_funding_accounts_v2) | **GET** /v2/fundingAccounts | Get Funding Accounts
*FundingManagerApi* | [**get_source_account**](docs/FundingManagerApi.md#get_source_account) | **GET** /v1/sourceAccounts/{sourceAccountId} | Get details about given source account.
*FundingManagerApi* | [**get_source_account_v2**](docs/FundingManagerApi.md#get_source_account_v2) | **GET** /v2/sourceAccounts/{sourceAccountId} | Get details about given source account.
*FundingManagerApi* | [**get_source_account_v3**](docs/FundingManagerApi.md#get_source_account_v3) | **GET** /v3/sourceAccounts/{sourceAccountId} | Get details about given source account.
*FundingManagerApi* | [**get_source_accounts**](docs/FundingManagerApi.md#get_source_accounts) | **GET** /v1/sourceAccounts | Get list of source accounts
*FundingManagerApi* | [**get_source_accounts_v2**](docs/FundingManagerApi.md#get_source_accounts_v2) | **GET** /v2/sourceAccounts | Get list of source accounts
*FundingManagerApi* | [**get_source_accounts_v3**](docs/FundingManagerApi.md#get_source_accounts_v3) | **GET** /v3/sourceAccounts | Get list of source accounts
*FundingManagerApi* | [**list_funding_audit_deltas**](docs/FundingManagerApi.md#list_funding_audit_deltas) | **GET** /v1/deltas/fundings | Get Funding Audit Delta
*FundingManagerApi* | [**set_notifications_request**](docs/FundingManagerApi.md#set_notifications_request) | **POST** /v1/sourceAccounts/{sourceAccountId}/notifications | Set notifications
*FundingManagerApi* | [**transfer_funds**](docs/FundingManagerApi.md#transfer_funds) | **POST** /v2/sourceAccounts/{sourceAccountId}/transfers | Transfer Funds between source accounts
*FundingManagerApi* | [**transfer_funds_v3**](docs/FundingManagerApi.md#transfer_funds_v3) | **POST** /v3/sourceAccounts/{sourceAccountId}/transfers | Transfer Funds between source accounts
*FundingManagerPrivateApi* | [**create_funding_account_v2**](docs/FundingManagerPrivateApi.md#create_funding_account_v2) | **POST** /v2/fundingAccounts | Create Funding Account
*FundingManagerPrivateApi* | [**delete_source_account_v3**](docs/FundingManagerPrivateApi.md#delete_source_account_v3) | **DELETE** /v3/sourceAccounts/{sourceAccountId} | Delete a source account by ID
*LoginApi* | [**logout**](docs/LoginApi.md#logout) | **POST** /v1/logout | Logout
*LoginApi* | [**reset_password**](docs/LoginApi.md#reset_password) | **POST** /v1/password/reset | Reset password
*LoginApi* | [**validate_access_token**](docs/LoginApi.md#validate_access_token) | **POST** /v1/validate | validate
*LoginApi* | [**velo_auth**](docs/LoginApi.md#velo_auth) | **POST** /v1/authenticate | Authentication endpoint
*PayeeInvitationApi* | [**get_payees_invitation_status_v3**](docs/PayeeInvitationApi.md#get_payees_invitation_status_v3) | **GET** /v3/payees/payors/{payorId}/invitationStatus | Get Payee Invitation Status
*PayeeInvitationApi* | [**get_payees_invitation_status_v4**](docs/PayeeInvitationApi.md#get_payees_invitation_status_v4) | **GET** /v4/payees/payors/{payorId}/invitationStatus | Get Payee Invitation Status
*PayeeInvitationApi* | [**query_batch_status_v3**](docs/PayeeInvitationApi.md#query_batch_status_v3) | **GET** /v3/payees/batch/{batchId} | Query Batch Status
*PayeeInvitationApi* | [**query_batch_status_v4**](docs/PayeeInvitationApi.md#query_batch_status_v4) | **GET** /v4/payees/batch/{batchId} | Query Batch Status
*PayeeInvitationApi* | [**resend_payee_invite_v3**](docs/PayeeInvitationApi.md#resend_payee_invite_v3) | **POST** /v3/payees/{payeeId}/invite | Resend Payee Invite
*PayeeInvitationApi* | [**resend_payee_invite_v4**](docs/PayeeInvitationApi.md#resend_payee_invite_v4) | **POST** /v4/payees/{payeeId}/invite | Resend Payee Invite
*PayeeInvitationApi* | [**v3_create_payee**](docs/PayeeInvitationApi.md#v3_create_payee) | **POST** /v3/payees | Initiate Payee Creation
*PayeeInvitationApi* | [**v4_create_payee**](docs/PayeeInvitationApi.md#v4_create_payee) | **POST** /v4/payees | Initiate Payee Creation
*PayeesApi* | [**delete_payee_by_id_v3**](docs/PayeesApi.md#delete_payee_by_id_v3) | **DELETE** /v3/payees/{payeeId} | Delete Payee by Id
*PayeesApi* | [**delete_payee_by_id_v4**](docs/PayeesApi.md#delete_payee_by_id_v4) | **DELETE** /v4/payees/{payeeId} | Delete Payee by Id
*PayeesApi* | [**get_payee_by_id_v3**](docs/PayeesApi.md#get_payee_by_id_v3) | **GET** /v3/payees/{payeeId} | Get Payee by Id
*PayeesApi* | [**get_payee_by_id_v4**](docs/PayeesApi.md#get_payee_by_id_v4) | **GET** /v4/payees/{payeeId} | Get Payee by Id
*PayeesApi* | [**list_payee_changes_v3**](docs/PayeesApi.md#list_payee_changes_v3) | **GET** /v3/payees/deltas | List Payee Changes
*PayeesApi* | [**list_payee_changes_v4**](docs/PayeesApi.md#list_payee_changes_v4) | **GET** /v4/payees/deltas | List Payee Changes
*PayeesApi* | [**list_payees_v3**](docs/PayeesApi.md#list_payees_v3) | **GET** /v3/payees | List Payees
*PayeesApi* | [**list_payees_v4**](docs/PayeesApi.md#list_payees_v4) | **GET** /v4/payees | List Payees
*PayeesApi* | [**payee_details_update_v3**](docs/PayeesApi.md#payee_details_update_v3) | **POST** /v3/payees/{payeeId}/payeeDetailsUpdate | Update Payee Details
*PayeesApi* | [**payee_details_update_v4**](docs/PayeesApi.md#payee_details_update_v4) | **POST** /v4/payees/{payeeId}/payeeDetailsUpdate | Update Payee Details
*PayeesApi* | [**v3_payees_payee_id_remote_id_update_post**](docs/PayeesApi.md#v3_payees_payee_id_remote_id_update_post) | **POST** /v3/payees/{payeeId}/remoteIdUpdate | Update Payee Remote Id
*PayeesApi* | [**v4_payees_payee_id_remote_id_update_post**](docs/PayeesApi.md#v4_payees_payee_id_remote_id_update_post) | **POST** /v4/payees/{payeeId}/remoteIdUpdate | Update Payee Remote Id
*PaymentAuditServiceApi* | [**export_transactions_csvv4**](docs/PaymentAuditServiceApi.md#export_transactions_csvv4) | **GET** /v4/paymentaudit/transactions | Export Transactions
*PaymentAuditServiceApi* | [**get_fundings_v4**](docs/PaymentAuditServiceApi.md#get_fundings_v4) | **GET** /v4/paymentaudit/fundings | Get Fundings for Payor
*PaymentAuditServiceApi* | [**get_payment_details_v4**](docs/PaymentAuditServiceApi.md#get_payment_details_v4) | **GET** /v4/paymentaudit/payments/{paymentId} | Get Payment
*PaymentAuditServiceApi* | [**get_payments_for_payout_v4**](docs/PaymentAuditServiceApi.md#get_payments_for_payout_v4) | **GET** /v4/paymentaudit/payouts/{payoutId} | Get Payments for Payout
*PaymentAuditServiceApi* | [**get_payout_stats_v4**](docs/PaymentAuditServiceApi.md#get_payout_stats_v4) | **GET** /v4/paymentaudit/payoutStatistics | Get Payout Statistics
*PaymentAuditServiceApi* | [**get_payouts_for_payor_v4**](docs/PaymentAuditServiceApi.md#get_payouts_for_payor_v4) | **GET** /v4/paymentaudit/payouts | Get Payouts for Payor
*PaymentAuditServiceApi* | [**list_payment_changes_v4**](docs/PaymentAuditServiceApi.md#list_payment_changes_v4) | **GET** /v4/payments/deltas | List Payment Changes
*PaymentAuditServiceApi* | [**list_payments_audit_v4**](docs/PaymentAuditServiceApi.md#list_payments_audit_v4) | **GET** /v4/paymentaudit/payments | Get List of Payments
*PaymentAuditServiceDeprecatedApi* | [**export_transactions_csvv3**](docs/PaymentAuditServiceDeprecatedApi.md#export_transactions_csvv3) | **GET** /v3/paymentaudit/transactions | V3 Export Transactions
*PaymentAuditServiceDeprecatedApi* | [**get_fundings_v1**](docs/PaymentAuditServiceDeprecatedApi.md#get_fundings_v1) | **GET** /v1/paymentaudit/fundings | V1 Get Fundings for Payor
*PaymentAuditServiceDeprecatedApi* | [**get_payment_details_v3**](docs/PaymentAuditServiceDeprecatedApi.md#get_payment_details_v3) | **GET** /v3/paymentaudit/payments/{paymentId} | V3 Get Payment
*PaymentAuditServiceDeprecatedApi* | [**get_payments_for_payout_pav3**](docs/PaymentAuditServiceDeprecatedApi.md#get_payments_for_payout_pav3) | **GET** /v3/paymentaudit/payouts/{payoutId} | V3 Get Payments for Payout
*PaymentAuditServiceDeprecatedApi* | [**get_payout_stats_v1**](docs/PaymentAuditServiceDeprecatedApi.md#get_payout_stats_v1) | **GET** /v1/paymentaudit/payoutStatistics | V1 Get Payout Statistics
*PaymentAuditServiceDeprecatedApi* | [**get_payouts_for_payor_v3**](docs/PaymentAuditServiceDeprecatedApi.md#get_payouts_for_payor_v3) | **GET** /v3/paymentaudit/payouts | V3 Get Payouts for Payor
*PaymentAuditServiceDeprecatedApi* | [**list_payment_changes**](docs/PaymentAuditServiceDeprecatedApi.md#list_payment_changes) | **GET** /v1/deltas/payments | V1 List Payment Changes
*PaymentAuditServiceDeprecatedApi* | [**list_payments_audit_v3**](docs/PaymentAuditServiceDeprecatedApi.md#list_payments_audit_v3) | **GET** /v3/paymentaudit/payments | V3 Get List of Payments
*PayorsApi* | [**get_payor_by_id**](docs/PayorsApi.md#get_payor_by_id) | **GET** /v1/payors/{payorId} | Get Payor
*PayorsApi* | [**get_payor_by_id_v2**](docs/PayorsApi.md#get_payor_by_id_v2) | **GET** /v2/payors/{payorId} | Get Payor
*PayorsApi* | [**payor_add_payor_logo**](docs/PayorsApi.md#payor_add_payor_logo) | **POST** /v1/payors/{payorId}/branding/logos | Add Logo
*PayorsApi* | [**payor_create_api_key_request**](docs/PayorsApi.md#payor_create_api_key_request) | **POST** /v1/payors/{payorId}/applications/{applicationId}/keys | Create API Key
*PayorsApi* | [**payor_create_application_request**](docs/PayorsApi.md#payor_create_application_request) | **POST** /v1/payors/{payorId}/applications | Create Application
*PayorsApi* | [**payor_email_opt_out**](docs/PayorsApi.md#payor_email_opt_out) | **POST** /v1/payors/{payorId}/reminderEmailsUpdate | Reminder Email Opt-Out
*PayorsApi* | [**payor_get_branding**](docs/PayorsApi.md#payor_get_branding) | **GET** /v1/payors/{payorId}/branding | Get Branding
*PayorsApi* | [**payor_links**](docs/PayorsApi.md#payor_links) | **GET** /v1/payorLinks | List Payor Links
*PayorsPrivateApi* | [**create_payor_links**](docs/PayorsPrivateApi.md#create_payor_links) | **POST** /v1/payorLinks | Create a Payor Link
*PayoutServiceApi* | [**create_quote_for_payout_v3**](docs/PayoutServiceApi.md#create_quote_for_payout_v3) | **POST** /v3/payouts/{payoutId}/quote | Create a quote for the payout
*PayoutServiceApi* | [**deschedule_payout**](docs/PayoutServiceApi.md#deschedule_payout) | **DELETE** /v3/payouts/{payoutId}/schedule | Deschedule a payout
*PayoutServiceApi* | [**get_payments_for_payout_v3**](docs/PayoutServiceApi.md#get_payments_for_payout_v3) | **GET** /v3/payouts/{payoutId}/payments | Retrieve payments for a payout
*PayoutServiceApi* | [**get_payout_summary_v3**](docs/PayoutServiceApi.md#get_payout_summary_v3) | **GET** /v3/payouts/{payoutId} | Get Payout Summary
*PayoutServiceApi* | [**instruct_payout_v3**](docs/PayoutServiceApi.md#instruct_payout_v3) | **POST** /v3/payouts/{payoutId} | Instruct Payout
*PayoutServiceApi* | [**schedule_for_payout**](docs/PayoutServiceApi.md#schedule_for_payout) | **POST** /v3/payouts/{payoutId}/schedule | Schedule a payout
*PayoutServiceApi* | [**submit_payout_v3**](docs/PayoutServiceApi.md#submit_payout_v3) | **POST** /v3/payouts | Submit Payout
*PayoutServiceApi* | [**withdraw_payment**](docs/PayoutServiceApi.md#withdraw_payment) | **POST** /v1/payments/{paymentId}/withdraw | Withdraw a Payment
*PayoutServiceApi* | [**withdraw_payout_v3**](docs/PayoutServiceApi.md#withdraw_payout_v3) | **DELETE** /v3/payouts/{payoutId} | Withdraw Payout
*TokensApi* | [**resend_token**](docs/TokensApi.md#resend_token) | **POST** /v2/users/{userId}/tokens | Resend a token
*UsersApi* | [**delete_user_by_id_v2**](docs/UsersApi.md#delete_user_by_id_v2) | **DELETE** /v2/users/{userId} | Delete a User
*UsersApi* | [**disable_user_v2**](docs/UsersApi.md#disable_user_v2) | **POST** /v2/users/{userId}/disable | Disable a User
*UsersApi* | [**enable_user_v2**](docs/UsersApi.md#enable_user_v2) | **POST** /v2/users/{userId}/enable | Enable a User
*UsersApi* | [**get_self**](docs/UsersApi.md#get_self) | **GET** /v2/users/self | Get Self
*UsersApi* | [**get_user_by_id_v2**](docs/UsersApi.md#get_user_by_id_v2) | **GET** /v2/users/{userId} | Get User
*UsersApi* | [**invite_user**](docs/UsersApi.md#invite_user) | **POST** /v2/users/invite | Invite a User
*UsersApi* | [**list_users**](docs/UsersApi.md#list_users) | **GET** /v2/users | List Users
*UsersApi* | [**register_sms**](docs/UsersApi.md#register_sms) | **POST** /v2/users/registration/sms | Register SMS Number
*UsersApi* | [**resend_token**](docs/UsersApi.md#resend_token) | **POST** /v2/users/{userId}/tokens | Resend a token
*UsersApi* | [**role_update**](docs/UsersApi.md#role_update) | **POST** /v2/users/{userId}/roleUpdate | Update User Role
*UsersApi* | [**unlock_user_v2**](docs/UsersApi.md#unlock_user_v2) | **POST** /v2/users/{userId}/unlock | Unlock a User
*UsersApi* | [**unregister_mfa**](docs/UsersApi.md#unregister_mfa) | **POST** /v2/users/{userId}/mfa/unregister | Unregister MFA for the user
*UsersApi* | [**unregister_mfa_for_self**](docs/UsersApi.md#unregister_mfa_for_self) | **POST** /v2/users/self/mfa/unregister | Unregister MFA for Self
*UsersApi* | [**update_password_self**](docs/UsersApi.md#update_password_self) | **POST** /v2/users/self/password | Update Password for self
*UsersApi* | [**user_details_update**](docs/UsersApi.md#user_details_update) | **POST** /v2/users/{userId}/userDetailsUpdate | Update User Details
*UsersApi* | [**user_details_update_for_self**](docs/UsersApi.md#user_details_update_for_self) | **POST** /v2/users/self/userDetailsUpdate | Update User Details for self
*UsersApi* | [**validate_password_self**](docs/UsersApi.md#validate_password_self) | **POST** /v2/users/self/password/validate | Validate the proposed password
*WebhooksApi* | [**create_webhook_v1**](docs/WebhooksApi.md#create_webhook_v1) | **POST** /v1/webhooks | Create Webhook
*WebhooksApi* | [**get_webhook_v1**](docs/WebhooksApi.md#get_webhook_v1) | **GET** /v1/webhooks/{webhookId} | Get details about the given webhook.
*WebhooksApi* | [**list_webhooks_v1**](docs/WebhooksApi.md#list_webhooks_v1) | **GET** /v1/webhooks | List the details about the webhooks for the given payor.
*WebhooksApi* | [**ping_webhook_v1**](docs/WebhooksApi.md#ping_webhook_v1) | **POST** /v1/webhooks/{webhookId}/ping | 
*WebhooksApi* | [**update_webhook_v1**](docs/WebhooksApi.md#update_webhook_v1) | **POST** /v1/webhooks/{webhookId} | Update Webhook


## Documentation For Models

 - [AcceptedPaymentV3](docs/AcceptedPaymentV3.md)
 - [AccessTokenResponse](docs/AccessTokenResponse.md)
 - [AccessTokenValidationRequest](docs/AccessTokenValidationRequest.md)
 - [AuthResponse](docs/AuthResponse.md)
 - [AutoTopUpConfig](docs/AutoTopUpConfig.md)
 - [AutoTopUpConfig2](docs/AutoTopUpConfig2.md)
 - [Category](docs/Category.md)
 - [Challenge](docs/Challenge.md)
 - [Challenge2](docs/Challenge2.md)
 - [Company](docs/Company.md)
 - [Company2](docs/Company2.md)
 - [CreateFundingAccountRequestV2](docs/CreateFundingAccountRequestV2.md)
 - [CreateIndividual](docs/CreateIndividual.md)
 - [CreateIndividual2](docs/CreateIndividual2.md)
 - [CreateIndividualName](docs/CreateIndividualName.md)
 - [CreatePayee](docs/CreatePayee.md)
 - [CreatePayee2](docs/CreatePayee2.md)
 - [CreatePayeeAddress](docs/CreatePayeeAddress.md)
 - [CreatePayeeAddress2](docs/CreatePayeeAddress2.md)
 - [CreatePayeesCSVRequest](docs/CreatePayeesCSVRequest.md)
 - [CreatePayeesCSVRequest2](docs/CreatePayeesCSVRequest2.md)
 - [CreatePayeesCSVResponse](docs/CreatePayeesCSVResponse.md)
 - [CreatePayeesCSVResponse2](docs/CreatePayeesCSVResponse2.md)
 - [CreatePayeesCSVResponseRejectedCsvRows](docs/CreatePayeesCSVResponseRejectedCsvRows.md)
 - [CreatePayeesRequest](docs/CreatePayeesRequest.md)
 - [CreatePayeesRequest2](docs/CreatePayeesRequest2.md)
 - [CreatePaymentChannel](docs/CreatePaymentChannel.md)
 - [CreatePaymentChannel2](docs/CreatePaymentChannel2.md)
 - [CreatePayorLinkRequest](docs/CreatePayorLinkRequest.md)
 - [CreatePayoutRequestV3](docs/CreatePayoutRequestV3.md)
 - [CreateWebhookRequest](docs/CreateWebhookRequest.md)
 - [DebitEvent](docs/DebitEvent.md)
 - [DebitEventAllOf](docs/DebitEventAllOf.md)
 - [DebitStatusChanged](docs/DebitStatusChanged.md)
 - [DebitStatusChangedAllOf](docs/DebitStatusChangedAllOf.md)
 - [Error](docs/Error.md)
 - [ErrorData](docs/ErrorData.md)
 - [ErrorResponse](docs/ErrorResponse.md)
 - [FailedPayee](docs/FailedPayee.md)
 - [FailedPayee2](docs/FailedPayee2.md)
 - [FailedSubmission](docs/FailedSubmission.md)
 - [FailedSubmission2](docs/FailedSubmission2.md)
 - [FundingAccountResponse](docs/FundingAccountResponse.md)
 - [FundingAccountResponse2](docs/FundingAccountResponse2.md)
 - [FundingAccountType](docs/FundingAccountType.md)
 - [FundingAudit](docs/FundingAudit.md)
 - [FundingEvent](docs/FundingEvent.md)
 - [FundingEventType](docs/FundingEventType.md)
 - [FundingPayorStatusAuditResponse](docs/FundingPayorStatusAuditResponse.md)
 - [FundingRequestV1](docs/FundingRequestV1.md)
 - [FundingRequestV2](docs/FundingRequestV2.md)
 - [FundingRequestV3](docs/FundingRequestV3.md)
 - [FxSummary](docs/FxSummary.md)
 - [FxSummaryV3](docs/FxSummaryV3.md)
 - [GetFundingsResponse](docs/GetFundingsResponse.md)
 - [GetFundingsResponseLinks](docs/GetFundingsResponseLinks.md)
 - [GetPayeeListResponse](docs/GetPayeeListResponse.md)
 - [GetPayeeListResponse2](docs/GetPayeeListResponse2.md)
 - [GetPayeeListResponseCompany](docs/GetPayeeListResponseCompany.md)
 - [GetPayeeListResponseCompany2](docs/GetPayeeListResponseCompany2.md)
 - [GetPayeeListResponseIndividual](docs/GetPayeeListResponseIndividual.md)
 - [GetPayeeListResponseIndividual2](docs/GetPayeeListResponseIndividual2.md)
 - [GetPaymentsForPayoutResponseV3](docs/GetPaymentsForPayoutResponseV3.md)
 - [GetPaymentsForPayoutResponseV3Page](docs/GetPaymentsForPayoutResponseV3Page.md)
 - [GetPaymentsForPayoutResponseV3Summary](docs/GetPaymentsForPayoutResponseV3Summary.md)
 - [GetPaymentsForPayoutResponseV4](docs/GetPaymentsForPayoutResponseV4.md)
 - [GetPaymentsForPayoutResponseV4Summary](docs/GetPaymentsForPayoutResponseV4Summary.md)
 - [GetPayoutStatistics](docs/GetPayoutStatistics.md)
 - [GetPayoutsResponse](docs/GetPayoutsResponse.md)
 - [GetPayoutsResponseV3](docs/GetPayoutsResponseV3.md)
 - [GetPayoutsResponseV3Links](docs/GetPayoutsResponseV3Links.md)
 - [GetPayoutsResponseV3Page](docs/GetPayoutsResponseV3Page.md)
 - [Individual](docs/Individual.md)
 - [Individual2](docs/Individual2.md)
 - [IndividualName](docs/IndividualName.md)
 - [InlineResponse400](docs/InlineResponse400.md)
 - [InlineResponse401](docs/InlineResponse401.md)
 - [InlineResponse403](docs/InlineResponse403.md)
 - [InlineResponse404](docs/InlineResponse404.md)
 - [InlineResponse409](docs/InlineResponse409.md)
 - [InlineResponse412](docs/InlineResponse412.md)
 - [InstructPayoutRequest](docs/InstructPayoutRequest.md)
 - [InvitationStatus](docs/InvitationStatus.md)
 - [InvitationStatus2](docs/InvitationStatus2.md)
 - [InvitePayeeRequest](docs/InvitePayeeRequest.md)
 - [InvitePayeeRequest2](docs/InvitePayeeRequest2.md)
 - [InviteUserRequest](docs/InviteUserRequest.md)
 - [IsoCountryCode](docs/IsoCountryCode.md)
 - [IsoCurrency](docs/IsoCurrency.md)
 - [KycState](docs/KycState.md)
 - [LinkForResponse](docs/LinkForResponse.md)
 - [ListFundingAccountsResponse](docs/ListFundingAccountsResponse.md)
 - [ListFundingAccountsResponse2](docs/ListFundingAccountsResponse2.md)
 - [ListPaymentsResponseV3](docs/ListPaymentsResponseV3.md)
 - [ListPaymentsResponseV3Page](docs/ListPaymentsResponseV3Page.md)
 - [ListPaymentsResponseV4](docs/ListPaymentsResponseV4.md)
 - [ListSourceAccountResponse](docs/ListSourceAccountResponse.md)
 - [ListSourceAccountResponseLinks](docs/ListSourceAccountResponseLinks.md)
 - [ListSourceAccountResponsePage](docs/ListSourceAccountResponsePage.md)
 - [ListSourceAccountResponseV2](docs/ListSourceAccountResponseV2.md)
 - [ListSourceAccountResponseV2Links](docs/ListSourceAccountResponseV2Links.md)
 - [ListSourceAccountResponseV3](docs/ListSourceAccountResponseV3.md)
 - [ListSourceAccountResponseV3Links](docs/ListSourceAccountResponseV3Links.md)
 - [LocalisationDetails](docs/LocalisationDetails.md)
 - [MFADetails](docs/MFADetails.md)
 - [MFAType](docs/MFAType.md)
 - [Name](docs/Name.md)
 - [Name2](docs/Name2.md)
 - [Notification](docs/Notification.md)
 - [Notifications](docs/Notifications.md)
 - [Notifications2](docs/Notifications2.md)
 - [OfacStatus](docs/OfacStatus.md)
 - [OnboardedStatus](docs/OnboardedStatus.md)
 - [OnboardedStatus2](docs/OnboardedStatus2.md)
 - [OnboardingStatusChanged](docs/OnboardingStatusChanged.md)
 - [PageForResponse](docs/PageForResponse.md)
 - [PageResourceFundingPayorStatusAuditResponseFundingPayorStatusAuditResponse](docs/PageResourceFundingPayorStatusAuditResponseFundingPayorStatusAuditResponse.md)
 - [PagedPayeeInvitationStatusResponse](docs/PagedPayeeInvitationStatusResponse.md)
 - [PagedPayeeInvitationStatusResponse2](docs/PagedPayeeInvitationStatusResponse2.md)
 - [PagedPayeeInvitationStatusResponsePage](docs/PagedPayeeInvitationStatusResponsePage.md)
 - [PagedPayeeResponse](docs/PagedPayeeResponse.md)
 - [PagedPayeeResponse2](docs/PagedPayeeResponse2.md)
 - [PagedPayeeResponseLinks](docs/PagedPayeeResponseLinks.md)
 - [PagedPayeeResponsePage](docs/PagedPayeeResponsePage.md)
 - [PagedPayeeResponseSummary](docs/PagedPayeeResponseSummary.md)
 - [PagedPaymentsResponseV3](docs/PagedPaymentsResponseV3.md)
 - [PagedUserResponse](docs/PagedUserResponse.md)
 - [PagedUserResponseLinks](docs/PagedUserResponseLinks.md)
 - [PagedUserResponsePage](docs/PagedUserResponsePage.md)
 - [PasswordRequest](docs/PasswordRequest.md)
 - [PayableIssue](docs/PayableIssue.md)
 - [PayableIssue2](docs/PayableIssue2.md)
 - [PayableStatusChanged](docs/PayableStatusChanged.md)
 - [PayeeAddress](docs/PayeeAddress.md)
 - [PayeeAddress2](docs/PayeeAddress2.md)
 - [PayeeDelta](docs/PayeeDelta.md)
 - [PayeeDelta2](docs/PayeeDelta2.md)
 - [PayeeDeltaResponse](docs/PayeeDeltaResponse.md)
 - [PayeeDeltaResponse2](docs/PayeeDeltaResponse2.md)
 - [PayeeDeltaResponse2Links](docs/PayeeDeltaResponse2Links.md)
 - [PayeeDeltaResponseLinks](docs/PayeeDeltaResponseLinks.md)
 - [PayeeDeltaResponsePage](docs/PayeeDeltaResponsePage.md)
 - [PayeeDetailResponse](docs/PayeeDetailResponse.md)
 - [PayeeDetailResponse2](docs/PayeeDetailResponse2.md)
 - [PayeeDetailsChanged](docs/PayeeDetailsChanged.md)
 - [PayeeEvent](docs/PayeeEvent.md)
 - [PayeeEventAllOf](docs/PayeeEventAllOf.md)
 - [PayeeEventAllOfReasons](docs/PayeeEventAllOfReasons.md)
 - [PayeeInvitationStatusResponse](docs/PayeeInvitationStatusResponse.md)
 - [PayeeInvitationStatusResponse2](docs/PayeeInvitationStatusResponse2.md)
 - [PayeePayorRef](docs/PayeePayorRef.md)
 - [PayeePayorRefV3](docs/PayeePayorRefV3.md)
 - [PayeeType](docs/PayeeType.md)
 - [PayeeType2](docs/PayeeType2.md)
 - [PayeeUserSelfUpdateRequest](docs/PayeeUserSelfUpdateRequest.md)
 - [PaymentAuditCurrency](docs/PaymentAuditCurrency.md)
 - [PaymentAuditCurrencyV3](docs/PaymentAuditCurrencyV3.md)
 - [PaymentChannelCountry](docs/PaymentChannelCountry.md)
 - [PaymentChannelRule](docs/PaymentChannelRule.md)
 - [PaymentChannelRulesResponse](docs/PaymentChannelRulesResponse.md)
 - [PaymentDelta](docs/PaymentDelta.md)
 - [PaymentDeltaResponse](docs/PaymentDeltaResponse.md)
 - [PaymentDeltaResponseV1](docs/PaymentDeltaResponseV1.md)
 - [PaymentDeltaV1](docs/PaymentDeltaV1.md)
 - [PaymentEvent](docs/PaymentEvent.md)
 - [PaymentEventAllOf](docs/PaymentEventAllOf.md)
 - [PaymentEventResponse](docs/PaymentEventResponse.md)
 - [PaymentEventResponseV3](docs/PaymentEventResponseV3.md)
 - [PaymentInstructionV3](docs/PaymentInstructionV3.md)
 - [PaymentRails](docs/PaymentRails.md)
 - [PaymentRejectedOrReturned](docs/PaymentRejectedOrReturned.md)
 - [PaymentRejectedOrReturnedAllOf](docs/PaymentRejectedOrReturnedAllOf.md)
 - [PaymentResponseV3](docs/PaymentResponseV3.md)
 - [PaymentResponseV4](docs/PaymentResponseV4.md)
 - [PaymentResponseV4Payout](docs/PaymentResponseV4Payout.md)
 - [PaymentStatusChanged](docs/PaymentStatusChanged.md)
 - [PaymentStatusChangedAllOf](docs/PaymentStatusChangedAllOf.md)
 - [PaymentV3](docs/PaymentV3.md)
 - [PayorAddress](docs/PayorAddress.md)
 - [PayorAddressV2](docs/PayorAddressV2.md)
 - [PayorAmlTransaction](docs/PayorAmlTransaction.md)
 - [PayorAmlTransactionV3](docs/PayorAmlTransactionV3.md)
 - [PayorBrandingResponse](docs/PayorBrandingResponse.md)
 - [PayorCreateApiKeyRequest](docs/PayorCreateApiKeyRequest.md)
 - [PayorCreateApiKeyResponse](docs/PayorCreateApiKeyResponse.md)
 - [PayorCreateApplicationRequest](docs/PayorCreateApplicationRequest.md)
 - [PayorEmailOptOutRequest](docs/PayorEmailOptOutRequest.md)
 - [PayorLinksResponse](docs/PayorLinksResponse.md)
 - [PayorLinksResponseLinks](docs/PayorLinksResponseLinks.md)
 - [PayorLinksResponsePayors](docs/PayorLinksResponsePayors.md)
 - [PayorLogoRequest](docs/PayorLogoRequest.md)
 - [PayorV1](docs/PayorV1.md)
 - [PayorV2](docs/PayorV2.md)
 - [PayoutCompanyV3](docs/PayoutCompanyV3.md)
 - [PayoutIndividualV3](docs/PayoutIndividualV3.md)
 - [PayoutNameV3](docs/PayoutNameV3.md)
 - [PayoutPayeeV3](docs/PayoutPayeeV3.md)
 - [PayoutPayor](docs/PayoutPayor.md)
 - [PayoutPayorIds](docs/PayoutPayorIds.md)
 - [PayoutPrincipal](docs/PayoutPrincipal.md)
 - [PayoutSchedule](docs/PayoutSchedule.md)
 - [PayoutSchedule2](docs/PayoutSchedule2.md)
 - [PayoutStatus](docs/PayoutStatus.md)
 - [PayoutStatusV3](docs/PayoutStatusV3.md)
 - [PayoutSummaryAudit](docs/PayoutSummaryAudit.md)
 - [PayoutSummaryAuditV3](docs/PayoutSummaryAuditV3.md)
 - [PayoutSummaryResponseV3](docs/PayoutSummaryResponseV3.md)
 - [PayoutType](docs/PayoutType.md)
 - [Ping](docs/Ping.md)
 - [PingResponse](docs/PingResponse.md)
 - [QueryBatchResponse](docs/QueryBatchResponse.md)
 - [QueryBatchResponse2](docs/QueryBatchResponse2.md)
 - [QuoteFxSummaryV3](docs/QuoteFxSummaryV3.md)
 - [QuoteResponseV3](docs/QuoteResponseV3.md)
 - [RegionV2](docs/RegionV2.md)
 - [RegisterSmsRequest](docs/RegisterSmsRequest.md)
 - [RejectedPaymentV3](docs/RejectedPaymentV3.md)
 - [ResendTokenRequest](docs/ResendTokenRequest.md)
 - [ResetPasswordRequest](docs/ResetPasswordRequest.md)
 - [Role](docs/Role.md)
 - [RoleUpdateRequest](docs/RoleUpdateRequest.md)
 - [SchedulePayoutRequest](docs/SchedulePayoutRequest.md)
 - [ScheduleStatus](docs/ScheduleStatus.md)
 - [ScheduleStatus2](docs/ScheduleStatus2.md)
 - [SelfMFATypeUnregisterRequest](docs/SelfMFATypeUnregisterRequest.md)
 - [SelfUpdatePasswordRequest](docs/SelfUpdatePasswordRequest.md)
 - [SetNotificationsRequest](docs/SetNotificationsRequest.md)
 - [SourceAccountResponse](docs/SourceAccountResponse.md)
 - [SourceAccountResponseV2](docs/SourceAccountResponseV2.md)
 - [SourceAccountResponseV3](docs/SourceAccountResponseV3.md)
 - [SourceAccountSummary](docs/SourceAccountSummary.md)
 - [SourceAccountSummaryV3](docs/SourceAccountSummaryV3.md)
 - [SourceAccountType](docs/SourceAccountType.md)
 - [SourceAccountV3](docs/SourceAccountV3.md)
 - [SourceEvent](docs/SourceEvent.md)
 - [SupportedCountriesResponse](docs/SupportedCountriesResponse.md)
 - [SupportedCountriesResponseV2](docs/SupportedCountriesResponseV2.md)
 - [SupportedCountry](docs/SupportedCountry.md)
 - [SupportedCountryV2](docs/SupportedCountryV2.md)
 - [SupportedCurrencyResponseV2](docs/SupportedCurrencyResponseV2.md)
 - [SupportedCurrencyV2](docs/SupportedCurrencyV2.md)
 - [TransferRequest](docs/TransferRequest.md)
 - [TransferRequest2](docs/TransferRequest2.md)
 - [TransmissionType](docs/TransmissionType.md)
 - [TransmissionTypes](docs/TransmissionTypes.md)
 - [TransmissionTypes2](docs/TransmissionTypes2.md)
 - [UnregisterMFARequest](docs/UnregisterMFARequest.md)
 - [UpdatePayeeDetailsRequest](docs/UpdatePayeeDetailsRequest.md)
 - [UpdatePayeeDetailsRequest2](docs/UpdatePayeeDetailsRequest2.md)
 - [UpdateRemoteIdRequest](docs/UpdateRemoteIdRequest.md)
 - [UpdateRemoteIdRequest2](docs/UpdateRemoteIdRequest2.md)
 - [UpdateWebhookRequest](docs/UpdateWebhookRequest.md)
 - [UserDetailsUpdateRequest](docs/UserDetailsUpdateRequest.md)
 - [UserInfo](docs/UserInfo.md)
 - [UserResponse](docs/UserResponse.md)
 - [UserStatus](docs/UserStatus.md)
 - [UserType](docs/UserType.md)
 - [UserType2](docs/UserType2.md)
 - [ValidatePasswordResponse](docs/ValidatePasswordResponse.md)
 - [VerificationCode](docs/VerificationCode.md)
 - [WatchlistStatus](docs/WatchlistStatus.md)
 - [WatchlistStatus2](docs/WatchlistStatus2.md)
 - [WebhookResponse](docs/WebhookResponse.md)
 - [WebhooksResponse](docs/WebhooksResponse.md)
 - [WithdrawPaymentRequest](docs/WithdrawPaymentRequest.md)


## Documentation For Authorization


## OAuth2

- **Type**: OAuth
- **Flow**: application
- **Authorization URL**: 
- **Scopes**: 
 - ** **: Scopes not required


## basicAuth

- **Type**: HTTP basic authentication


## oAuthVeloBackOffice

- **Type**: OAuth
- **Flow**: application
- **Authorization URL**: 
- **Scopes**: 
 - ** **: Scopes not required


## Author




## Notes for Large OpenAPI documents
If the OpenAPI document is large, imports in velo_payments.apis and velo_payments.models may fail with a
RecursionError indicating the maximum recursion limit has been exceeded. In that case, there are a couple of solutions:

Solution 1:
Use specific imports for apis and models like:
- `from velo_payments.api.default_api import DefaultApi`
- `from velo_payments.model.pet import Pet`

Solution 2:
Before importing the package, adjust the maximum recursion limit as shown below:
```
import sys
sys.setrecursionlimit(1500)
import velo_payments
from velo_payments.apis import *
from velo_payments.models import *
```

