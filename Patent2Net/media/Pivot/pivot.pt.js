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
    nf = $.pivotUtilities.numberFormat;
    tpl = $.pivotUtilities.aggregatorTemplates;
    r = $.pivotUtilities.renderers;
    gcr = $.pivotUtilities.gchart_renderers;
    frFmt = nf({
      thousandsSep: ".",
      decimalSep: ","
    });
    frFmtInt = nf({
      digitsAfterDecimal: 0,
      thousandsSep: ".",
      decimalSep: ","
    });
    frFmtPct = nf({
      digitsAfterDecimal: 2,
      scaler: 100,
      suffix: "%",
      thousandsSep: ".",
      decimalSep: ","
    });
    return $.pivotUtilities.locales.pt = {
      localeStrings: {
        renderError: "Ocorreu um erro ao renderizar os resultados da Tabela Dinamica.",
        computeError: "Ocorreu um erro ao computar os resultados da Tabela Dinamica.",
        uiRenderError: "Ocorreu um erro ao renderizar a interface da Tabela Dinamica.",
        selectAll: "Selecionar Tudo",
        selectNone: "Selecionar Nenhum",
        tooMany: "(demais para listar)",
        filterResults: "Filtrar resultados",
        totals: "Totais",
        vs: "vs",
        by: "por"
      },
      aggregators: {
        "Contagem": tpl.count(frFmtInt),
        "Contagem de Valores Unicos": tpl.countUnique(frFmtInt),
        "Lista de Valores Unicos": tpl.listUnique(", "),
        "Soma": tpl.sum(frFmt),
        "Soma de Inteiros": tpl.sum(frFmtInt),
        "Media": tpl.average(frFmt),
        "Soma sobre Soma": tpl.sumOverSum(frFmt),
        "Limite Superior a 80%": tpl.sumOverSumBound80(true, frFmt),
        "Limite Inferior a 80%": tpl.sumOverSumBound80(false, frFmt),
        "Soma como Fracao do Total": tpl.fractionOf(tpl.sum(), "total", frFmtPct),
        "Soma como Fracao da Linha": tpl.fractionOf(tpl.sum(), "row", frFmtPct),
        "Soma como Fracao da Coluna": tpl.fractionOf(tpl.sum(), "col", frFmtPct),
        "Contagem como Fracao do Total": tpl.fractionOf(tpl.count(), "total", frFmtPct),
        "Contagem como Fracao da Linha": tpl.fractionOf(tpl.count(), "row", frFmtPct),
        "Contagem como Fracao da Coluna": tpl.fractionOf(tpl.count(), "col", frFmtPct)
      },
      renderers: {
        "Tabela": r["Table"],
        "Tabela com Barras": r["Table Barchart"],
        "Tabela com Mapa de Calor": r["Heatmap"],
        "Tabela com Mapa de Calor por Linhas": r["Row Heatmap"],
        "Tabela com Mapa de Calor por Colunas": r["Col Heatmap"],
        "Grafico de Linhas": $.pivotUtilities.gchart_renderers["Line Chart"],
        "Grafico de Barras": $.pivotUtilities.gchart_renderers["Bar Chart"],
        "Grafico de Barras Empilhadas": $.pivotUtilities.gchart_renderers["Stacked Bar Chart"],
        "Grafico de Area": $.pivotUtilities.gchart_renderers["Area Chart"],
        "Grafico de Arvore": $.pivotUtilities.d3_renderers["Treemap"],
        "Exportar Excel" : $.pivotUtilities.export_renderers ["TSV Export"]
      } 
    };
  });

}).call(this);

//# sourceMappingURL=pivot.pt.js.map