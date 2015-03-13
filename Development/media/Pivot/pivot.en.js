(function() {
  var callWithJQuery;

  callWithJQuery = function(pivotModule) {
    if (typeof exports === "object" && typeof module === "object") {
      return pivotModule(require("jquery"));
    } else if (typeof define === "function" && define.amd) {
      return define(["jquery"], pivotModule);
    } else {
      return pivotModule(jQuery);
    }
  };

  callWithJQuery(function($) {
    var frFmt, frFmtInt, frFmtPct, gcr, nf, r, tpl;
    $.pivotUtilities.locales.en.renderers = $.extend({},$.pivotUtilities.renderers, 
                            $.pivotUtilities.gchart_renderers, 
                            $.pivotUtilities.d3_renderers, 
                            $.pivotUtilities.export_renderers,true)
    return $.pivotUtilities.locales.en.renderers
       
    });
}).call(this);