# Copyright (c) 2013-2014 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Barbican exception subclasses
"""

import urlparse

from barbican.openstack.common import gettextutils as u

_FATAL_EXCEPTION_FORMAT_ERRORS = False


class RedirectException(Exception):
    def __init__(self, url):
        self.url = urlparse.urlparse(url)


class BarbicanException(Exception):
    """Base Barbican Exception

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """
    message = u._("An unknown exception occurred")

    def __init__(self, message=None, *args, **kwargs):
        if not message:
            message = self.message
        try:
            message = message % kwargs
        except Exception as e:
            if _FATAL_EXCEPTION_FORMAT_ERRORS:
                raise e
            else:
                # at least get the core message out if something happened
                pass
        super(BarbicanException, self).__init__(message)


class MissingArgumentError(BarbicanException):
    message = u._("Missing required argument.")


class MissingCredentialError(BarbicanException):
    message = u._("Missing required credential: %(required)s")


class BadAuthStrategy(BarbicanException):
    message = u._("Incorrect auth strategy, expected \"%(expected)s\" but "
                  "received \"%(received)s\"")


class NotFound(BarbicanException):
    message = u._("An object with the specified identifier was not found.")


class UnknownScheme(BarbicanException):
    message = u._("Unknown scheme '%(scheme)s' found in URI")


class BadStoreUri(BarbicanException):
    message = u._("The Store URI was malformed.")


class Duplicate(BarbicanException):
    message = u._("An object with the same identifier already exists.")


class StorageFull(BarbicanException):
    message = u._("There is not enough disk space on the image storage media.")


class StorageWriteDenied(BarbicanException):
    message = u._("Permission to write image storage media denied.")


class AuthBadRequest(BarbicanException):
    message = u._("Connect error/bad request to Auth service at URL %(url)s.")


class AuthUrlNotFound(BarbicanException):
    message = u._("Auth service at URL %(url)s not found.")


class AuthorizationFailure(BarbicanException):
    message = u._("Authorization failed.")


class NotAuthenticated(BarbicanException):
    message = u._("You are not authenticated.")


class Forbidden(BarbicanException):
    message = u._("You are not authorized to complete this action.")


class NotSupported(BarbicanException):
    message = u._("Operation is not supported.")


class ForbiddenPublicImage(Forbidden):
    message = u._("You are not authorized to complete this action.")


class ProtectedImageDelete(Forbidden):
    message = u._("Image %(image_id)s is protected and cannot be deleted.")


#NOTE(bcwaldon): here for backwards-compatibility, need to deprecate.
class NotAuthorized(Forbidden):
    message = u._("You are not authorized to complete this action.")


class Invalid(BarbicanException):
    message = u._("Data supplied was not valid.")


class NoDataToProcess(BarbicanException):
    message = u._("No data supplied to process.")


class InvalidSortKey(Invalid):
    message = u._("Sort key supplied was not valid.")


class InvalidFilterRangeValue(Invalid):
    message = u._("Unable to filter using the specified range.")


class ReadonlyProperty(Forbidden):
    message = u._("Attribute '%(property)s' is read-only.")


class ReservedProperty(Forbidden):
    message = u._("Attribute '%(property)s' is reserved.")


class AuthorizationRedirect(BarbicanException):
    message = u._("Redirecting to %(uri)s for authorization.")


class DatabaseMigrationError(BarbicanException):
    message = u._("There was an error migrating the database.")


class ClientConnectionError(BarbicanException):
    message = u._("There was an error connecting to a server")


class ClientConfigurationError(BarbicanException):
    message = u._("There was an error configuring the client.")


class MultipleChoices(BarbicanException):
    message = u._("The request returned a 302 Multiple Choices. This "
                  "generally means that you have not included a version "
                  "indicator in a request URI.\n\nThe body of response "
                  "returned:\n%(body)s")


class LimitExceeded(BarbicanException):
    message = u._("The request returned a 413 Request Entity Too Large. This "
                  "generally means that rate limiting or a quota threshold "
                  "was breached.\n\nThe response body:\n%(body)s")

    def __init__(self, *args, **kwargs):
        super(LimitExceeded, self).__init__(*args, **kwargs)
        self.retry_after = (int(kwargs['retry']) if kwargs.get('retry')
                            else None)


class ServiceUnavailable(BarbicanException):
    message = u._("The request returned 503 Service Unavilable. This "
                  "generally occurs on service overload or other transient "
                  "outage.")

    def __init__(self, *args, **kwargs):
        super(ServiceUnavailable, self).__init__(*args, **kwargs)
        self.retry_after = (int(kwargs['retry']) if kwargs.get('retry')
                            else None)


class ServerError(BarbicanException):
    message = u._("The request returned 500 Internal Server Error.")


class UnexpectedStatus(BarbicanException):
    message = u._("The request returned an unexpected status: %(status)s."
                  "\n\nThe response body:\n%(body)s")


class InvalidContentType(BarbicanException):
    message = u._("Invalid content type %(content_type)s")


class InvalidContentEncoding(BarbicanException):
    message = u._("Invalid content encoding %(content_encoding)s")


class PayloadDecodingError(BarbicanException):
    message = u._("Error while attempting to decode payload.")


class BadRegistryConnectionConfiguration(BarbicanException):
    message = u._("Registry was not configured correctly on API server. "
                  "Reason: %(reason)s")


class BadStoreConfiguration(BarbicanException):
    message = u._("Store %(store_name)s could not be configured correctly. "
                  "Reason: %(reason)s")


class BadDriverConfiguration(BarbicanException):
    message = u._("Driver %(driver_name)s could not be configured correctly. "
                  "Reason: %(reason)s")


class StoreDeleteNotSupported(BarbicanException):
    message = u._("Deleting images from this store is not supported.")


class StoreAddDisabled(BarbicanException):
    message = u._("Configuration for store failed. Adding images to this "
                  "store is disabled.")


class InvalidNotifierStrategy(BarbicanException):
    message = u._("'%(strategy)s' is not an available notifier strategy.")


class MaxRedirectsExceeded(BarbicanException):
    message = u._("Maximum redirects (%(redirects)s) was exceeded.")


class InvalidRedirect(BarbicanException):
    message = u._("Received invalid HTTP redirect.")


class NoServiceEndpoint(BarbicanException):
    message = u._("Response from Keystone does not contain a "
                  "Barbican endpoint.")


class RegionAmbiguity(BarbicanException):
    message = u._("Multiple 'image' service matches for region %(region)s. "
                  "This generally means that a region is required and you "
                  "have not supplied one.")


class WorkerCreationFailure(BarbicanException):
    message = u._("Server worker creation failed: %(reason)s.")


class SchemaLoadError(BarbicanException):
    message = u._("Unable to load schema: %(reason)s")


class InvalidObject(BarbicanException):
    message = u._("Provided object does not match schema "
                  "'%(schema)s': %(reason)s")

    def __init__(self, *args, **kwargs):
        super(InvalidObject, self).__init__(*args, **kwargs)
        self.invalid_property = kwargs.get('property')


class UnsupportedField(BarbicanException):
    message = u._("No support for value set on field '%(field)s' on "
                  "schema '%(schema)s': %(reason)s")

    def __init__(self, *args, **kwargs):
        super(UnsupportedField, self).__init__(*args, **kwargs)
        self.invalid_field = kwargs.get('field')


class UnsupportedHeaderFeature(BarbicanException):
    message = u._("Provided header feature is unsupported: %(feature)s")


class InUseByStore(BarbicanException):
    message = u._("The image cannot be deleted because it is in use through "
                  "the backend store outside of Barbican.")


class ImageSizeLimitExceeded(BarbicanException):
    message = u._("The provided image is too large.")
