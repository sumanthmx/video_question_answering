"use strict";

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault").default;
var _interopRequireWildcard = require("@babel/runtime/helpers/interopRequireWildcard").default;
Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.AppCacheProvider = AppCacheProvider;
var React = _interopRequireWildcard(require("react"));
var _react2 = require("@emotion/react");
var _createCache = _interopRequireDefault(require("./createCache"));
var _jsxRuntime = require("react/jsx-runtime");
const defaultEmotionCache = (0, _createCache.default)();
function AppCacheProvider({
  emotionCache = defaultEmotionCache,
  children
}) {
  return /*#__PURE__*/(0, _jsxRuntime.jsx)(_react2.CacheProvider, {
    value: emotionCache,
    children: children
  });
}