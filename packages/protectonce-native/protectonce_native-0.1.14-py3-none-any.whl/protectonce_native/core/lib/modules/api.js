const _ = require('lodash');
const { Route, Api, Inventory } = require('../reports/inventory');
const { SecurityActivity } = require('../reports/security_activity');
const HeartbeatCache = require('../reports/heartbeat_cache');
const Logger = require('../utils/logger');
const toJsonSchema = require('to-json-schema');

function storeRoute(inputData) {
  try {
    const { data } = inputData;
    const trimmedPath = data.path.replace(/^\/+|\/+$/g, '');
    const supportedMethods = data.methods.filter((method) =>
      supportedHttpMethods().includes(method)
    );
    let inventory = HeartbeatCache.getInventory();
    if (inventory && inventory.api && _.isArray(inventory.api.routes)) {
      const existingRoute = inventory.api.routes.find(
        (route) => route.path === trimmedPath
      );
      if (existingRoute) {
        existingRoute.addMethods(supportedMethods);
      } else {
        inventory.api.addRoute(
          new Route(trimmedPath, supportedMethods, data.host)
        );
      }
    } else {
      inventory = new Inventory(
        new Api([new Route(trimmedPath, supportedMethods, data.host)])
      );
    }

    HeartbeatCache.cacheInventory(inventory);
  } catch (error) {
    Logger.write(
      Logger.ERROR && `api.StoreRoute: Failed to store route: ${error}`
    );
  }
}

function parseHttpData(data) {
  try {
    const inputData = data.data;
    let securityActivity = HeartbeatCache.getReport(inputData.poSessionId);
    const requestHeaders = inputData.requestHeaders
      ? inputData.requestHeaders
      : securityActivity?.requestHeaders;
    securityActivity = mapSecurityActivity(securityActivity, inputData, requestHeaders);
    HeartbeatCache.cacheReport(securityActivity);
    return inputData;
  } catch (error) {
    Logger.write(
      Logger.ERROR && `api.parseHttpData: Failed to parse http data: ${error}`
    );
    return {};
  }
}

function mapSecurityActivity(securityActivity, inputData, requestHeaders) {
  if (!securityActivity) {
    securityActivity = new SecurityActivity();
    securityActivity.date = new Date();
    securityActivity.duration = 0;
    securityActivity.closed = false;
    securityActivity.requestId = inputData.poSessionId;
  }
  securityActivity.url = inputData.url;
  securityActivity.requestVerb = inputData.method;
  securityActivity.requestPath = inputData.requestPath?.replace(
    /^\/+|\/+$/g,
    ''
  );
  securityActivity.user = inputData.user;
  securityActivity.queryParams = inputData.queryParams;
  securityActivity.host = inputData.host;
  securityActivity.pathParams = inputData.pathParams;
  securityActivity.ipAddresses = [inputData.sourceIP];
  securityActivity.requestHeaders = inputData.requestHeaders;
  securityActivity.responseHeaders = inputData.responseHeaders;
  securityActivity.requestBodySchema = getJsonSchema(
    inputData.requestBody,
    requestHeaders && requestHeaders.accept
  );
  securityActivity.responseBodySchema = getJsonSchema(inputData.responseBody, requestHeaders &&
    requestHeaders['content-type']);

  securityActivity.statusCode = inputData.statusCode;

  return securityActivity;
}

function getJsonSchema(body, headerToCheck) {
  if (body) {
    const parsedBody = _.parseIfJson(new Buffer.from(body).toString());
    if (
      _.isValidJsonRequest(headerToCheck) &&
      parsedBody
    ) {
      return toJsonSchema(parsedBody);
    }
  }
  return undefined;
}

function supportedHttpMethods() {
  return [
    'GET',
    'PUT',
    'POST',
    'DELETE',
    'PATCH',
    'HEAD',
    'OPTIONS',
    'CONNECT',
    'TRACE'
  ];
}

function parseIfJson(str) {
  try {
    return JSON.parse(str);
  } catch (e) {
    return false;
  }
}

module.exports = {
  storeRoute,
  parseHttpData
};
