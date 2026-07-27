import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const workbookPath = "./output/Юля_фасады_выборка_90_Малярка.xlsx";
const sourceUrl = "https://docs.google.com/document/d/1JNChytotc_FnYacu0NHB4F_AVJ1WfvIBxDKvOsq_2RQ";
const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(workbookPath));
const sheet = workbook.worksheets.getItem("Общий итог");

sheet.getRange("A23:G40").unmerge();
sheet.getRange("A23:G40").clear({ applyTo: "all" });
sheet.getRange("A23:G23").merge();
sheet.getRange("A23").values = [["РАСХОД И СТОИМОСТЬ ГРУНТА И КРАСКИ"]];
sheet.getRange("A24:G24").values = [[
  "Материал", "Тип деталей", "Площадь, м²", "Норма, кг/м²", "Расход, кг", "Цена, ₸/кг", "Стоимость, ₸"
]];

sheet.getRange("A25:D27").values = [
  ["Краска", "Модерн", null, 0.3],
  ["Краска", "Выборка 90°", null, 0.3],
  ["Краска", "Витрина", null, 0.3],
];
sheet.getRange("C25:C27").formulas = [["=D11"], ["=D10"], ["=D12"]];
sheet.getRange("E25:E27").formulas = [["=C25*D25"], ["=C26*D26"], ["=C27*D27"]];
sheet.getRange("F25:F27").values = [[12000], [12000], [12000]];
sheet.getRange("G25:G27").formulas = [["=E25*F25"], ["=E26*F26"], ["=E27*F27"]];
sheet.getRange("A28:G28").values = [["Краска — итого", null, null, null, null, null, null]];
sheet.getRange("C28").formulas = [["=SUM(C25:C27)"]];
sheet.getRange("E28").formulas = [["=SUM(E25:E27)"]];
sheet.getRange("G28").formulas = [["=SUM(G25:G27)"]];

sheet.getRange("A30:D32").values = [
  ["Грунт", "Модерн", null, 0.3],
  ["Грунт", "Выборка 90°", null, 0.6],
  ["Грунт", "Витрина", null, 0.6],
];
sheet.getRange("C30:C32").formulas = [["=D11"], ["=D10"], ["=D12"]];
sheet.getRange("E30:E32").formulas = [["=C30*D30"], ["=C31*D31"], ["=C32*D32"]];
sheet.getRange("F30:F32").values = [[5000], [5000], [5000]];
sheet.getRange("G30:G32").formulas = [["=E30*F30"], ["=E31*F31"], ["=E32*F32"]];
sheet.getRange("A33:G33").values = [["Грунт — итого", null, null, null, null, null, null]];
sheet.getRange("C33").formulas = [["=SUM(C30:C32)"]];
sheet.getRange("E33").formulas = [["=SUM(E30:E32)"]];
sheet.getRange("G33").formulas = [["=SUM(G30:G32)"]];

sheet.getRange("A35:G35").values = [["Стоимость ЛКМ", null, null, null, null, null, null]];
sheet.getRange("G35").formulas = [["=G28+G33"]];
sheet.getRange("A36:G36").values = [["Стоимость работ + ЛКМ", null, null, null, null, null, null]];
sheet.getRange("G36").formulas = [["=D21+G35"]];

sheet.getRange("A38:G38").merge();
sheet.getRange("A38").values = [["Принято для расчёта: витрины считаются по норме грунта для выборки — 0,600 кг/м², так как в деталях есть выборка под стекло."]];
sheet.getRange("A39:G39").merge();
sheet.getRange("A39").values = [["Источник норм: Реестр норм расхода Малярка — Google Drive"]];
sheet.getRange("A40:G40").merge();
sheet.getRange("A40").values = [[sourceUrl]];

const headerStyle = { fill: "#4472C4", font: { bold: true, color: "#FFFFFF" }, borders: { preset: "all", style: "thin", color: "#D9E2F3" }, horizontalAlignment: "center", wrapText: true };
sheet.getRange("A23:G23").format = { fill: "#1F4E78", font: { bold: true, color: "#FFFFFF", fontSize: 13 }, horizontalAlignment: "center", rowHeight: 26 };
sheet.getRange("A24:G24").format = headerStyle;
sheet.getRange("A25:G27").format = { fill: "#DDEBF7", borders: { preset: "all", style: "thin", color: "#D9D9D9" } };
sheet.getRange("A30:G32").format = { fill: "#FFF2CC", borders: { preset: "all", style: "thin", color: "#D9D9D9" } };
sheet.getRange("A28:G28").format = { fill: "#BDD7EE", font: { bold: true }, borders: { preset: "all", style: "medium", color: "#5B9BD5" } };
sheet.getRange("A33:G33").format = { fill: "#FFE699", font: { bold: true }, borders: { preset: "all", style: "medium", color: "#BF9000" } };
sheet.getRange("A35:G35").format = { fill: "#E2F0D9", font: { bold: true }, borders: { preset: "all", style: "medium", color: "#70AD47" } };
sheet.getRange("A36:G36").format = { fill: "#C6E0B4", font: { bold: true, color: "#006100" }, borders: { preset: "all", style: "medium", color: "#70AD47" } };
sheet.getRange("A38:G40").format = { fill: "#F2F2F2", font: { italic: true, color: "#595959" }, wrapText: true };

sheet.getRange("C25:C33").format.numberFormat = "0.000000";
sheet.getRange("D25:D32").format.numberFormat = "0.000";
sheet.getRange("E25:E33").format.numberFormat = "0.000";
sheet.getRange("F25:G36").format.numberFormat = '#,##0.00 "₸"';
sheet.getRange("A24:G36").format.verticalAlignment = "center";
sheet.getRange("A24:G36").format.rowHeight = 22;
sheet.getRange("A38:G40").format.rowHeight = 28;
sheet.getRange("A1:G40").format.font = { name: "Carlito", size: 11 };
sheet.getRange("A1:A40").format.columnWidth = 24;
sheet.getRange("B1:B40").format.columnWidth = 20;
sheet.getRange("C1:C40").format.columnWidth = 15;
sheet.getRange("D1:D40").format.columnWidth = 16;
sheet.getRange("E1:E40").format.columnWidth = 16;
sheet.getRange("F1:F40").format.columnWidth = 16;
sheet.getRange("G1:G40").format.columnWidth = 18;

const exported = await SpreadsheetFile.exportXlsx(workbook);
await exported.save(workbookPath);
const preview = await workbook.render({ sheetName: "Общий итог", range: "A1:G40", scale: 1.2, format: "png" });
await fs.writeFile("./output/lkm_summary.png", new Uint8Array(await preview.arrayBuffer()));
const preview6010 = await workbook.render({ sheetName: "6010-R90B", range: "A1:I33", scale: 1, format: "png" });
await fs.writeFile("./output/lkm_6010.png", new Uint8Array(await preview6010.arrayBuffer()));
const preview1000 = await workbook.render({ sheetName: "1000-N", range: "A1:I22", scale: 1, format: "png" });
await fs.writeFile("./output/lkm_1000.png", new Uint8Array(await preview1000.arrayBuffer()));

console.log((await workbook.inspect({ kind: "table", range: "Общий итог!A15:G40", include: "values,formulas", tableMaxRows: 30, tableMaxCols: 7, tableMaxCellChars: 160 })).ndjson);
console.log((await workbook.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options: { useRegex: true, maxResults: 100 }, summary: "formula errors" })).ndjson);
